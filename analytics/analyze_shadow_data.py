#!/usr/bin/env python3
"""
LangCache Shadow Mode Analytics

This script analyzes shadow mode data to provide insights on cache performance,
hit rates, latency improvements, and potential cost savings.

Usage:
    python analyze_shadow_data.py --source redis
    python analyze_shadow_data.py --source file --file shadow_mode.log
"""

import json
import argparse
import statistics
from datetime import datetime, timedelta
from typing import List, Dict, Any
import redis

class ShadowDataAnalyzer:
    def __init__(self):
        self.data = []
    
    def load_from_redis(self, redis_url: str = "redis://localhost:6379"):
        """Load shadow data from Redis"""
        try:
            r = redis.from_url(redis_url)
            keys = r.keys("shadow:*")
            
            for key in keys:
                data = r.get(key)
                if data:
                    self.data.append(json.loads(data))
            
            print(f"Loaded {len(self.data)} records from Redis")
        except Exception as e:
            print(f"Error loading from Redis: {e}")
    
    def load_from_file(self, filename: str):
        """Load shadow data from log file"""
        try:
            with open(filename, 'r') as f:
                for line in f:
                    if line.strip():
                        self.data.append(json.loads(line))
            
            print(f"Loaded {len(self.data)} records from {filename}")
        except Exception as e:
            print(f"Error loading from file: {e}")
    
    def analyze(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of shadow data"""
        if not self.data:
            return {"error": "No data to analyze"}
        
        # Basic metrics
        total_queries = len(self.data)
        cache_hits = sum(1 for d in self.data if d.get('cache_hit', False))
        cache_misses = total_queries - cache_hits
        hit_rate = (cache_hits / total_queries) * 100 if total_queries > 0 else 0
        
        # Latency analysis
        llm_latencies = [d.get('llm_latency_ms', 0) for d in self.data if d.get('llm_latency_ms')]
        cache_latencies = [d.get('cache_latency_ms', 0) for d in self.data if d.get('cache_latency_ms')]
        
        avg_llm_latency = statistics.mean(llm_latencies) if llm_latencies else 0
        avg_cache_latency = statistics.mean(cache_latencies) if cache_latencies else 0
        latency_improvement = avg_llm_latency - avg_cache_latency
        
        # Similarity analysis
        similarities = [d.get('similarity_score', 0) for d in self.data if d.get('similarity_score') is not None]
        avg_similarity = statistics.mean(similarities) if similarities else 0
        
        # Time-based analysis
        time_analysis = self._analyze_by_time()
        
        # Cost estimation (assuming $0.002 per 1K tokens, average 100 tokens per response)
        estimated_tokens_saved = cache_hits * 100  # Rough estimate
        estimated_cost_savings = (estimated_tokens_saved / 1000) * 0.002
        
        return {
            "summary": {
                "total_queries": total_queries,
                "cache_hits": cache_hits,
                "cache_misses": cache_misses,
                "hit_rate_percent": round(hit_rate, 2),
                "avg_llm_latency_ms": round(avg_llm_latency, 2),
                "avg_cache_latency_ms": round(avg_cache_latency, 2),
                "latency_improvement_ms": round(latency_improvement, 2),
                "avg_similarity_score": round(avg_similarity, 3),
                "estimated_cost_savings_usd": round(estimated_cost_savings, 4)
            },
            "performance": {
                "latency_percentiles": self._calculate_percentiles(llm_latencies),
                "cache_latency_percentiles": self._calculate_percentiles(cache_latencies),
                "similarity_distribution": self._analyze_similarity_distribution(similarities)
            },
            "time_analysis": time_analysis,
            "recommendations": self._generate_recommendations(hit_rate, avg_similarity, latency_improvement)
        }
    
    def _analyze_by_time(self) -> Dict[str, Any]:
        """Analyze data by time periods"""
        if not self.data:
            return {}
        
        # Group by hour
        hourly_data = {}
        for record in self.data:
            try:
                timestamp = datetime.fromisoformat(record.get('timestamp', '').replace('Z', '+00:00'))
                hour_key = timestamp.strftime('%Y-%m-%d %H:00')
                
                if hour_key not in hourly_data:
                    hourly_data[hour_key] = {'total': 0, 'hits': 0}
                
                hourly_data[hour_key]['total'] += 1
                if record.get('cache_hit', False):
                    hourly_data[hour_key]['hits'] += 1
            except:
                continue
        
        # Calculate hourly hit rates
        hourly_hit_rates = {}
        for hour, data in hourly_data.items():
            hit_rate = (data['hits'] / data['total']) * 100 if data['total'] > 0 else 0
            hourly_hit_rates[hour] = round(hit_rate, 2)
        
        return {
            "hourly_hit_rates": hourly_hit_rates,
            "peak_hour": max(hourly_data.keys(), key=lambda h: hourly_data[h]['total']) if hourly_data else None,
            "total_hours_analyzed": len(hourly_data)
        }
    
    def _calculate_percentiles(self, values: List[float]) -> Dict[str, float]:
        """Calculate latency percentiles"""
        if not values:
            return {}
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        return {
            "p50": sorted_values[int(n * 0.5)],
            "p90": sorted_values[int(n * 0.9)],
            "p95": sorted_values[int(n * 0.95)],
            "p99": sorted_values[int(n * 0.99)]
        }
    
    def _analyze_similarity_distribution(self, similarities: List[float]) -> Dict[str, int]:
        """Analyze distribution of similarity scores"""
        if not similarities:
            return {}
        
        distribution = {
            "very_high_0.9+": 0,
            "high_0.8-0.9": 0,
            "medium_0.7-0.8": 0,
            "low_0.6-0.7": 0,
            "very_low_<0.6": 0
        }
        
        for sim in similarities:
            if sim >= 0.9:
                distribution["very_high_0.9+"] += 1
            elif sim >= 0.8:
                distribution["high_0.8-0.9"] += 1
            elif sim >= 0.7:
                distribution["medium_0.7-0.8"] += 1
            elif sim >= 0.6:
                distribution["low_0.6-0.7"] += 1
            else:
                distribution["very_low_<0.6"] += 1
        
        return distribution
    
    def _generate_recommendations(self, hit_rate: float, avg_similarity: float, latency_improvement: float) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if hit_rate < 20:
            recommendations.append("Low hit rate detected. Consider expanding your cache with more diverse content.")
        elif hit_rate > 60:
            recommendations.append("Excellent hit rate! LangCache would provide significant performance benefits.")
        
        if avg_similarity < 0.7:
            recommendations.append("Low similarity scores. Consider adjusting similarity thresholds or improving query preprocessing.")
        
        if latency_improvement > 500:
            recommendations.append("Significant latency improvements possible. LangCache could greatly enhance user experience.")
        
        if not recommendations:
            recommendations.append("Shadow mode data looks good. Consider proceeding with production deployment.")
        
        return recommendations
    
    def print_report(self):
        """Print a formatted analysis report"""
        analysis = self.analyze()
        
        if "error" in analysis:
            print(f"Error: {analysis['error']}")
            return
        
        print("=" * 60)
        print("LANGCACHE SHADOW MODE ANALYSIS REPORT")
        print("=" * 60)
        
        summary = analysis["summary"]
        print(f"\n📊 SUMMARY")
        print(f"Total Queries: {summary['total_queries']:,}")
        print(f"Cache Hits: {summary['cache_hits']:,}")
        print(f"Cache Misses: {summary['cache_misses']:,}")
        print(f"Hit Rate: {summary['hit_rate_percent']}%")
        
        print(f"\n⚡ PERFORMANCE")
        print(f"Average LLM Latency: {summary['avg_llm_latency_ms']}ms")
        print(f"Average Cache Latency: {summary['avg_cache_latency_ms']}ms")
        print(f"Latency Improvement: {summary['latency_improvement_ms']}ms")
        print(f"Average Similarity Score: {summary['avg_similarity_score']}")
        
        print(f"\n💰 COST IMPACT")
        print(f"Estimated Cost Savings: ${summary['estimated_cost_savings_usd']}")
        
        print(f"\n🎯 RECOMMENDATIONS")
        for rec in analysis["recommendations"]:
            print(f"• {rec}")
        
        print("\n" + "=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Analyze LangCache shadow mode data")
    parser.add_argument("--source", choices=["redis", "file"], required=True,
                       help="Data source: redis or file")
    parser.add_argument("--file", help="Log file path (required if source=file)")
    parser.add_argument("--redis-url", default="redis://localhost:6379",
                       help="Redis URL (default: redis://localhost:6379)")
    
    args = parser.parse_args()
    
    analyzer = ShadowDataAnalyzer()
    
    if args.source == "redis":
        analyzer.load_from_redis(args.redis_url)
    elif args.source == "file":
        if not args.file:
            print("Error: --file is required when source=file")
            return
        analyzer.load_from_file(args.file)
    
    analyzer.print_report()

if __name__ == "__main__":
    main()
