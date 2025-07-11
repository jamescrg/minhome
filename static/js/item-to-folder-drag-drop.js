/**
 * Item to folder drag-and-drop functionality
 * Handles dragging favorites, tasks, contacts, and notes to folders
 * Uses timer-based click vs drag detection (150ms delay)
 */

let draggedItem = null;
let draggedItemType = null;
let itemDragTimeout = null;
let isItemDragging = false;

/**
 * Initialize item to folder drag and drop
 */
function initializeItemToFolderDragDrop() {
    console.log('Initializing item to folder drag and drop');

    // Initialize draggable items by type
    initializeDraggableItems('.favorite-item', 'favorite');
    initializeDraggableItems('.task-title a', 'task');
    initializeDraggableItems('.contact-item a', 'contact');
    initializeDraggableItems('.note-item a', 'note');

    // Make folders accept drops from items
    initializeFolderDropZones();
}

/**
 * Initialize draggable items with timer-based detection
 */
function initializeDraggableItems(selector, itemType) {
    const items = document.querySelectorAll(selector);
    console.log(`Found ${items.length} ${itemType} items with selector: ${selector}`);

    items.forEach(item => {
        const listItem = itemType === 'favorite' ? item : item.closest('.list-group-item');
        if (!listItem) return;

        // Make items draggable by default
        listItem.draggable = true;
        listItem.setAttribute('draggable', 'true');

        // For favorites, we're already selecting the list item
        const dragTarget = itemType === 'favorite' ? item : item;
        const clickTarget = itemType === 'favorite' ? item.querySelector('.link a') : item;

        // Timer-based drag detection
        dragTarget.addEventListener('mousedown', function(e) {
            // Set drag mode immediately for native drag to work
            isItemDragging = true;
            draggedItem = listItem;
            draggedItemType = itemType;

            itemDragTimeout = setTimeout(() => {
                listItem.classList.add('dragging');
                dragTarget.style.cursor = 'grabbing';
            }, 150);
        });

        let dragStarted = false;

        dragTarget.addEventListener('mouseup', function(e) {
            clearTimeout(itemDragTimeout);

            // Clean up
            const wasDragging = dragStarted;
            dragStarted = false;
            isItemDragging = false;
            listItem.classList.remove('dragging');
            dragTarget.style.cursor = '';
        });

        // Prevent navigation during drag
        if (clickTarget) {
            clickTarget.addEventListener('click', function(e) {
                if (isItemDragging) {
                    e.preventDefault();
                    return false;
                }
            });
        }

        // Drag events
        listItem.addEventListener('dragstart', handleItemDragStart);
        listItem.addEventListener('dragend', handleItemDragEnd);
    });
}

/**
 * Initialize folder drop zones
 */
function initializeFolderDropZones() {
    const folderItems = document.querySelectorAll('.folder-item');
    console.log(`Found ${folderItems.length} folders as drop zones`);

    folderItems.forEach(folder => {
        // Add event listeners for item drops
        folder.addEventListener('dragover', handleItemToFolderDragOver);
        folder.addEventListener('drop', handleItemToFolderDrop);
        folder.addEventListener('dragenter', handleItemToFolderDragEnter);
        folder.addEventListener('dragleave', handleItemToFolderDragLeave);
    });
}

/**
 * Handle item drag start
 */
function handleItemDragStart(e) {
    console.log('Drag start event fired', e);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);

    // Mark the element with data attribute to track drag state
    this.setAttribute('data-is-dragging', 'true');
}

/**
 * Handle item drag end
 */
function handleItemDragEnd(e) {
    this.classList.remove('dragging');
    this.removeAttribute('data-is-dragging');
    isItemDragging = false;

    // Clean up all drop indicators
    const folders = document.querySelectorAll('.folder-item');
    folders.forEach(folder => {
        folder.classList.remove('drop-target', 'drop-target-active');
    });

    draggedItem = null;
    draggedItemType = null;
}

/**
 * Handle drag over folder
 */
function handleItemToFolderDragOver(e) {
    // Only handle item drags, not folder drags
    if (!draggedItem || (typeof draggedFolderItem !== 'undefined' && draggedFolderItem)) {
        console.log('Ignoring dragover - draggedItem:', draggedItem, 'draggedFolderItem:', typeof draggedFolderItem !== 'undefined' ? draggedFolderItem : 'undefined');
        return;
    }

    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    return false;
}

/**
 * Handle drag enter folder
 */
function handleItemToFolderDragEnter(e) {
    // Only handle item drags
    if (!draggedItem || (typeof draggedFolderItem !== 'undefined' && draggedFolderItem)) return;

    this.classList.add('drop-target', 'drop-target-active');
}

/**
 * Handle drag leave folder
 */
function handleItemToFolderDragLeave(e) {
    // Only handle item drags
    if (!draggedItem || (typeof draggedFolderItem !== 'undefined' && draggedFolderItem)) return;

    // Check if we're actually leaving the folder (not just moving to a child element)
    const rect = this.getBoundingClientRect();
    if (e.clientX < rect.left || e.clientX >= rect.right ||
        e.clientY < rect.top || e.clientY >= rect.bottom) {
        this.classList.remove('drop-target', 'drop-target-active');
    }
}

/**
 * Handle drop on folder
 */
function handleItemToFolderDrop(e) {
    console.log('Drop event triggered', draggedItem, draggedItemType);

    // Only handle item drags
    if (!draggedItem || (typeof draggedFolderItem !== 'undefined' && draggedFolderItem)) return;

    e.preventDefault();
    e.stopPropagation();

    const targetFolderId = this.getAttribute('data-folder-id');
    console.log('Target folder ID:', targetFolderId);
    let itemId;

    switch(draggedItemType) {
        case 'favorite':
            itemId = draggedItem.getAttribute('data-favorite-id');
            if (itemId && targetFolderId) {
                moveItemToFolder('favorite', itemId, targetFolderId);
            }
            break;
        case 'task':
            itemId = draggedItem.getAttribute('data-task-id');
            console.log('Task ID:', itemId, 'Target folder:', targetFolderId);
            if (itemId && targetFolderId) {
                moveItemToFolder('task', itemId, targetFolderId);
            }
            break;
        case 'contact':
            itemId = draggedItem.getAttribute('data-contact-id');
            if (itemId && targetFolderId) {
                moveItemToFolder('contact', itemId, targetFolderId);
            }
            break;
        case 'note':
            itemId = draggedItem.getAttribute('data-note-id');
            if (itemId && targetFolderId) {
                moveItemToFolder('note', itemId, targetFolderId);
            }
            break;
    }

    return false;
}

/**
 * Move item to folder via API
 */
function moveItemToFolder(itemType, itemId, folderId) {
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
            // Reload the page to show updated organization
            window.location.reload();
        } else {
            console.error('Failed to move item:', data.message);
        }
    })
    .catch(error => {
        console.error('Error moving item:', error);
    });
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

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize on pages with folders and items
    if (document.querySelector('.folders') &&
        (document.querySelector('.favorites') ||
         document.querySelector('.tasks') ||
         document.querySelector('.contacts') ||
         document.querySelector('.notes'))) {
        initializeItemToFolderDragDrop();
    }
});
