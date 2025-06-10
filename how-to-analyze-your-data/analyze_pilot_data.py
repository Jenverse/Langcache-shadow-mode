#!/usr/bin/env python3
"""
LangCache Shadow Mode Pilot Data Analyzer

Analyzes the specific dataset format for the two-week pilot experiment:
{
  "request_id": "uuid4",
  "ts_request": "2025-05-27T15:04:32.123Z",
  "query": "How do I reset my API key?",
  "rag_response": "...",
  "cache_hit": true,
  "cache_query": "How do I update my API keys?",
  "cache_response": ".....",
  "vector_distance": 0.14,
  "cached_id": "faq:api-reset:dskjfhkjsdg",
  "latency_cache_ms": 8,
  "latency_llm_ms": 612,
  "tokens_llm": 128,
  "model_name": "openai/gpt-4o-mini",
  "langcache_version": "v0.9.1"
}
"""

import json
import argparse
import statistics
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict, Counter

class PilotDataAnalyzer:
    def __init__(self):
        self.data = []
    
    def load_from_file(self, filename: str):
        """Load pilot data from JSONL file"""
        try:
            with open(filename, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():
                        try:
                            record = json.loads(line)
                            self.data.append(record)
                        except json.JSONDecodeError as e:
                            print(f"Warning: Invalid JSON on line {line_num}: {e}")
            
            print(f"✅ Loaded {len(self.data)} records from {filename}")
        except Exception as e:
            print(f"❌ Error loading from file: {e}")
    
    def analyze_pilot_metrics(self) -> Dict[str, Any]:
        """Analyze pilot experiment metrics"""
        if not self.data:
            return {}
        
        # Basic metrics
        total_queries = len(self.data)
        cache_hits = sum(1 for d in self.data if d.get('cache_hit', False))
        cache_misses = total_queries - cache_hits
        hit_rate = (cache_hits / total_queries) * 100 if total_queries > 0 else 0
        
        # Latency analysis
        llm_latencies = [d.get('latency_llm_ms', 0) for d in self.data if d.get('latency_llm_ms')]
        cache_latencies = [d.get('latency_cache_ms', 0) for d in self.data if d.get('latency_cache_ms')]
        
        avg_llm_latency = statistics.mean(llm_latencies) if llm_latencies else 0
        avg_cache_latency = statistics.mean(cache_latencies) if cache_latencies else 0
        latency_improvement = avg_llm_latency - avg_cache_latency
        
        # Vector distance analysis (similarity)
        distances = [d.get('vector_distance', 1.0) for d in self.data if d.get('vector_distance') is not None]
        similarities = [1.0 - dist for dist in distances]  # Convert distance to similarity
        avg_similarity = statistics.mean(similarities) if similarities else 0
        
        # Token analysis
        tokens = [d.get('tokens_llm', 0) for d in self.data if d.get('tokens_llm')]
        total_tokens = sum(tokens)
        avg_tokens = statistics.mean(tokens) if tokens else 0
        
        # Model usage
        models = [d.get('model_name', 'unknown') for d in self.data]
        model_counts = Counter(models)
        
        # Time-based analysis
        time_analysis = self._analyze_by_time()
        
        # Cost estimation (rough - adjust based on your pricing)
        tokens_saved = sum(d.get('tokens_llm', 0) for d in self.data if d.get('cache_hit', False))
        cost_per_1k_tokens = 0.002  # Adjust based on your model pricing
        estimated_savings = (tokens_saved / 1000) * cost_per_1k_tokens
        
        return {
            "pilot_summary": {
                "total_queries": total_queries,
                "cache_hits": cache_hits,
                "cache_misses": cache_misses,
                "hit_rate_percent": round(hit_rate, 2),
                "avg_llm_latency_ms": round(avg_llm_latency, 2),
                "avg_cache_latency_ms": round(avg_cache_latency, 2),
                "latency_improvement_ms": round(latency_improvement, 2),
                "avg_similarity_score": round(avg_similarity, 3),
                "total_tokens": total_tokens,
                "avg_tokens_per_query": round(avg_tokens, 1),
                "tokens_saved": tokens_saved,
                "estimated_cost_savings_usd": round(estimated_savings, 4)
            },
            "model_usage": dict(model_counts),
            "performance_distribution": {
                "latency_percentiles": self._calculate_percentiles(llm_latencies),
                "similarity_distribution": self._analyze_similarity_distribution(similarities),
                "vector_distance_stats": self._analyze_vector_distances(distances)
            },
            "time_analysis": time_analysis
        }
    
    def _analyze_by_time(self) -> Dict[str, Any]:
        """Analyze data by time periods"""
        if not self.data:
            return {}
        
        hourly_data = defaultdict(lambda: {'total': 0, 'hits': 0, 'latency_sum': 0})
        daily_data = defaultdict(lambda: {'total': 0, 'hits': 0})
        
        for record in self.data:
            try:
                timestamp = datetime.fromisoformat(record.get('ts_request', '').replace('Z', '+00:00'))
                hour_key = timestamp.strftime('%Y-%m-%d %H:00')
                day_key = timestamp.strftime('%Y-%m-%d')
                
                # Hourly stats
                hourly_data[hour_key]['total'] += 1
                hourly_data[hour_key]['latency_sum'] += record.get('latency_llm_ms', 0)
                if record.get('cache_hit', False):
                    hourly_data[hour_key]['hits'] += 1
                
                # Daily stats
                daily_data[day_key]['total'] += 1
                if record.get('cache_hit', False):
                    daily_data[day_key]['hits'] += 1
                    
            except Exception:
                continue
        
        # Calculate hit rates
        hourly_hit_rates = {}
        for hour, data in hourly_data.items():
            hit_rate = (data['hits'] / data['total']) * 100 if data['total'] > 0 else 0
            hourly_hit_rates[hour] = round(hit_rate, 2)
        
        daily_hit_rates = {}
        for day, data in daily_data.items():
            hit_rate = (data['hits'] / data['total']) * 100 if data['total'] > 0 else 0
            daily_hit_rates[day] = round(hit_rate, 2)
        
        return {
            "hourly_hit_rates": hourly_hit_rates,
            "daily_hit_rates": daily_hit_rates,
            "peak_hour": max(hourly_data.keys(), key=lambda k: hourly_data[k]['total']) if hourly_data else None
        }
    
    def _calculate_percentiles(self, values: List[float]) -> Dict[str, float]:
        """Calculate percentile distribution"""
        if not values:
            return {}
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        return {
            "p50": sorted_values[int(n * 0.5)],
            "p90": sorted_values[int(n * 0.9)],
            "p95": sorted_values[int(n * 0.95)],
            "p99": sorted_values[int(n * 0.99)] if n > 100 else sorted_values[-1]
        }
    
    def _analyze_similarity_distribution(self, similarities: List[float]) -> Dict[str, Any]:
        """Analyze similarity score distribution"""
        if not similarities:
            return {}
        
        high_similarity = sum(1 for s in similarities if s >= 0.8)
        medium_similarity = sum(1 for s in similarities if 0.6 <= s < 0.8)
        low_similarity = sum(1 for s in similarities if s < 0.6)
        
        return {
            "high_similarity_count": high_similarity,
            "medium_similarity_count": medium_similarity,
            "low_similarity_count": low_similarity,
            "avg_similarity": round(statistics.mean(similarities), 3) if similarities else 0
        }
    
    def _analyze_vector_distances(self, distances: List[float]) -> Dict[str, float]:
        """Analyze vector distance statistics"""
        if not distances:
            return {}
        
        return {
            "min_distance": round(min(distances), 4),
            "max_distance": round(max(distances), 4),
            "avg_distance": round(statistics.mean(distances), 4),
            "median_distance": round(statistics.median(distances), 4)
        }
    
    def print_pilot_report(self):
        """Print comprehensive pilot experiment report"""
        analysis = self.analyze_pilot_metrics()
        
        if not analysis:
            print("❌ No data to analyze")
            return
        
        print("=" * 80)
        print("🔍 LANGCACHE SHADOW MODE PILOT EXPERIMENT REPORT")
        print("=" * 80)
        
        summary = analysis["pilot_summary"]
        print(f"\n📊 EXPERIMENT SUMMARY")
        print(f"Total Queries Processed: {summary['total_queries']:,}")
        print(f"Cache Hits: {summary['cache_hits']:,}")
        print(f"Cache Misses: {summary['cache_misses']:,}")
        print(f"Overall Hit Rate: {summary['hit_rate_percent']}%")
        
        print(f"\n⚡ PERFORMANCE METRICS")
        print(f"Average LLM Latency: {summary['avg_llm_latency_ms']}ms")
        print(f"Average Cache Latency: {summary['avg_cache_latency_ms']}ms")
        print(f"Latency Improvement: {summary['latency_improvement_ms']}ms")
        print(f"Average Similarity Score: {summary['avg_similarity_score']}")
        
        print(f"\n🎯 TOKEN & COST ANALYSIS")
        print(f"Total Tokens Processed: {summary['total_tokens']:,}")
        print(f"Average Tokens per Query: {summary['avg_tokens_per_query']}")
        print(f"Tokens Saved (Cache Hits): {summary['tokens_saved']:,}")
        print(f"Estimated Cost Savings: ${summary['estimated_cost_savings_usd']}")
        
        print(f"\n🤖 MODEL USAGE")
        for model, count in analysis["model_usage"].items():
            print(f"  {model}: {count:,} queries")
        
        print(f"\n📈 PERFORMANCE DISTRIBUTION")
        perf = analysis["performance_distribution"]
        if "latency_percentiles" in perf:
            lat = perf["latency_percentiles"]
            print(f"Latency P50: {lat.get('p50', 0)}ms | P90: {lat.get('p90', 0)}ms | P95: {lat.get('p95', 0)}ms")
        
        print(f"\n🕒 TIME-BASED ANALYSIS")
        time_data = analysis["time_analysis"]
        if "peak_hour" in time_data and time_data["peak_hour"]:
            print(f"Peak Usage Hour: {time_data['peak_hour']}")
        
        print(f"\n✅ PILOT EXPERIMENT COMPLETE")
        print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Analyze LangCache shadow mode pilot data")
    parser.add_argument("--file", required=True, help="Path to shadow_mode.log file")
    
    args = parser.parse_args()
    
    analyzer = PilotDataAnalyzer()
    analyzer.load_from_file(args.file)
    analyzer.print_pilot_report()

if __name__ == "__main__":
    main()
