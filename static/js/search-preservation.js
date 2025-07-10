// Search text preservation for HTMX search engine changes
document.addEventListener('DOMContentLoaded', function() {
    // Store search text globally
    window.preservedSearchText = '';
    window.searchHadFocus = false;
    
    // Listen for HTMX before request
    document.body.addEventListener('htmx:beforeRequest', function(evt) {
        // Only handle search engine changes
        if (evt.detail.target.id === 'search-section') {
            console.log('Before HTMX request'); // Debug
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                window.preservedSearchText = searchInput.value;
                window.searchHadFocus = document.activeElement === searchInput;
                console.log('Preserved text:', window.preservedSearchText); // Debug
                console.log('Had focus:', window.searchHadFocus); // Debug
            }
        }
    });
    
    // Listen for HTMX after swap (when new content is in DOM)
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        // Only handle search engine changes
        if (evt.detail.target.id === 'search-section') {
            console.log('After HTMX swap'); // Debug
            console.log('Restoring text:', window.preservedSearchText); // Debug
            
            const searchInput = document.getElementById('search-input');
            if (searchInput && window.preservedSearchText) {
                searchInput.value = window.preservedSearchText;
                if (window.searchHadFocus) {
                    searchInput.focus();
                    // Set cursor to end of text
                    searchInput.setSelectionRange(window.preservedSearchText.length, window.preservedSearchText.length);
                }
                console.log('Text restored successfully'); // Debug
            }
        }
    });
});