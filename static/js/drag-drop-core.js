/**
 * Core drag-and-drop functionality
 * Handles initialization and shared utilities
 */

// Global drag state
let draggedFolder = null;
let draggedFavorite = null;

/**
 * Initialize all drag-and-drop functionality
 */
function initializeDragDrop() {
    const dragHandles = document.querySelectorAll('.drag-handle');
    const folders = document.querySelectorAll('.folder');
    const dropZones = document.querySelectorAll('.drop-zone');

    // Set up folders as drop targets only (not draggable)
    folders.forEach((folder, index) => {
        folder.draggable = false; // Never draggable

        // Create extended drop zone for each folder
        createExtendedDropZone(folder, index);

        // Add folder event listeners (drop only, not drag)
        folder.addEventListener('dragover', handleFolderDragOver);
        folder.addEventListener('dragleave', handleFolderDragLeave);
        folder.addEventListener('drop', handleFolderDrop);

        // Set up card title as drop zone for favorites
        const cardTitle = folder.querySelector('.card-title');
        if (cardTitle) {
            cardTitle.addEventListener('dragover', handleCardTitleDragOver);
            cardTitle.addEventListener('drop', handleCardTitleDrop);
        }
    });

    // Continue with the rest of initialization
    continueInitialization(dragHandles, dropZones);

    // Initialize favorite link drag-and-drop
    initializeFavoriteDragDrop();
}

/**
 * Continue initialization after folder setup
 */
function continueInitialization(dragHandles, dropZones) {
    // Set up drag handles with different behavior based on type
    dragHandles.forEach((handle, index) => {
        const isNavigationLink = handle.href && !handle.href.includes('javascript:void(0)');

        if (isNavigationLink) {
            // Folder title link - needs click/drag detection
            let dragTimeout;
            let isDragging = false;

            // Mouse down starts potential drag
            handle.addEventListener('mousedown', function(e) {
                dragTimeout = setTimeout(() => {
                    // After delay, enable dragging
                    handle.draggable = true;
                    isDragging = true;
                    handle.style.cursor = 'grabbing';
                }, 150); // 150ms delay before drag starts
            });

            // Mouse up cancels drag or allows navigation
            handle.addEventListener('mouseup', function(e) {
                clearTimeout(dragTimeout);
                if (!isDragging) {
                    // Short click - allow navigation
                    window.location.href = handle.href;
                } else {
                    // Was dragging - clean up
                    handle.draggable = false;
                    isDragging = false;
                    handle.style.cursor = 'grab';
                }
            });

            // Prevent default link behavior during drag
            handle.addEventListener('click', function(e) {
                if (isDragging) {
                    e.preventDefault();
                    return false;
                }
            });

            // Add drag event listeners
            handle.addEventListener('dragstart', handleDragHandleDragStart);
            handle.addEventListener('dragend', function(e) {
                handleDragHandleDragEnd.call(this, e);
                // Clean up drag state
                handle.draggable = false;
                isDragging = false;
                handle.style.cursor = 'grab';
            });
        } else {
            // Folder icon - always draggable, no navigation
            handle.draggable = true;

            // Add drag event listeners
            handle.addEventListener('dragstart', handleDragHandleDragStart);
            handle.addEventListener('dragend', handleDragHandleDragEnd);
        }
    });

    // Calculate optimal drop zone height
    const viewportHeight = window.innerHeight;
    const favoritesSection = document.querySelector('.row.align-items-start');
    const favoritesTop = favoritesSection ? favoritesSection.getBoundingClientRect().top : 200;
    const optimalHeight = Math.max(600, viewportHeight - favoritesTop - 40); // 40px bottom padding

    // Add drop zone event listeners
    dropZones.forEach((zone, index) => {
        // Set dynamic height based on available space
        zone.style.minHeight = optimalHeight + 'px';

        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('dragenter', handleDragEnter);
        zone.addEventListener('dragleave', handleDragLeave);
        zone.addEventListener('drop', handleDrop);
    });
}

/**
 * Create extended drop zones to improve UX
 */
function createExtendedDropZone(folder, index) {
    // Create an invisible extended drop zone that covers the gap below each folder
    const extendedZone = document.createElement('div');
    extendedZone.className = 'folder-extended-drop-zone';
    extendedZone.style.position = 'absolute';
    extendedZone.style.left = '0';
    extendedZone.style.right = '0';
    extendedZone.style.height = '2rem'; // Cover the full gap below (was margin-bottom: 2rem)
    extendedZone.style.top = '100%';
    extendedZone.style.zIndex = '10';

    // Copy folder data attributes to the extended zone
    extendedZone.setAttribute('data-folder-id', folder.getAttribute('data-folder-id'));
    extendedZone.setAttribute('data-current-column', folder.getAttribute('data-current-column'));

    // Add event listeners for the extended zone
    extendedZone.addEventListener('dragover', handleFolderDragOver);
    extendedZone.addEventListener('drop', handleFolderDrop);

    // Position the folder relatively and append the extended zone
    folder.style.position = 'relative';
    folder.appendChild(extendedZone);
}

/**
 * Handle drag over for card title (favorite drop zone)
 */
function handleCardTitleDragOver(e) {
    // Only handle favorite drops, not folder drops
    if (draggedFavorite !== null && draggedFolder === null) {
        if (e.preventDefault) {
            e.preventDefault();
        }
        e.dataTransfer.dropEffect = 'move';
        return false;
    }
}

/**
 * Handle drop on card title (move favorite to folder)
 */
function handleCardTitleDrop(e) {
    // Only handle favorite drops, not folder drops
    if (draggedFavorite !== null && draggedFolder === null) {
        if (e.stopPropagation) {
            e.stopPropagation();
        }

        const folder = this.closest('.folder');
        if (folder) {
            const draggedFavoriteId = draggedFavorite.getAttribute('data-favorite-id');
            const targetFolderId = folder.getAttribute('data-folder-id');

            // Validate IDs before making API call
            if (draggedFavoriteId && targetFolderId) {
                // Find the last favorite in the target folder
                const lastFavorite = folder.querySelector('.favorite-item:last-child');

                if (lastFavorite) {
                    // If folder has favorites, move below the last one using cross-folder move
                    const lastFavoriteId = lastFavorite.getAttribute('data-favorite-id');
                    moveFavoriteToNewFolder(draggedFavoriteId, lastFavoriteId, targetFolderId);
                } else {
                    // If folder is empty, use a simple update approach
                    moveFavoriteToEmptyFolder(draggedFavoriteId, targetFolderId);
                }
            }
        }

        return false;
    }
}

/**
 * Get CSRF token for AJAX requests
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDragDrop();
});
