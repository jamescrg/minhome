/**
 * Folder hierarchy drag-and-drop functionality
 * Handles folder dragging for reorganizing folder hierarchy on content pages
 */

let draggedFolderItem = null;

/**
 * Initialize folder hierarchy drag and drop
 */
function initializeFolderHierarchyDragDrop() {
    // Use event delegation for better performance and to handle dynamic content
    const folderList = document.querySelector('.folders');
    if (!folderList) return;
    
    // Remove any existing listeners to avoid duplicates
    folderList.removeEventListener('dragstart', handleDragStart);
    folderList.removeEventListener('dragend', handleDragEnd);
    folderList.removeEventListener('dragover', handleDragOver);
    folderList.removeEventListener('dragleave', handleDragLeave);
    folderList.removeEventListener('drop', handleDrop);
    
    // Add event listeners using delegation
    folderList.addEventListener('dragstart', handleDragStart);
    folderList.addEventListener('dragend', handleDragEnd);
    folderList.addEventListener('dragover', handleDragOver);
    folderList.addEventListener('dragleave', handleDragLeave);
    folderList.addEventListener('drop', handleDrop);
}

function handleDragStart(e) {
    if (e.target.classList.contains('folder-item')) {
        handleFolderItemDragStart.call(e.target, e);
    }
}

function handleDragEnd(e) {
    if (e.target.classList.contains('folder-item')) {
        handleFolderItemDragEnd.call(e.target, e);
    }
}

function handleDragOver(e) {
    const folderItem = e.target.closest('.folder-item');
    if (folderItem && draggedFolderItem) {
        handleFolderItemDragOver.call(folderItem, e);
    }
}

function handleDragLeave(e) {
    const folderItem = e.target.closest('.folder-item');
    if (folderItem) {
        handleFolderItemDragLeave.call(folderItem, e);
    }
}

function handleDrop(e) {
    const folderItem = e.target.closest('.folder-item');
    if (folderItem && draggedFolderItem) {
        handleFolderItemDrop.call(folderItem, e);
    }
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
    // If they're the same, target is not a descendant
    if (draggedId === targetId) {
        return false;
    }
    
    // Get the dragged folder element
    const draggedFolder = document.getElementById(`folder-${draggedId}`);
    if (!draggedFolder) return false;
    
    // Check if the target folder is within the dragged folder's children container
    const childrenContainer = document.querySelector(`.folder-children-container[data-parent-id="${draggedId}"]`);
    if (!childrenContainer) return false;
    
    // Look for the target folder within the descendants
    const targetFolder = childrenContainer.querySelector(`#folder-${targetId}`);
    
    // If we found the target folder within the dragged folder's descendants, it's a descendant
    return targetFolder !== null;
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

/**
 * Initialize folder expand/collapse functionality
 */
function initializeFolderExpandCollapse() {
    const expandToggles = document.querySelectorAll('.folder-expand-toggle');
    console.log('Found', expandToggles.length, 'expandable folders');
    
    expandToggles.forEach(toggle => {
        toggle.addEventListener('click', handleFolderToggle);
    });
}

/**
 * Handle folder expand/collapse toggle
 */
function handleFolderToggle(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const folderId = this.getAttribute('data-folder-id');
    const folderItem = document.getElementById(`folder-${folderId}`);
    const childrenContainer = document.querySelector(`.folder-children-container[data-parent-id="${folderId}"]`);
    const icon = this.querySelector('i');
    
    if (!folderItem || !childrenContainer) return;
    
    const isExpanded = folderItem.classList.contains('expanded');
    
    if (isExpanded) {
        // Collapse
        folderItem.classList.remove('expanded');
        childrenContainer.classList.add('collapsed');
        icon.classList.remove('bi-caret-down-fill');
        icon.classList.add('bi-caret-right-fill');
        
        // Save collapsed state
        saveFolderState(folderId, false);
    } else {
        // Expand
        folderItem.classList.add('expanded');
        childrenContainer.classList.remove('collapsed');
        icon.classList.remove('bi-caret-right-fill');
        icon.classList.add('bi-caret-down-fill');
        
        // Save expanded state
        saveFolderState(folderId, true);
    }
}

/**
 * Save folder expanded/collapsed state to localStorage
 */
function saveFolderState(folderId, isExpanded) {
    const page = getCurrentPage();
    const storageKey = `folder-state-${page}`;
    let folderStates = JSON.parse(localStorage.getItem(storageKey) || '{}');
    
    folderStates[folderId] = isExpanded;
    localStorage.setItem(storageKey, JSON.stringify(folderStates));
}

/**
 * Restore folder states from localStorage
 */
function restoreFolderStates() {
    const page = getCurrentPage();
    const storageKey = `folder-state-${page}`;
    const folderStates = JSON.parse(localStorage.getItem(storageKey) || '{}');
    
    Object.entries(folderStates).forEach(([folderId, isExpanded]) => {
        const folderItem = document.getElementById(`folder-${folderId}`);
        const childrenContainer = document.querySelector(`.folder-children-container[data-parent-id="${folderId}"]`);
        const toggle = document.querySelector(`.folder-expand-toggle[data-folder-id="${folderId}"]`);
        
        if (!folderItem || !childrenContainer || !toggle) return;
        
        const icon = toggle.querySelector('i');
        
        if (isExpanded) {
            folderItem.classList.add('expanded');
            childrenContainer.classList.remove('collapsed');
            icon.classList.remove('bi-caret-right-fill');
            icon.classList.add('bi-caret-down-fill');
        } else {
            folderItem.classList.remove('expanded');
            childrenContainer.classList.add('collapsed');
            icon.classList.remove('bi-caret-down-fill');
            icon.classList.add('bi-caret-right-fill');
        }
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeFolderHierarchyDragDrop();
    initializeFolderExpandCollapse();
    restoreFolderStates();
});