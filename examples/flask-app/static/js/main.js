document.addEventListener('DOMContentLoaded', function() {
    const queryInput = document.getElementById('query-input');
    const submitButton = document.getElementById('submit-query');
    const cachedChat = document.getElementById('cached-chat');
    const cachedTimeDisplay = document.getElementById('cached-time');
    const llmModelSelect = document.getElementById('llm-model');
    const embeddingModelSelect = document.getElementById('embedding-model');

    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const refreshLogsBtn = document.getElementById('refresh-logs');

    // Clear welcome messages when first query is submitted
    let isFirstQuery = true;

    submitButton.addEventListener('click', handleSubmit);
    queryInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSubmit();
        }
    });

    // Tab switching
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');

            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            document.getElementById(targetTab + '-tab').classList.add('active');

            // Load logs if switching to logs tab
            if (targetTab === 'logs') {
                loadLogs();
            }
        });
    });

    // Refresh logs button
    refreshLogsBtn.addEventListener('click', loadLogs);

    function handleSubmit() {
        const query = queryInput.value.trim();
        if (!query) return;

        // Clear ALL previous messages for single response behavior
        cachedChat.innerHTML = '';
        isFirstQuery = false;

        // Add user message to the panel
        addMessage(cachedChat, query, 'user');

        // Add loading indicator
        const cachedLoadingMsg = addLoadingMessage(cachedChat);

        // Reset time display
        cachedTimeDisplay.textContent = '';

        // Make request to the endpoint
        fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                use_cache: true,
                llm_model: llmModelSelect.value,
                embedding_model: embeddingModelSelect.value
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            cachedChat.removeChild(cachedLoadingMsg);

            // Display response time
            cachedTimeDisplay.textContent = `${data.time_taken.toFixed(2)}s`;

            // Add response message with enhanced source indication
            addResponseMessage(cachedChat, data.response, data.source === 'cache', data.similarity);
        })
        .catch(error => {
            cachedChat.removeChild(cachedLoadingMsg);
            addErrorMessage(cachedChat, 'Error: ' + error.message);
            console.error('Error:', error);
        });

        // Clear input
        queryInput.value = '';
    }

    function addMessage(container, text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        messageDiv.textContent = text;
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
        return messageDiv;
    }

    function addResponseMessage(container, text, fromCache, similarity) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'response');

        // Add simple source indicator
        const sourceIndicator = document.createElement('div');
        sourceIndicator.classList.add('source-indicator');

        if (fromCache) {
            sourceIndicator.classList.add('cache');

            // Database icon for cache
            const cacheIcon = document.createElement('span');
            cacheIcon.classList.add('source-icon');
            cacheIcon.innerHTML = '🗄️';
            cacheIcon.style.fontSize = '16px';
            cacheIcon.style.marginRight = '6px';

            const cacheText = document.createElement('span');
            cacheText.textContent = 'Served from Redis LangCache';
            cacheText.style.color = '#4CAF50';
            cacheText.style.fontWeight = '600';
            if (similarity) {
                const similarityPercent = Math.round(similarity * 100);
                cacheText.textContent += ` (${similarityPercent}%)`;
            }

            sourceIndicator.appendChild(cacheIcon);
            sourceIndicator.appendChild(cacheText);
        } else {
            sourceIndicator.classList.add('llm');

            // Red checkmark for LLM
            const llmIcon = document.createElement('span');
            llmIcon.classList.add('source-icon');
            llmIcon.innerHTML = '✓';
            llmIcon.style.color = '#F44336';

            const llmText = document.createElement('span');
            llmText.textContent = 'From LLM';

            sourceIndicator.appendChild(llmIcon);
            sourceIndicator.appendChild(llmText);
        }

        // Add the response text
        const responseText = document.createElement('div');
        responseText.classList.add('response-content');
        responseText.textContent = text;

        // Add elements to the message div
        messageDiv.appendChild(sourceIndicator);
        messageDiv.appendChild(responseText);

        container.appendChild(messageDiv);
        // Remove auto-scrolling - let user control scrolling
        return messageDiv;
    }

    function addLoadingMessage(container) {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'loading', 'response');

        // Enhanced loading indicator
        const loadingContent = document.createElement('div');
        loadingContent.classList.add('loading-content');

        // Loading text
        const loadingText = document.createElement('div');
        loadingText.classList.add('loading-text');
        loadingText.textContent = 'Generating response...';

        // Loading animation
        const loadingDots = document.createElement('div');
        loadingDots.classList.add('loading-dots');

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            loadingDots.appendChild(dot);
        }

        loadingContent.appendChild(loadingText);
        loadingContent.appendChild(loadingDots);
        loadingDiv.appendChild(loadingContent);

        container.appendChild(loadingDiv);
        container.scrollTop = container.scrollHeight;
        return loadingDiv;
    }

    function addErrorMessage(container, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'response', 'error');
        messageDiv.textContent = text;
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
        return messageDiv;
    }

    function loadLogs() {
        fetch('/logs')
            .then(response => response.json())
            .then(data => {
                updateLogsStats(data);
                updateLogsTable(data.operations);
            })
            .catch(error => {
                console.error('Error loading logs:', error);
            });
    }

    function updateLogsStats(data) {
        document.getElementById('total-ops').textContent = data.total_operations;
        document.getElementById('cache-hits').textContent = data.cache_hits;
        document.getElementById('cache-misses').textContent = data.cache_misses;

        // Update Cache ID at the top
        if (data.operations.length > 0) {
            const cacheId = data.operations[0].cache_id || 'N/A';
            document.getElementById('cache-id-value').textContent = cacheId;
        }
    }

    function updateLogsTable(operations) {
        const tbody = document.getElementById('logs-tbody');

        if (operations.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="no-logs">No operations logged yet. Start chatting to see logs!</td></tr>';
            return;
        }

        tbody.innerHTML = '';

        // Show most recent operations first
        operations.reverse().forEach(op => {
            const row = document.createElement('tr');

            const sourceClass = op.source === 'cache' ? 'source-cache' : 'source-llm';
            const sourceText = op.source === 'cache' ? '🗄️ Redis LangCache' : '✓ LLM';
            const matchedQuery = op.matched_query || '-';
            const similarity = op.similarity ? `${Math.round(op.similarity * 100)}%` : '-';
            const responseTime = `${(op.response_time * 1000).toFixed(2)}ms`;

            row.innerHTML = `
                <td>${op.timestamp}</td>
                <td class="query-cell">${op.query}</td>
                <td class="${sourceClass}">${sourceText}</td>
                <td class="query-cell">${matchedQuery}</td>
                <td class="similarity-score">${similarity}</td>
                <td>${responseTime}</td>
                <td>${op.llm_model}</td>
            `;

            tbody.appendChild(row);
        });
    }

    // Load logs on page load
    loadLogs();
});