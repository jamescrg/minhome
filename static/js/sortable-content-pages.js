/**
 * SortableJS-based drag-and-drop functionality for content pages (Favorites, Tasks, Contacts, Notes)
 * Handles both folder hierarchy reorganization and item-to-folder movement
 */

let folderHierarchySortable = null;
let itemSortables = [];

/**
 * Initialize SortableJS for content pages
 */
function initializeSortableContentPages() {
    console.log('Initializing SortableJS for content pages');

    // Clean up existing sortables
    cleanupContentSortables();

    // Initialize folder hierarchy sorting
    initializeFolderHierarchySortable();

    // Initialize item-to-folder dragging
    initializeItemToFolderSortables();
}

/**
 * Clean up existing sortable instances
 */
function cleanupContentSortables() {
    if (folderHierarchySortable && folderHierarchySortable.destroy) {
        folderHierarchySortable.destroy();
        folderHierarchySortable = null;
    }

    itemSortables.forEach(sortable => {
        if (sortable && sortable.destroy) {
            sortable.destroy();
        }
    });
    itemSortables = [];
}

/**
 * Initialize folder hierarchy sorting (nesting only, no reordering)
 */
function initializeFolderHierarchySortable() {
    const foldersContainer = document.querySelector('.folders');
    if (!foldersContainer) return;

    // Create a single sortable for the entire folders container
    folderHierarchySortable = new Sortable(foldersContainer, {
        group: 'folder-hierarchy',
        animation: 200,
        handle: '.folder-link',
        delay: 200,
        delayOnTouchStart: true,
        ghostClass: 'sortable-ghost',
        chosenClass: 'sortable-chosen',
        dragClass: 'sortable-drag',

        // Filter out elements that shouldn't be draggable
        filter: function(evt, item) {
            // Don't allow dragging shared folders
            if (item.getAttribute('data-shared') === 'true') {
                return true; // Filter out (don't allow dragging)
            }
            // Don't allow dragging children containers
            if (item.classList.contains('folder-children-container')) {
                return true; // Filter out
            }
            // Only allow dragging folder-item elements
            if (!item.classList.contains('folder-item')) {
                return true; // Filter out
            }
            return false; // Allow dragging
        },

        onStart: function(evt) {
            console.log('Folder drag started');
            evt.item.classList.add('dragging');

            // Add drop target indicators to all other folders
            const allFolders = document.querySelectorAll('.folder-item');
            allFolders.forEach(folder => {
                if (folder !== evt.item && folder.getAttribute('data-shared') !== 'true') {
                    folder.classList.add('drop-target-available');
                }
            });
        },

        onEnd: function(evt) {
            console.log('Folder drag ended');
            evt.item.classList.remove('dragging');

            // Remove all drop target indicators
            const allFolders = document.querySelectorAll('.folder-item');
            allFolders.forEach(folder => {
                folder.classList.remove('drop-target-available', 'drop-target');
            });

            // Handle the drop if position changed
            if (evt.oldIndex !== evt.newIndex || evt.from !== evt.to) {
                handleFolderDrop(evt);
            }
        },

        onMove: function(evt) {
            const draggedItem = evt.dragged;
            const relatedItem = evt.related;

            // Only allow dropping on folder items
            if (!relatedItem || !relatedItem.classList.contains('folder-item')) {
                return false;
            }

            const draggedId = draggedItem.getAttribute('data-folder-id');
            const targetId = relatedItem.getAttribute('data-folder-id');

            // Don't allow dropping on self
            if (draggedId === targetId) return false;

            // Don't allow dropping on descendants
            if (isDescendantFolder(draggedId, targetId)) return false;

            // Check depth limit
            const targetDepth = getFolderDepth(relatedItem);
            if (targetDepth >= 2) return false;

            // Add visual feedback
            relatedItem.classList.add('drop-target');

            // Remove feedback from other folders
            const allFolders = document.querySelectorAll('.folder-item');
            allFolders.forEach(folder => {
                if (folder !== relatedItem) {
                    folder.classList.remove('drop-target');
                }
            });

            return true;
        }
    });

    // Initialize expand/collapse functionality
    initializeFolderExpandCollapse();
}

/**
 * Handle folder drop operation
 */
function handleFolderDrop(evt) {
    const draggedFolderId = evt.item.getAttribute('data-folder-id');
    const targetFolder = evt.item.nextElementSibling || evt.item.previousElementSibling;

    // If dropped next to another folder, nest under it
    if (targetFolder && targetFolder.classList.contains('folder-item')) {
        const targetFolderId = targetFolder.getAttribute('data-folder-id');
        console.log(`Nesting folder ${draggedFolderId} under ${targetFolderId}`);
        moveFolderToParent(draggedFolderId, targetFolderId);
    } else {
        // If dropped at root level, move to root
        console.log(`Moving folder ${draggedFolderId} to root level`);
        moveFolderToParent(draggedFolderId, null);
    }
}

