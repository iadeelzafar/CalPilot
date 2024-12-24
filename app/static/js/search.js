let searchTimeout = null;

function debounce(func, wait) {
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(searchTimeout);
            func(...args);
        };
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(later, wait);
    };
}

function updateCallsList() {
    const search = document.getElementById('search').value;
    const company = document.getElementById('company-filter').value;
    const dateFrom = document.getElementById('date-from').value;
    const dateTo = document.getElementById('date-to').value;
    
    const url = `/api/calls/search?query=${search}&company=${company}&date_from=${dateFrom}&date_to=${dateTo}`;
    
    // Show loading state
    document.getElementById('calls-list').classList.add('animate-pulse');
    
    fetch(url)
        .then(response => response.json())
        .then(calls => {
            const callsList = document.getElementById('calls-list');
            callsList.innerHTML = calls.map(call => `
                <div class="border rounded p-4 hover:bg-gray-50 cursor-pointer call-item" 
                     data-call-id="${call.id}">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="font-semibold">${call.call_metadata.title}</h3>
                            <p class="text-sm text-gray-600">
                                ${call.formatted_date} • ${call.duration_mins} minutes
                            </p>
                        </div>
                        <div class="text-sm text-gray-500">
                            <i class="fas fa-users"></i> ${call.call_metadata.parties.length}
                        </div>
                    </div>
                    <p class="text-sm text-gray-500 mt-2">
                        Companies: 
                        ${call.companies.map(company => `
                            <span class="inline-block bg-gray-100 rounded px-2 py-1 text-xs">
                                ${company.charAt(0).toUpperCase() + company.slice(1)}
                            </span>
                        `).join(' ')}
                    </p>
                </div>
            `).join('');
            
            // Remove loading state
            callsList.classList.remove('animate-pulse');
            
            // Reattach event listeners
            attachCallItemListeners();
        })
        .catch(error => {
            console.error('Error fetching calls:', error);
            document.getElementById('calls-list').classList.remove('animate-pulse');
        });
}

// Attach event listeners
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('search').addEventListener('input', 
        debounce(updateCallsList, 300));
    document.getElementById('company-filter').addEventListener('change', 
        updateCallsList);
    document.getElementById('date-from').addEventListener('change', 
        updateCallsList);
    document.getElementById('date-to').addEventListener('change', 
        updateCallsList);
});
