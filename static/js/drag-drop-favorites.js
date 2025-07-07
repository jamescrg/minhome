/**
 * Favorite links drag-and-drop functionality
 * Handles dragging individual favorite links with timer-based detection
 */

/**
 * Initialize favorite link drag-and-drop
 */
function initializeFavoriteDragDrop() {
    const favoriteLinks = document.querySelectorAll('.favorite-drag-link');
    const favoriteItems = document.querySelectorAll('.favorite-item');
    
    // Set up favorite items (list items) with drag and click behavior
    favoriteItems.forEach((item, index) => {
        const link = item.querySelector('.favorite-drag-link');
        if (!link) return;
        
        let dragTimeout;
        let isDragging = false;
        
        // Mouse down on the item starts potential drag
        item.addEventListener('mousedown', function(e) {
            dragTimeout = setTimeout(() => {
                // After delay, enable dragging on the item
                item.draggable = true;
                isDragging = true;
                item.style.cursor = 'grabbing';
            }, 150); // 150ms delay before drag starts
        });
        
        // Mouse up cancels drag or allows navigation
        item.addEventListener('mouseup', function(e) {
            clearTimeout(dragTimeout);
            if (!isDragging) {
                // Short click - check if it was on the link for navigation
                if (e.target === link || link.contains(e.target)) {
                    window.location.href = link.href;
                }
            } else {
                // Was dragging - clean up
                item.draggable = false;
                isDragging = false;
                item.style.cursor = '';
            }
        });
        
        // Prevent default link behavior during drag
        link.addEventListener('click', function(e) {
            if (isDragging) {
                e.preventDefault();
                return false;
            }
        });
        
        // Drag events on the item
        item.addEventListener('dragstart', function(e) {
            handleFavoriteDragStart.call(link, e); // Call with link context
        });
        item.addEventListener('dragend', function(e) {
            handleFavoriteDragEnd.call(link, e); // Call with link context
        });
    });
    
    // Set up favorite items as drop targets - dropping on any link positions below it
    favoriteItems.forEach((item, index) => {
        item.addEventListener('dragover', handleFavoriteDragOver);
        item.addEventListener('drop', handleFavoriteDrop);
        item.addEventListener('dragenter', function(e) {
            e.preventDefault();
        });
        
        // Style for better drop targeting
        item.style.minHeight = '2rem'; // Make drop target bigger
        item.style.display = 'flex';
        item.style.alignItems = 'center';
    });
}

/**
 * Create extended drop zones for favorites (currently unused but available)
 */
function createFavoriteExtendedDropZone(favoriteItem, index) {
    // Create an invisible extended drop zone that covers the gap below each favorite
    const extendedZone = document.createElement('div');
    extendedZone.className = 'favorite-extended-drop-zone';
    extendedZone.style.position = 'absolute';
    extendedZone.style.left = '0';
    extendedZone.style.right = '0';
    extendedZone.style.height = '0.5rem';
    extendedZone.style.top = '100%';
    extendedZone.style.zIndex = '10';
    
    // Copy favorite data attributes to the extended zone
    extendedZone.setAttribute('data-favorite-id', favoriteItem.getAttribute('data-favorite-id'));
    extendedZone.setAttribute('data-folder-id', favoriteItem.getAttribute('data-folder-id'));
    
    // Add event listeners for the extended zone
    extendedZone.addEventListener('dragover', handleFavoriteDragOver);
    extendedZone.addEventListener('drop', handleFavoriteDrop);
    
    // Position the favorite item relatively and append the extended zone
    favoriteItem.style.position = 'relative';
    favoriteItem.appendChild(extendedZone);
}

/**
 * Handle favorite drag start
 */
function handleFavoriteDragStart(e) {
    draggedFavorite = this;
    const favoriteItem = this.closest('.favorite-item');
    if (favoriteItem) {
        favoriteItem.classList.add('dragging');
        // Disable drop events on the dragged item to prevent conflicts
        favoriteItem.style.pointerEvents = 'none';
    }
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.outerHTML);
}

/**
 * Handle favorite drag end
 */
function handleFavoriteDragEnd(e) {
    const favoriteItem = this.closest('.favorite-item');
    if (favoriteItem) {
        favoriteItem.classList.remove('dragging');
        // Re-enable pointer events
        favoriteItem.style.pointerEvents = '';
    }
    favoriteItem.draggable = false;
    favoriteItem.style.cursor = '';
    draggedFavorite = null;
}

/**
 * Handle favorite drag over
 */
function handleFavoriteDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    return false;
}

/**
 * Handle favorite drop
 */
function handleFavoriteDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    // Don't allow dropping on self
    if (this === draggedFavorite?.closest('.favorite-item')) {
        return false;
    }
    
    if (draggedFavorite !== null) {
        const draggedFavoriteId = draggedFavorite.getAttribute('data-favorite-id');
        const draggedFolderId = draggedFavorite.getAttribute('data-folder-id');
        const targetFavoriteId = this.getAttribute('data-favorite-id');
        const targetFolderId = this.getAttribute('data-folder-id');
        
        // Validate IDs before making API call
        if (!draggedFavoriteId || !targetFavoriteId) {
            return false;
        }
        
        if (draggedFolderId === targetFolderId) {
            // Same folder - place below the target favorite
            insertFavoriteBelowFavorite(draggedFavoriteId, targetFavoriteId);
        } else {
            // Cross-folder drop - move to new folder and place below target
            moveFavoriteToNewFolder(draggedFavoriteId, targetFavoriteId, targetFolderId);
        }
    }
    
    return false;
}