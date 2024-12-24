let selectedCallId = null;

function attachCallItemListeners() {
    document.querySelectorAll('.call-item').forEach(item => {
        item.addEventListener('click', async () => {
            // Update selection
            document.querySelectorAll('.call-item').forEach(i => 
                i.classList.remove('bg-blue-50'));
            item.classList.add('bg-blue-50');
            
            // Enable question asking
            selectedCallId = item.dataset.callId;
            document.getElementById('ask-button').disabled = false;
            
            // Update selected call display
            const response = await fetch(`/api/call/${selectedCallId}`);
            const call = await response.json();
            document.getElementById('selected-call').textContent = 
                `Selected: ${call.call_metadata.title}`;
            
            // Load call summary
            loadCallSummary(selectedCallId);
        });
    });
}

async function loadCallSummary(callId) {
    const summaryDiv = document.getElementById('call-summary');
    const placeholderDiv = document.getElementById('summary-placeholder');
    
    try {
        summaryDiv.classList.add('animate-pulse');
        const response = await fetch(`/api/call/${callId}/summary`);
        const summary = await response.json();
        
        // Update summary sections
        document.getElementById('summary-duration').textContent = 
            `${summary.duration_mins}`;
        document.getElementById('summary-participants').textContent = 
            `${summary.participant_count} participants`;
        
        // Update keywords
        const keywordsDiv = document.getElementById('summary-keywords');
        keywordsDiv.innerHTML = Object.keys(summary.keywords).map(keyword => `
            <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded keyword-tag">
                ${keyword}
            </span>
        `).join('');
        
        // Update AI summary
        document.getElementById('summary-text').textContent = summary.summary;
        
        // Show summary section
        summaryDiv.classList.remove('hidden', 'animate-pulse');
        placeholderDiv.classList.add('hidden');
    } catch (error) {
        console.error('Error loading call summary:', error);
        placeholderDiv.textContent = 'Error loading summary';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    attachCallItemListeners();
});
