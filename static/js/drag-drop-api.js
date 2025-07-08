/**
 * AJAX API calls for drag-and-drop operations
 * Handles all server communication for folder and favorite reordering
 */

/**
 * Swap positions of two folders within the same column
 */
function swapFolderPositions(draggedFolderId, targetFolderId) {
    const formData = new FormData();
    formData.append('dragged_folder_id', draggedFolderId);
    formData.append('target_folder_id', targetFolderId);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    fetch('/home/swap-folder-positions/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload the page to reflect the changes
            window.location.reload();
        } else {
            console.error('Error swapping folders:', data.error);
            alert('Error swapping folders: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error swapping folders');
    });
}

/**
 * Insert folder above another folder
 */
function insertAboveFolder(draggedFolderId, targetFolderId, targetColumn) {
    const formData = new FormData();
    formData.append('dragged_folder_id', draggedFolderId);
    formData.append('target_folder_id', targetFolderId);
    formData.append('target_column', targetColumn);
    formData.append('insert_below', 'false');
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    fetch('/home/insert-folder-at-position/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload the page to reflect the changes
            window.location.reload();
        } else {
            console.error('Error inserting folder above:', data.error);
            alert('Error inserting folder above: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error inserting folder above');
    });
}

/**
 * Insert folder at specific position (cross-column drop)
 */
function insertFolderAtPosition(draggedFolderId, targetFolderId, targetColumn) {
    const formData = new FormData();
    formData.append('dragged_folder_id', draggedFolderId);
    formData.append('target_folder_id', targetFolderId);
    formData.append('target_column', targetColumn);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    fetch('/home/insert-folder-at-position/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload the page to reflect the changes
            window.location.reload();
        } else {
            console.error('Error inserting folder:', data.error);
            alert('Error inserting folder: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error inserting folder');
    });
}

/**
 * Update folder column (column drop zone)
 */
function updateFolderColumn(folderId, targetColumn, targetPosition) {
    const formData = new FormData();
    formData.append('folder_id', folderId);
    formData.append('target_column', targetColumn);
    if (targetPosition !== undefined) {
        formData.append('target_position', targetPosition);
    }
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    fetch('/home/update-folder-column/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload the page to reflect the changes
            window.location.reload();
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
 * Swap positions of two favorites within the same folder
 */
function swapFavoritePositions(draggedFavoriteId, targetFavoriteId) {
    const formData = new FormData();
    formData.append('dragged_favorite_id', draggedFavoriteId);
    formData.append('target_favorite_id', targetFavoriteId);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    fetch('/home/swap-favorite-positions/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload the page to reflect the changes
            window.location.reload();
        } else {
            console.error('Error swapping favorites:', data.error);
            alert('Error swapping favorites: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error swapping favorites');
    });
}

/**
 * Insert favorite below another favorite
 */
function insertFavoriteBelowFavorite(draggedFavoriteId, targetFavoriteId) {
    const formData = new FormData();
    formData.append('dragged_favorite_id', draggedFavoriteId);
    formData.append('target_favorite_id', targetFavoriteId);
    formData.append('insert_below', 'true');
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    fetch('/home/insert-favorite-at-position/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            console.error('Error inserting favorite:', data.error);
            alert('Error inserting favorite: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error inserting favorite');
    });
}

/**
 * Move favorite to a new folder
 */
function moveFavoriteToNewFolder(draggedFavoriteId, targetFavoriteId, targetFolderId) {
    const formData = new FormData();
    formData.append('dragged_favorite_id', draggedFavoriteId);
    if (targetFavoriteId) {
        formData.append('target_favorite_id', targetFavoriteId);
    }
    formData.append('target_folder_id', targetFolderId);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    fetch('/home/move-favorite-to-folder/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            console.error('Error moving favorite:', data.error);
            alert('Error moving favorite: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error moving favorite');
    });
}

/**
 * Move favorite to a folder (end of folder)
 */
function moveFavoriteToFolder(draggedFavoriteId, targetFolderId) {
    const formData = new FormData();
    formData.append('dragged_favorite_id', draggedFavoriteId);
    formData.append('target_folder_id', targetFolderId);
    formData.append('move_to_end', 'true'); // Indicate we want to move to end of folder
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    fetch('/home/move-favorite-to-folder/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            console.error('Error moving favorite:', data.error);
            alert('Error moving favorite: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error moving favorite');
    });
}

/**
 * Move favorite to an empty folder - send -1 as target_favorite_id to indicate empty folder
 */
function moveFavoriteToEmptyFolder(draggedFavoriteId, targetFolderId) {
    const formData = new FormData();
    formData.append('dragged_favorite_id', draggedFavoriteId);
    formData.append('target_favorite_id', '-1'); // Special value to indicate empty folder
    formData.append('target_folder_id', targetFolderId);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    fetch('/home/move-favorite-to-folder/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            console.error('Error moving favorite to empty folder:', data.error);
            alert('Error moving favorite to empty folder: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error moving favorite to empty folder');
    });
}