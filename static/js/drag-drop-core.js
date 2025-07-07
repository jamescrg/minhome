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
        folder.addEventListener('drop', handleFolderDrop);
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
    // Make only the drag handles draggable
    dragHandles.forEach((handle, index) => {
        handle.draggable = true;
        
        // Add drag handle event listeners
        handle.addEventListener('dragstart', handleDragHandleDragStart);
        handle.addEventListener('dragend', handleDragHandleDragEnd);
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