/**
 * Initialize item-to-folder dragging
 */
function initializeItemToFolderSortables() {
    const itemContainers = document.querySelectorAll('.list-group');

    itemContainers.forEach(container => {
        const sortable = new Sortable(container, {
            group: {
                name: 'items-to-folders',
                pull: 'clone',
                put: false // Don't allow items to be moved within the list
            },
            animation: 200,
            delay: 200, // Delay to distinguish from clicks
            delayOnTouchStart: true,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',
            sort: false, // Don't allow sorting within the container

            onStart: function(evt) {
                console.log('Item drag started');
                evt.item.classList.add('dragging');

                // Add drop zones to folders
                const folderItems = document.querySelectorAll('.folder-item');
                folderItems.forEach(folder => {
                    folder.classList.add('drop-zone-active');
                });
            },

            onEnd: function(evt) {
                console.log('Item drag ended');
                evt.item.classList.remove('dragging');

                // Remove drop zones from folders
                const folderItems = document.querySelectorAll('.folder-item');
                folderItems.forEach(folder => {
                    folder.classList.remove('drop-zone-active', 'drop-target');
                });
            }
        });

        itemSortables.push(sortable);
    });

    // Make folders accept item drops
    initializeFolderDropZones();
}

/**
 * Initialize folder drop zones for items
 */
function initializeFolderDropZones() {
    const folderItems = document.querySelectorAll('.folder-item');

    folderItems.forEach(folder => {
        const dropSortable = new Sortable(folder, {
            group: {
                name: 'items-to-folders',
                pull: false,
                put: true
            },
            animation: 200,
            ghostClass: 'sortable-ghost',

            onAdd: function(evt) {
                const droppedItem = evt.item;
                const targetFolderId = folder.getAttribute('data-folder-id');

                // Determine item type and ID
                const itemType = getItemTypeFromElement(droppedItem);
                const itemId = getItemIdFromElement(droppedItem, itemType);

                console.log(`Moving ${itemType} ${itemId} to folder ${targetFolderId}`);

                // Move item to folder via API
                moveItemToFolder(itemId, targetFolderId, itemType);

                // Remove the cloned element
                droppedItem.remove();
            }
        });

        itemSortables.push(dropSortable);
    });
}

/**
 * Move folder to new parent via API
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
            location.reload();
        } else {
            console.error('Error moving folder:', data.error);
            alert('Error moving folder: ' + data.error);
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error moving folder');
        location.reload();
    });
}

/**
 * Move item to folder via API
 */
function moveItemToFolder(itemId, folderId, itemType) {
    const url = `/${itemType}s/move-to-folder/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            item_id: itemId,
            folder_id: folderId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(`${itemType} moved successfully`);
            location.reload();
        } else {
            console.error(`Error moving ${itemType}:`, data.error);
            alert(`Error moving ${itemType}: ` + data.error);
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Error moving ${itemType}`);
        location.reload();
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

function getItemTypeFromElement(element) {
    if (element.querySelector('.favorite-left')) return 'favorite';
    if (element.querySelector('.task-title')) return 'task';
    if (element.querySelector('.contact-item')) return 'contact';
    if (element.querySelector('.note-item')) return 'note';
    return 'favorite'; // Default fallback
}

function getItemIdFromElement(element, itemType) {
    const link = element.querySelector(`${itemType === 'favorite' ? '.favorite-left' : `.${itemType}-item`} a, .${itemType}-title a`);
    if (link) {
        const href = link.getAttribute('href');
        const match = href.match(/\/(\d+)\//);
        return match ? match[1] : null;
    }
    return null;
}

function isDescendantFolder(draggedId, targetId) {
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

function getFolderDepth(folderElement) {
    const level = folderElement.getAttribute('data-level');
    return level ? parseInt(level, 10) : 0;
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
    // Only initialize on content pages that have folders
    if (document.querySelector('.folders')) {
        initializeSortableContentPages();
        restoreFolderStates();
    }
});

// Re-initialize after HTMX updates
document.addEventListener('htmx:afterSwap', function(e) {
    if (e.target.id === 'folder-list' || e.target.closest('#folder-list')) {
        setTimeout(() => {
            initializeSortableContentPages();
            restoreFolderStates();
        }, 100);
    }
});

// Global failsafe to clean up drop targets
window.addEventListener('dragend', function() {
    const dropTargets = document.querySelectorAll('.drop-target, .drop-target-available');
    dropTargets.forEach(target => {
        target.classList.remove('drop-target', 'drop-target-available');
    });
});
