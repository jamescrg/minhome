/**
 * Folder hierarchy drag-and-drop functionality
 * Handles folder dragging for reorganizing folder hierarchy on content pages
 */

let draggedFolderItem = null;

/**
 * Initialize folder hierarchy drag and drop
 */
function initializeFolderHierarchyDragDrop() {
    const folderItems = document.querySelectorAll('.folder-item');
    console.log('Found', folderItems.length, 'folder items for drag-drop');
    
    folderItems.forEach(item => {
        console.log('Setting up drag-drop for folder:', item.getAttribute('data-folder-name'));
        item.addEventListener('dragstart', handleFolderItemDragStart);
        item.addEventListener('dragend', handleFolderItemDragEnd);
        item.addEventListener('dragover', handleFolderItemDragOver);
        item.addEventListener('dragleave', handleFolderItemDragLeave);
        item.addEventListener('drop', handleFolderItemDrop);
    });
}

/**
 * Handle drag start for folder items
 */
function handleFolderItemDragStart(e) {
    console.log('Drag start for folder:', this.getAttribute('data-folder-name'));
    draggedFolderItem = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.outerHTML);
}

/**
 * Handle drag end for folder items
 */
function handleFolderItemDragEnd(e) {
    this.classList.remove('dragging');
    draggedFolderItem = null;
    
    // Remove all drop indicators
    const allItems = document.querySelectorAll('.folder-item');
    allItems.forEach(item => {
        item.classList.remove('drag-over', 'drop-target');
    });
}

/**
 * Handle drag over for folder items
 */
function handleFolderItemDragOver(e) {
    if (!draggedFolderItem) return;
    
    e.preventDefault();
    
    // Don't allow dropping on self
    if (this === draggedFolderItem) {
        return false;
    }
    
    // Don't allow dropping on descendants
    const draggedId = draggedFolderItem.getAttribute('data-folder-id');
    const targetId = this.getAttribute('data-folder-id');
    
    if (isDescendant(draggedId, targetId)) {
        return false;
    }
    
    this.classList.add('drop-target');
    e.dataTransfer.dropEffect = 'move';
    return false;
}

/**
 * Handle drag leave for folder items
 */
function handleFolderItemDragLeave(e) {
    this.classList.remove('drop-target');
}

/**
 * Handle drop on folder items
 */
function handleFolderItemDrop(e) {
    if (!draggedFolderItem) return false;
    
    e.stopPropagation();
    e.preventDefault();
    
    // Don't allow dropping on self
    if (this === draggedFolderItem) {
        return false;
    }
    
    const draggedId = draggedFolderItem.getAttribute('data-folder-id');
    const targetId = this.getAttribute('data-folder-id');
    
    // Don't allow dropping on descendants
    if (isDescendant(draggedId, targetId)) {
        return false;
    }
    
    this.classList.remove('drop-target');
    
    // Move the folder to be a child of the target
    moveFolderToParent(draggedId, targetId);
    
    return false;
}

/**
 * Check if targetId is a descendant of draggedId
 */
function isDescendant(draggedId, targetId) {
    // This is a simplified check - in a real implementation you'd want to
    // traverse the actual folder hierarchy or maintain a lookup
    return false; // For now, allow all moves
}

/**
 * Move folder to new parent via AJAX
 */
function moveFolderToParent(folderId, newParentId) {
    const page = getCurrentPage();
    console.log('Moving folder', folderId, 'to parent', newParentId, 'on page', page);
    
    fetch(`/folders/move/${folderId}/${page}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            new_parent_id: newParentId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Folder moved successfully');
            // Reload the page to show the new folder structure
            location.reload();
        } else {
            console.error('Error moving folder:', data.error);
            alert('Error moving folder: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error moving folder');
    });
}

/**
 * Get current page from URL or context
 */
function getCurrentPage() {
    // Extract page from URL path
    const path = window.location.pathname;
    const segments = path.split('/').filter(segment => segment.length > 0);
    
    // Common page types
    const pageTypes = ['favorites', 'contacts', 'notes', 'tasks'];
    
    for (const pageType of pageTypes) {
        if (segments.includes(pageType)) {
            return pageType;
        }
    }
    
    return 'favorites'; // Default fallback
}

/**
 * Get CSRF token for AJAX requests
 */
function getCsrfToken() {
    // Try multiple ways to get the CSRF token
    let token = document.querySelector('[name=csrfmiddlewaretoken]');
    if (token) return token.value;
    
    // Try meta tag
    token = document.querySelector('meta[name="csrf-token"]');
    if (token) return token.getAttribute('content');
    
    // Try from cookies
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') return value;
    }
    
    return '';
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeFolderHierarchyDragDrop();
});