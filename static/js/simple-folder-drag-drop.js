/**
 * Simple folder drag-and-drop for nesting (content pages)
 * Uses native HTML5 drag and drop with timer-based click detection
 */

let draggedFolderItem = null;
let isDragging = false;
let dragTimeout = null;

/**
 * Initialize folder drag and drop
 */
function initializeSimpleFolderDragDrop() {
    const folderContainer = document.querySelector('.folders');
    if (!folderContainer) return;

    console.log('Initializing simple folder drag and drop');

    // Initialize draggable folders
    initializeDraggableFolders();

    // Initialize expand/collapse functionality
    initializeFolderExpandCollapse();

    // Restore folder states
    restoreFolderStates();
}

/**
 * Initialize draggable folders
 */
function initializeDraggableFolders() {
    const folderItems = document.querySelectorAll('.folder-item');

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

                // Add drop targets to other folders
                addDropTargetsToFolders(item);
            }, 150); // 150ms delay before drag starts
        });

        link.addEventListener('mouseup', function(e) {
            clearTimeout(dragTimeout);
            if (!isDragging) {
                // Short click - allow navigation
                // Default behavior will handle the navigation
            } else {
                // Was dragging - clean up
                cleanupDragState(item, link);
            }
        });

        // Prevent link navigation during drag
        link.addEventListener('click', function(e) {
            if (isDragging) {
                e.preventDefault();
                return false;
            }
        });

        // Add drag event listeners
        item.addEventListener('dragstart', handleDragStart);
        item.addEventListener('dragend', handleDragEnd);
        item.addEventListener('dragover', handleDragOver);
        item.addEventListener('dragenter', handleDragEnter);
        item.addEventListener('dragleave', handleDragLeave);
        item.addEventListener('drop', handleDrop);
    });
}

/**
 * Add drop targets to folders
 */
function addDropTargetsToFolders(draggedItem) {
    const allFolders = document.querySelectorAll('.folder-item');
    allFolders.forEach(folder => {
        if (folder !== draggedItem && folder.getAttribute('data-shared') !== 'true') {
            folder.classList.add('drop-target-available');
        }
    });
}

/**
 * Remove drop targets from all folders
 */
function removeDropTargetsFromFolders() {
    const allFolders = document.querySelectorAll('.folder-item');
    allFolders.forEach(folder => {
        folder.classList.remove('drop-target-available', 'drop-target');
    });
}

/**
 * Clean up drag state
 */
function cleanupDragState(item, link) {
    item.draggable = false;
    isDragging = false;
    draggedFolderItem = null;
    item.classList.remove('dragging');
    link.style.cursor = '';
    removeDropTargetsFromFolders();
}

/**
 * Handle drag start
 */
function handleDragStart(e) {
    console.log('Drag start');
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.outerHTML);
}

/**
 * Handle drag end
 */
function handleDragEnd(e) {
    console.log('Drag end');
    this.classList.remove('dragging');
    removeDropTargetsFromFolders();

    // Reset drag state
    const link = this.querySelector('.folder-link');
    if (link) {
        cleanupDragState(this, link);
    }
}

/**
 * Handle drag over
 */
function handleDragOver(e) {
    if (!draggedFolderItem) return;

    e.preventDefault();

    // Don't allow dropping on self
    if (this === draggedFolderItem) {
        return false;
    }

    // Validate drop
    const draggedId = draggedFolderItem.getAttribute('data-folder-id');
    const targetId = this.getAttribute('data-folder-id');

    // Don't allow dropping on descendants
    if (isDescendantFolder(draggedId, targetId)) {
        return false;
    }

    // Check depth limit
    const targetDepth = getFolderDepth(this);
    if (targetDepth >= 2) {
        return false;
    }

    // Add visual feedback
    this.classList.add('drop-target');
    e.dataTransfer.dropEffect = 'move';
    return false;
}

/**
 * Handle drag enter
 */
function handleDragEnter(e) {
    e.preventDefault();
}

/**
 * Handle drag leave
 */
function handleDragLeave(e) {
    // Only remove if we're actually leaving this element
    if (!this.contains(e.relatedTarget)) {
        this.classList.remove('drop-target');
    }
}

/**
 * Handle drop
 */
function handleDrop(e) {
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
    if (isDescendantFolder(draggedId, targetId)) {
        return false;
    }

    // Check depth limit
    const targetDepth = getFolderDepth(this);
    if (targetDepth >= 2) {
        showCustomAlert('Cannot nest folders more than 3 levels deep');
        this.classList.remove('drop-target');
        return false;
    }

    this.classList.remove('drop-target');

    console.log(`Moving folder ${draggedId} to parent ${targetId}`);

    // Move the folder to be a child of the target
    moveFolderToParent(draggedId, targetId);

    return false;
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
            'X-CSRFToken': getCookie('csrftoken')
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
 * Helper functions
 */
function getCurrentPage() {
    const path = window.location.pathname;
    const segments = path.split('/').filter(segment => segment.length > 0);
    const pageTypes = ['favorites', 'contacts', 'notes', 'tasks'];

    for (const pageType of pageTypes) {
        if (segments.includes(pageType)) {
            return pageType;
        }
    }

    return 'favorites'; // Default fallback
}

function getFolderDepth(folderElement) {
    const level = folderElement.getAttribute('data-level');
    return level ? parseInt(level, 10) : 0;
}

function isDescendantFolder(draggedId, targetId) {
    if (draggedId === targetId) {
        return false;
    }

    const draggedFolder = document.getElementById(`folder-${draggedId}`);
    if (!draggedFolder) return false;

    const childrenContainer = document.querySelector(`.folder-children-container[data-parent-id="${draggedId}"]`);
    if (!childrenContainer) return false;

    const targetFolder = childrenContainer.querySelector(`#folder-${targetId}`);
    return targetFolder !== null;
}

function showCustomAlert(message) {
    const messageElement = document.getElementById('customAlertMessage');
    const modal = document.getElementById('customAlertModal');

    if (messageElement && modal) {
        messageElement.textContent = message;
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    } else {
        alert(message);
    }
}

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

/**
 * Initialize folder expand/collapse functionality
 */
function initializeFolderExpandCollapse() {
    const expandToggles = document.querySelectorAll('.folder-expand-toggle');
    console.log('Found', expandToggles.length, 'expandable folders');

    expandToggles.forEach(toggle => {
        // Remove existing listeners
        toggle.removeEventListener('click', handleFolderToggle);
        // Add new listener
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
        icon.classList.remove('bi-chevron-down');
        icon.classList.add('bi-chevron-right');

        // Save collapsed state
        saveFolderState(folderId, false);
    } else {
        // Expand
        folderItem.classList.add('expanded');
        childrenContainer.classList.remove('collapsed');
        icon.classList.remove('bi-chevron-right');
        icon.classList.add('bi-chevron-down');

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
            icon.classList.remove('bi-chevron-right');
            icon.classList.add('bi-chevron-down');
        } else {
            folderItem.classList.remove('expanded');
            childrenContainer.classList.add('collapsed');
            icon.classList.remove('bi-chevron-down');
            icon.classList.add('bi-chevron-right');
        }
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.folders')) {
        initializeSimpleFolderDragDrop();
    }
});

// Re-initialize after HTMX updates
document.addEventListener('htmx:afterSwap', function(e) {
    if (e.target.id === 'folder-list' || e.target.closest('#folder-list')) {
        setTimeout(() => {
            initializeSimpleFolderDragDrop();
        }, 100);
    }
});

// Global failsafe to clean up drop targets
window.addEventListener('dragend', function() {
    removeDropTargetsFromFolders();
});
