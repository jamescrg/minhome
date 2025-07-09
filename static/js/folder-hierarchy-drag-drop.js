/**
 * Folder hierarchy drag-and-drop functionality
 * Handles folder dragging for reorganizing folder hierarchy on content pages
 * Uses timer-based click vs drag detection like favorites on home page
 */

let draggedFolderItem = null;
let isDragging = false;
let dragTimeout = null;

/**
 * Initialize folder hierarchy drag and drop
 */
function initializeFolderHierarchyDragDrop() {
    const folderContainer = document.querySelector('.folders');
    if (!folderContainer) return;

    // Get all folder items and links
    const folderItems = document.querySelectorAll('.folder-item');
    const folderLinks = document.querySelectorAll('.folder-link');

    folderItems.forEach(item => {
        const link = item.querySelector('.folder-link');
        if (!link) return;

        // Prevent dragging shared folders
        const isShared = item.getAttribute('data-shared') === 'true';
        if (isShared) return;

        // Timer-based drag detection on the link
        link.addEventListener('mousedown', function(e) {
            dragTimeout = setTimeout(() => {
                // After delay, enable dragging on the item
                item.draggable = true;
                isDragging = true;
                draggedFolderItem = item;
                item.classList.add('dragging');
                link.style.cursor = 'grabbing';
            }, 150); // 150ms delay before drag starts
        });

        link.addEventListener('mouseup', function(e) {
            clearTimeout(dragTimeout);
            if (!isDragging) {
                // Short click - allow navigation
                // Default behavior will handle the navigation
            } else {
                // Was dragging - clean up
                item.draggable = false;
                isDragging = false;
                draggedFolderItem = null;
                item.classList.remove('dragging');
                link.style.cursor = '';
            }
        });

        // Prevent link navigation during drag
        link.addEventListener('click', function(e) {
            if (isDragging) {
                e.preventDefault();
                return false;
            }
        });
    });

    // Add drop zone event listeners
    folderContainer.addEventListener('dragover', handleDragOver);
    folderContainer.addEventListener('dragleave', handleDragLeave);
    folderContainer.addEventListener('drop', handleDrop);
    folderContainer.addEventListener('dragend', handleDragEnd);
    
    console.log('Folder drag and drop initialized');
}

function handleDragEnd(e) {
    const folderItem = e.target.closest('.folder-item');
    if (folderItem) {
        handleFolderItemDragEnd.call(folderItem, e);
    }
}

function handleDragOver(e) {
    const folderItem = e.target.closest('.folder-item');
    const titleDropZone = e.target.closest('.folders-title-drop-zone');
    
    if (folderItem && draggedFolderItem) {
        handleFolderItemDragOver.call(folderItem, e);
    } else if (titleDropZone && draggedFolderItem) {
        handleTitleDropZoneDragOver.call(titleDropZone, e);
    }
}

function handleDragLeave(e) {
    const folderItem = e.target.closest('.folder-item');
    const titleDropZone = e.target.closest('.folders-title-drop-zone');
    
    if (folderItem) {
        handleFolderItemDragLeave.call(folderItem, e);
    } else if (titleDropZone) {
        handleTitleDropZoneDragLeave.call(titleDropZone, e);
    }
}

function handleDrop(e) {
    const folderItem = e.target.closest('.folder-item');
    const titleDropZone = e.target.closest('.folders-title-drop-zone');
    
    if (folderItem && draggedFolderItem) {
        handleFolderItemDrop.call(folderItem, e);
    } else if (titleDropZone && draggedFolderItem) {
        handleTitleDropZoneDrop.call(titleDropZone, e);
    }
}


/**
 * Handle drag end for folder items
 */
function handleFolderItemDragEnd(e) {
    if (draggedFolderItem) {
        draggedFolderItem.classList.remove('dragging');
        draggedFolderItem.draggable = false;
        
        // Reset link cursor
        const link = draggedFolderItem.querySelector('.folder-link');
        if (link) {
            link.style.cursor = '';
        }
    }

    // Remove all drop indicators
    const allItems = document.querySelectorAll('.folder-item');
    allItems.forEach(item => {
        item.classList.remove('drag-over', 'drop-target');
    });

    // Remove drop indicator from title drop zone
    const titleDropZone = document.querySelector('.folders-title-drop-zone');
    if (titleDropZone) {
        titleDropZone.classList.remove('drop-target');
    }

    // Reset state
    draggedFolderItem = null;
    isDragging = false;
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

    // Don't allow moving shared folders
    const isShared = draggedFolderItem.getAttribute('data-shared') === 'true';
    if (isShared) {
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

    // Don't allow moving shared folders
    const isShared = draggedFolderItem.getAttribute('data-shared') === 'true';
    if (isShared) {
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
 * Handle drag over for title drop zone
 */
function handleTitleDropZoneDragOver(e) {
    if (!draggedFolderItem) return;

    e.preventDefault();

    // Don't allow moving shared folders
    const isShared = draggedFolderItem.getAttribute('data-shared') === 'true';
    if (isShared) {
        return false;
    }

    this.classList.add('drop-target');
    e.dataTransfer.dropEffect = 'move';
    return false;
}

/**
 * Handle drag leave for title drop zone
 */
function handleTitleDropZoneDragLeave(e) {
    this.classList.remove('drop-target');
}

/**
 * Handle drop on title drop zone (move to root level)
 */
function handleTitleDropZoneDrop(e) {
    if (!draggedFolderItem) return false;

    e.stopPropagation();
    e.preventDefault();

    // Don't allow moving shared folders
    const isShared = draggedFolderItem.getAttribute('data-shared') === 'true';
    if (isShared) {
        return false;
    }

    const draggedId = draggedFolderItem.getAttribute('data-folder-id');

    this.classList.remove('drop-target');

    // Move the folder to root level (no parent)
    moveFolderToParent(draggedId, null);

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

// Re-initialize after HTMX updates
document.addEventListener('htmx:afterSwap', function(e) {
    // Only reinitialize if the target contains folder content
    if (e.target.id === 'folder-list' || e.target.closest('#folder-list')) {
        initializeFolderHierarchyDragDrop();
        initializeFolderExpandCollapse();
        restoreFolderStates();
    }
});
