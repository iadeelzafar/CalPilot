document.addEventListener('DOMContentLoaded', () => {
    // Question template handling
    document.getElementById('question-template').addEventListener('change', function() {
        const questionInput = document.getElementById('question');
        questionInput.value = this.value;
    });

    // Question asking functionality
    document.getElementById('ask-button').addEventListener('click', async () => {
        const question = document.getElementById('question').value;
        if (!question) return;

        const button = document.getElementById('ask-button');
        const answerDiv = document.getElementById('answer');
        
        // Show loading state
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Loading...';
        answerDiv.innerHTML = `
            <div class="flex items-center space-x-2">
                <i class="fas fa-spinner fa-spin"></i>
                <span>Getting answer...</span>
            </div>
        `;
        answerDiv.classList.remove('hidden');

        try {
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    call_id: selectedCallId,
                    question: question
                })
            });

            const data = await response.json();
            
            // Format answer with icons
            answerDiv.innerHTML = `
                <div class="space-y-2">
                    <div class="flex items-start space-x-2">
                        <i class="fas fa-question-circle text-blue-500 mt-1"></i>
                        <p class="text-gray-600">${question}</p>
                    </div>
                    <div class="flex items-start space-x-2">
                        <i class="fas fa-comment-dots text-green-500 mt-1"></i>
                        <p>${data.answer}</p>
                    </div>
                </div>
            `;
        } catch (error) {
            answerDiv.innerHTML = `
                <div class="flex items-center space-x-2 text-red-500">
                    <i class="fas fa-exclamation-circle"></i>
                    <span>Error getting answer. Please try again.</span>
                </div>
            `;
        } finally {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-question-circle mr-2"></i>Ask Question';
        }
    });
});
