// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Tourism System: DOM loaded, initializing...');
    
    // Initialize event listeners
    const input = document.getElementById('queryInput');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                processQuery();
            }
        });
        input.focus();
    } else {
        console.error('Query input element not found!');
    }
    
    console.log('Tourism System: Initialization complete');
});

// Example queries
const examples = [
    "I'm going to go to Bangalore, let's plan my trip.",
    "I'm going to go to Bangalore, what is the temperature there",
    "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"
];

// Fill example query
function fillExample(index) {
    console.log('Filling example', index);
    const input = document.getElementById('queryInput');
    if (input) {
        input.value = examples[index];
        input.focus();
    } else {
        console.error('Input element not found');
    }
}

// Process query
async function processQuery() {
    console.log('Processing query...');
    const input = document.getElementById('queryInput');
    if (!input) {
        console.error('Input element not found');
        showError('Input element not found');
        return;
    }
    
    const query = input.value.trim();
    
    if (!query) {
        showError('Please enter a query');
        return;
    }
    
    console.log('Query:', query);
    
    // Hide previous responses/errors
    hideError();
    hideResponse();
    
    // Show loading state
    setLoading(true);
    
    try {
        console.log('Sending request to /api/query');
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);
        
        if (data.success) {
            showResponse(data.response);
        } else {
            showError(data.error || 'An error occurred while processing your query');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error: ' + error.message);
    } finally {
        setLoading(false);
    }
}

// Show response
function showResponse(response) {
    const section = document.getElementById('responseSection');
    const content = document.getElementById('responseContent');
    
    // Format the response - convert newlines to <br> and preserve formatting
    const formattedResponse = response
        .replace(/\n/g, '<br>')
        .replace(/In ([^,]+)/g, '<strong>In $1</strong>');
    
    content.innerHTML = formattedResponse;
    section.style.display = 'block';
    
    // Scroll to response
    section.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Hide response
function hideResponse() {
    document.getElementById('responseSection').style.display = 'none';
}

// Clear response
function clearResponse() {
    hideResponse();
    document.getElementById('queryInput').focus();
}

// Show error
function showError(message) {
    const section = document.getElementById('errorSection');
    const content = document.getElementById('errorMessage');
    
    content.textContent = message;
    section.style.display = 'block';
    
    // Scroll to error
    section.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Hide error
function hideError() {
    document.getElementById('errorSection').style.display = 'none';
}

// Set loading state
function setLoading(loading) {
    const btn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    
    if (loading) {
        btn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
    } else {
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Make functions globally available
window.fillExample = fillExample;
window.processQuery = processQuery;
window.clearResponse = clearResponse;

