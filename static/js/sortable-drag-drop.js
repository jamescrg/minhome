/**
 * SortableJS-based drag-and-drop functionality for home page
 * Handles both folder and favorite dragging with better UX
 */

let folderSortables = [];
let favoriteSortables = [];

/**
 * Initialize SortableJS for home page drag and drop
 */
function initializeSortableDragDrop() {
    console.log('Initializing SortableJS drag and drop');

    // Clean up existing sortables
    cleanupSortables();

    // Initialize folder sorting
    initializeFolderSortables();

    // Initialize favorite sorting
    initializeFavoriteSortables();
}

/**
 * Clean up existing sortable instances
 */
function cleanupSortables() {
    folderSortables.forEach(sortable => {
        if (sortable && sortable.destroy) {
            sortable.destroy();
        }
    });
    folderSortables = [];

    favoriteSortables.forEach(sortable => {
        if (sortable && sortable.destroy) {
            sortable.destroy();
        }
    });
    favoriteSortables = [];
}

/**
 * Initialize folder sortables for each column
 */
function initializeFolderSortables() {
    const columns = document.querySelectorAll('.drop-zone');

    columns.forEach((column, index) => {
        const sortable = new Sortable(column, {
            group: 'folders', // Allow dragging between columns
            animation: 200,
            handle: '.drag-handle', // Only drag by the handle
            filter: '.list-group', // Don't make favorites sortable here
            preventOnFilter: false,
            delay: 150, // Delay to prevent accidental drags
            delayOnTouchStart: true,
            delayOnTouchOnly: true, // Only apply delay on touch devices
            touchStartThreshold: 20, // Require more movement before starting drag
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',

            // Custom placeholder
            onStart: function(evt) {
                console.log('Folder drag started');
                // Add visual feedback
                evt.item.classList.add('dragging');
            },

            onEnd: function(evt) {
                console.log('Folder drag ended');
                evt.item.classList.remove('dragging');

                // If item moved to different position or column
                if (evt.oldIndex !== evt.newIndex || evt.from !== evt.to) {
                    const folderId = evt.item.getAttribute('data-folder-id');
                    const newColumn = evt.to.getAttribute('data-column');
                    const newPosition = evt.newIndex;

                    console.log(`Moving folder ${folderId} to column ${newColumn}, position ${newPosition}`);

                    // Update folder position via API
                    updateFolderPosition(folderId, newColumn, newPosition);
                }
            },

            // Show insertion indicator
            onMove: function(evt) {
                // Don't allow dropping favorites into folder container
                if (evt.dragged.classList.contains('favorite-item')) {
                    return false;
                }
                return true;
            }
        });

        folderSortables.push(sortable);
    });
}

/**
 * Initialize favorite sortables within each folder
 */
function initializeFavoriteSortables() {
    const favoriteLists = document.querySelectorAll('.folder .list-group');
    console.log('Found', favoriteLists.length, 'favorite lists');

    favoriteLists.forEach((list, index) => {
        const sortable = new Sortable(list, {
            group: 'favorites', // Allow dragging between folders
            animation: 200,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',
            delay: 200, // Delay to distinguish from clicks
            delayOnTouchStart: true,
            delayOnTouchOnly: true, // Only apply delay on touch devices
            touchStartThreshold: 20, // Require more movement before starting drag

            onStart: function(evt) {
                console.log('Favorite drag started');
                evt.item.classList.add('dragging');
            },

            onEnd: function(evt) {
                console.log('Favorite drag ended');
                evt.item.classList.remove('dragging');

                // If item moved to different position or folder
                if (evt.oldIndex !== evt.newIndex || evt.from !== evt.to) {
                    const favoriteId = evt.item.getAttribute('data-favorite-id');
                    const newFolderId = evt.to.closest('.folder').getAttribute('data-folder-id');
                    const newPosition = evt.newIndex;

                    console.log(`Moving favorite ${favoriteId} to folder ${newFolderId}, position ${newPosition}`);

                    // Update favorite position via API
                    updateFavoritePosition(favoriteId, newFolderId, newPosition);
                }
            }
        });

        favoriteSortables.push(sortable);
    });
}

/**
 * Update folder position via API
 */
function updateFolderPosition(folderId, newColumn, newPosition) {
    const formData = new FormData();
    formData.append('folder_id', folderId);
    formData.append('target_column', newColumn);
    formData.append('target_position', newPosition);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch('/home/update-folder-column/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Folder position updated successfully');
            // Update the data attributes
            const folder = document.querySelector(`[data-folder-id="${folderId}"]`);
            if (folder) {
                folder.setAttribute('data-current-column', newColumn);
            }
            // Reload to reflect changes (like existing implementation)
            window.location.reload();
        } else {
            console.error('Error updating folder position:', data.error);
            alert('Error updating folder position: ' + data.error);
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating folder position');
        location.reload();
    });
}

/**
 * Update favorite position via API
 */
function updateFavoritePosition(favoriteId, newFolderId, newPosition) {
    // Get the dragged favorite element to check its current folder
    const draggedFavorite = document.querySelector(`[data-favorite-id="${favoriteId}"]`);
    const currentFolderId = draggedFavorite?.getAttribute('data-folder-id');

    // If moving within the same folder, use swap positions endpoint
    if (currentFolderId === newFolderId) {
        // Find the target favorite at the new position
        const folderContainer = document.querySelector(`[data-folder-id="${newFolderId}"] .favorites-list`);
        const favoritesInFolder = folderContainer?.querySelectorAll('[data-favorite-id]');

        if (favoritesInFolder && favoritesInFolder[newPosition]) {
            const targetFavoriteId = favoritesInFolder[newPosition].getAttribute('data-favorite-id');

            const formData = new FormData();
            formData.append('dragged_favorite_id', favoriteId);
            formData.append('target_favorite_id', targetFavoriteId);
            formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

            fetch('/home/swap-favorite-positions/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Favorite positions swapped successfully');
                    window.location.reload();
                } else {
                    console.error('Error swapping favorite positions:', data.error);
                    alert('Error updating favorite position: ' + data.error);
                    location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating favorite position');
                location.reload();
            });
        } else {
            console.log('No target favorite found for swap, position may already be correct');
            return;
        }
    } else {
        // Moving to different folder, use existing move endpoint
        const formData = new FormData();
        formData.append('dragged_favorite_id', favoriteId);
        formData.append('target_folder_id', newFolderId);
        formData.append('target_favorite_id', -1);
        formData.append('insert_below', 'true');
        formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

        fetch('/home/move-favorite-to-folder/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Favorite position updated successfully');
                // Update the data attributes
                const favorite = document.querySelector(`[data-favorite-id="${favoriteId}"]`);
                if (favorite) {
                    favorite.setAttribute('data-folder-id', newFolderId);
                }
                // Reload to reflect changes (like existing implementation)
                window.location.reload();
            } else {
                console.error('Error updating favorite position:', data.error);
                alert('Error updating favorite position: ' + data.error);
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error updating favorite position');
            location.reload();
        });
    }
}

/**
 * Get CSRF token from cookies (matches existing implementation)
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
    // Only initialize on home page
    if (document.querySelector('.drop-zone')) {
        initializeSortableDragDrop();
    }
});

// Re-initialize after HTMX updates
document.addEventListener('htmx:afterSwap', function(e) {
    // Check if we're on home page and content was updated
    if (e.target.id === 'content' || e.target.closest('.drop-zone')) {
        setTimeout(() => {
            initializeSortableDragDrop();
        }, 100); // Small delay to ensure DOM is ready
    }
});
