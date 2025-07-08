/**
 * Folder drag-and-drop functionality
 * Handles folder dragging between and within columns
 */

/**
 * Handle drag start for folder drag handles
 */
function handleDragHandleDragStart(e) {
    // Find the parent folder
    const folder = this.closest('.folder');
    
    if (folder) {
        draggedFolder = folder;
        folder.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', folder.outerHTML);
    }
}

/**
 * Handle drag end for folder drag handles
 */
function handleDragHandleDragEnd(e) {
    // Find the parent folder
    const folder = this.closest('.folder');
    if (folder) {
        folder.classList.remove('dragging', 'drag-enabled');
    }
    
    // Remove drag-over class from all drop zones and folders
    const dropZones = document.querySelectorAll('.drop-zone');
    dropZones.forEach(zone => {
        zone.classList.remove('drag-over', 'drop-zone-active');
    });
    
    const folders = document.querySelectorAll('.folder');
    folders.forEach(folder => {
        folder.classList.remove('drag-over-top', 'drag-over-bottom', 'drop-target-active', 'insertion-target');
    });
    
    // Remove any insertion indicators from anywhere in the document
    const existingIndicators = document.querySelectorAll('.insertion-indicator');
    existingIndicators.forEach(indicator => {
        indicator.remove();
    });
}

/**
 * Handle drag over for folders
 */
function handleFolderDragOver(e) {
    // Only handle folder drags, ignore favorite drags completely
    if (draggedFavorite !== null) {
        return; // Let favorite handlers deal with it
    }
    
    if (e.preventDefault) {
        e.preventDefault();
    }
    
    // Don't allow dropping on self
    if (this === draggedFolder) {
        return false;
    }
    
    // Only show indicator when dragging folders
    if (draggedFolder !== null) {
        // Clear previous hover states and insertion indicators
        const folders = document.querySelectorAll('.folder');
        folders.forEach(folder => {
            folder.classList.remove('drag-over-top', 'drag-over-bottom', 'insertion-target');
        });
        
        // Add a simple CSS class to show insertion point
        this.classList.add('insertion-target');
    }
    
    e.dataTransfer.dropEffect = 'move';
    return false;
}

/**
 * Handle drag leave for folders
 */
function handleFolderDragLeave(e) {
    // Remove the insertion indicator when leaving the folder
    this.classList.remove('insertion-target');
}

/**
 * Handle drop on folders
 */
function handleFolderDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    // Don't allow dropping on self
    if (this === draggedFolder) {
        return false;
    }
    
    if (draggedFolder !== null) {
        const draggedFolderId = draggedFolder.getAttribute('data-folder-id');
        const draggedColumn = parseInt(draggedFolder.getAttribute('data-current-column'));
        const targetFolderId = this.getAttribute('data-folder-id');
        const targetColumn = parseInt(this.getAttribute('data-current-column'));
        
        // Always insert above the target folder when dropping on any folder or its extended zone
        insertAboveFolder(draggedFolderId, targetFolderId, targetColumn);
    }
    
    return false;
}

/**
 * Handle general drag over for drop zones
 */
function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    
    // Temporarily disabled - this might be removing indicators too aggressively
    // Clear insertion indicators when dragging over drop zones
    // const existingIndicators = document.querySelectorAll('.insertion-indicator');
    // existingIndicators.forEach(indicator => {
    //     indicator.remove();
    // });
    
    e.dataTransfer.dropEffect = 'move';
    return false;
}

/**
 * Handle drag enter for drop zones
 */
function handleDragEnter(e) {
    this.classList.add('drag-over');
}

/**
 * Handle drag leave for drop zones
 */
function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

/**
 * Handle drop on column drop zones
 */
function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    this.classList.remove('drag-over');
    
    if (draggedFolder !== null) {
        const folderId = draggedFolder.getAttribute('data-folder-id');
        const targetColumn = this.getAttribute('data-column');
        const currentColumn = draggedFolder.getAttribute('data-current-column');
        
        if (targetColumn !== currentColumn) {
            // Calculate position at end of column
            const foldersInColumn = this.querySelectorAll('.folder').length;
            // Update folder column via AJAX
            updateFolderColumn(folderId, targetColumn, foldersInColumn);
        }
    }
    
    return false;
}