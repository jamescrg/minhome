/**
 * Folder hierarchy drag-and-drop functionality
 * Handles folder dragging for reorganizing folder hierarchy on content pages
 * Uses timer-based click vs drag detection like favorites on home page
 */

let draggedFolderItem = null;
let isDragging = false;
let dragTimeout = null;
let currentDropTarget = null;

/**
 * Initialize folder hierarchy drag and drop
 */
function initializeFolderHierarchyDragDrop() {
    const folderContainer = document.querySelector('.folders');
    if (!folderContainer) return;

    // Detect if we're on a mobile device (more specific detection)
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
                     (navigator.maxTouchPoints > 0 && /Mobi|Android/i.test(navigator.userAgent));

    console.log('Mobile detection:', isMobile, 'User agent:', navigator.userAgent, 'MaxTouchPoints:', navigator.maxTouchPoints);

    // Get all folder items and links
    const folderItems = document.querySelectorAll('.folder-item');
    const folderLinks = document.querySelectorAll('.folder-link');

    folderItems.forEach(item => {
        const link = item.querySelector('.folder-link');
        if (!link) return;

        // Allow dragging shared folders (editors can now move them)

        // Touch-based drag detection variables
        let touchStartPos = null;
        let isTouchSequence = false;
        let isDragModeActive = false;
        let isScrolling = false;
        const MOVE_THRESHOLD = 10; // pixels
        const SCROLL_THRESHOLD = 5; // pixels - smaller threshold for scroll detection
        const TAP_DURATION = 200; // milliseconds - max duration for a tap

        // On mobile: completely disable HTML5 drag, on desktop: start disabled
        if (isMobile) {
            item.draggable = false;
            item.removeAttribute('draggable');
            // Prevent any drag events on mobile
            item.addEventListener('dragstart', function(e) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                return false;
            }, { capture: true });
        } else {
            item.draggable = false;
        }

        // Separate mouse and touch event handlers
        const handleMouseStart = function(e) {
            // Don't interfere with touch events
            if (e.type === 'touchstart') return;

            // Mouse: Enable dragging immediately for desktop
            item.draggable = true;
            item.setAttribute('draggable', 'true');
        };

        const handleMouseEnd = function(e) {
            // Don't interfere with touch events
            if (e.type === 'touchend') return;

            // Mouse handling - reset draggable state
            setTimeout(() => {
                if (!isDragging) {
                    item.draggable = false;
                }
            }, 10);
        };

        const handleTouchStart = function(e) {

            // DON'T prevent default initially - allow scrolling until we confirm long press
            // e.preventDefault(); // Removed to allow scrolling

            // Set touch sequence flag
            isTouchSequence = true;

            // Record initial touch position
            touchStartPos = {
                x: e.touches[0].clientX,
                y: e.touches[0].clientY,
                time: Date.now()
            };

            // Add visual feedback for potential long press
            item.classList.add('long-pressing');

            // Start long press timer
            dragTimeout = setTimeout(() => {
                // Long press threshold met - check if finger hasn't moved too much
                if (!hasMovedSignificantly(touchStartPos, e.touches[0])) {
                    // Long press confirmed without significant movement
                    confirmLongPress();
                } else {
                    // Moved too much, cancel long press
                    cancelLongPress();
                }
            }, 500); // 500ms long press threshold

            // Add movement monitoring
            document.addEventListener('touchmove', handleTouchMoveMonitor, { passive: false });
            document.addEventListener('touchend', handleTouchEndLocal, { passive: false });
        };

        // Helper function to check if touch has moved significantly
        const hasMovedSignificantly = function(startPos, currentTouch) {
            if (!startPos || !currentTouch) return false;
            const deltaX = Math.abs(currentTouch.clientX - startPos.x);
            const deltaY = Math.abs(currentTouch.clientY - startPos.y);
            return (deltaX > MOVE_THRESHOLD || deltaY > MOVE_THRESHOLD);
        };

        // Helper function to confirm long press and enter drag mode
        const confirmLongPress = function() {

            // Remove long press indicator
            item.classList.remove('long-pressing');

            // Enter drag mode
            isDragModeActive = true;
            isDragging = true;
            draggedFolderItem = item;
            item.classList.add('dragging');

            // Add visual feedback
            item.style.opacity = '0.8';
            item.style.transform = 'scale(1.05)';

            // Haptic feedback if available
            if (navigator.vibrate) {
                navigator.vibrate(50);
            }

            // Now listen for drag movements
            document.addEventListener('touchmove', handleDragMove, { passive: false });
        };

        // Helper function to cancel long press
        const cancelLongPress = function() {

            // Clean up visual feedback
            item.classList.remove('long-pressing');

            // Reset touch sequence flag to allow normal behavior
            isTouchSequence = false;

            // Clean up listeners
            document.removeEventListener('touchmove', handleTouchMoveMonitor);
            document.removeEventListener('touchend', handleTouchEndLocal);
        };

        // Monitor touch movement during long press detection
        const handleTouchMoveMonitor = function(e) {
            if (!touchStartPos) return;

            const deltaX = Math.abs(e.touches[0].clientX - touchStartPos.x);
            const deltaY = Math.abs(e.touches[0].clientY - touchStartPos.y);

            // Detect scrolling with a small threshold
            if (deltaX > SCROLL_THRESHOLD || deltaY > SCROLL_THRESHOLD) {
                // Mark as scrolling
                isScrolling = true;

                // Cancel any drag detection
                clearTimeout(dragTimeout);
                cancelLongPress();

                // Don't prevent default - allow scrolling
                return;
            }

            // Check if moved significantly for drag purposes
            if (hasMovedSignificantly(touchStartPos, e.touches[0])) {
                // Too much movement for long press, but not scrolling
                clearTimeout(dragTimeout);
                cancelLongPress();
            } else {
                // Still within threshold - this might be a long press
                // Only prevent default if we're very close to the original position
                if (deltaX < SCROLL_THRESHOLD && deltaY < SCROLL_THRESHOLD) {
                    e.preventDefault();
                }
            }
        };

        // Handle dragging movement (after long press confirmed)
        const handleDragMove = function(e) {
            if (!isDragModeActive) return;

            e.preventDefault();

            console.log('DRAG MOVE');

            // Update visual feedback during drag
            const touch = e.touches[0];

            // Find element under touch for drop target highlighting
            item.style.pointerEvents = 'none';
            const elementBelow = document.elementFromPoint(touch.clientX, touch.clientY);
            item.style.pointerEvents = 'auto';

            // Clean up previous drop targets
            cleanupAllDropTargets();

            if (elementBelow) {
                const targetFolder = elementBelow.closest('.folder-item');
                if (targetFolder && targetFolder !== item) {
                    targetFolder.classList.add('drop-target');
                    currentDropTarget = targetFolder;
                }

                const titleDropZone = elementBelow.closest('.folders-title-drop-zone');
                if (titleDropZone) {
                    titleDropZone.classList.add('drop-target');
                    currentDropTarget = titleDropZone;
                }
            }
        };

        const handleTouchEndLocal = function(e) {
            console.log('TOUCH END');

            // Clear timeout if still running
            clearTimeout(dragTimeout);

            // Clean up listeners
            document.removeEventListener('touchmove', handleTouchMoveMonitor);
            document.removeEventListener('touchend', handleTouchEndLocal);

            if (isDragModeActive) {
                // We were in drag mode, handle drop
                console.log('DRAG END - Processing drop');

                const touch = e.changedTouches[0];

                // Find drop target
                item.style.pointerEvents = 'none';
                const elementBelow = document.elementFromPoint(touch.clientX, touch.clientY);
                item.style.pointerEvents = 'auto';

                if (elementBelow && currentDropTarget) {
                    const draggedId = item.getAttribute('data-folder-id');

                    if (currentDropTarget.classList.contains('folders-title-drop-zone')) {
                        // Move to root
                        console.log('Moving to root');
                        moveFolderToRoot(draggedId);
                    } else {
                        // Move to folder
                        const targetId = currentDropTarget.getAttribute('data-folder-id');
                        console.log('Moving to folder:', targetId);
                        moveFolderToFolder(draggedId, targetId);
                    }
                }

                // Clean up drag state
                isDragModeActive = false;
                isDragging = false;
                draggedFolderItem = null;
                item.classList.remove('dragging');
                item.style.opacity = '';
                item.style.transform = '';
                cleanupAllDropTargets();

                document.removeEventListener('touchmove', handleDragMove);
            } else {
                // Short tap - handle navigation
                console.log('SHORT TAP - Navigation');

                // Clean up any visual feedback
                item.classList.remove('long-pressing');

                // Allow navigation only if:
                // 1. Not scrolling
                // 2. Touch was on the link itself
                // 3. Touch duration was short (tap, not long press)
                // 4. Didn't move significantly
                if (!isScrolling &&
                    !hasMovedSignificantly(touchStartPos, e.changedTouches[0]) &&
                    touchStartPos && (Date.now() - touchStartPos.time) < TAP_DURATION) {

                    const touch = e.changedTouches[0];
                    const elementAtTouch = document.elementFromPoint(touch.clientX, touch.clientY);

                    // Check if the touched element is the link or a child of the link
                    if (elementAtTouch && (elementAtTouch === link || link.contains(elementAtTouch))) {
                        link.click();
                    }
                }
            }

            // Reset state
            isTouchSequence = false;
            touchStartPos = null;
            isScrolling = false;
        };

        // Add mouse listeners for desktop drag functionality
        item.addEventListener('mousedown', handleMouseStart);
        item.addEventListener('mouseup', handleMouseEnd);

        // Add HTML5 drag event listeners only on desktop
        if (!isMobile) {
            item.addEventListener('dragstart', function(e) {
                // Prevent drag if item is not explicitly draggable or during touch sequence
                if (!item.draggable || (isTouchSequence && !isDragging)) {
                    e.preventDefault();
                    e.stopPropagation();
                    e.stopImmediatePropagation();
                    return false;
                }
                isDragging = true;
                draggedFolderItem = item;
                item.classList.add('dragging');
            }, { capture: true });

            item.addEventListener('dragend', function(e) {
                isDragging = false;
                draggedFolderItem = null;
                item.classList.remove('dragging');
                item.draggable = false;
            });
        }

        // Add touch listeners to the entire item (for larger touch target) with capture
        item.addEventListener('touchstart', handleTouchStart, { passive: false, capture: true });
        item.addEventListener('touchend', handleTouchEndLocal, { capture: true });

        // Note: Extensive drag event logging removed for production

        // Prevent context menu on long press
        item.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            return false;
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

/**
 * Clean up all drop target styles
 */
function cleanupAllDropTargets() {
    // Remove drop target class from all folder items
    const allFolders = document.querySelectorAll('.folder-item.drop-target');
    allFolders.forEach(folder => {
        folder.classList.remove('drop-target');
    });

    // Remove drop target class from title drop zone
    const titleDropZone = document.querySelector('.folders-title-drop-zone.drop-target');
    if (titleDropZone) {
        titleDropZone.classList.remove('drop-target');
    }

    currentDropTarget = null;
}

function handleDragEnd(e) {
    // Clean up all drop targets when drag ends
    cleanupAllDropTargets();

    const folderItem = e.target.closest('.folder-item');
    if (folderItem) {
        folderItem.classList.remove('dragging');
    }
}

function handleDragOver(e) {
    if (!isDragging) return;

    e.preventDefault();
    e.stopPropagation();

    const folderItem = e.target.closest('.folder-item');
    const titleDropZone = e.target.closest('.folders-title-drop-zone');

    // Clear previous drop target
    if (currentDropTarget) {
        currentDropTarget.classList.remove('drop-target');
    }

    if (folderItem && folderItem !== draggedFolderItem) {
        // Valid drop target
        folderItem.classList.add('drop-target');
        currentDropTarget = folderItem;
    } else if (titleDropZone) {
        // Drop on title zone (move to root)
        titleDropZone.classList.add('drop-target');
        currentDropTarget = titleDropZone;
    }
}

function handleDragLeave(e) {
    if (!isDragging) return;

    // Only remove drop target if we're actually leaving the container
    if (!e.currentTarget.contains(e.relatedTarget)) {
        cleanupAllDropTargets();
    }
}

function handleDrop(e) {
    if (!isDragging) return;

    e.preventDefault();
    e.stopPropagation();

    const folderItem = e.target.closest('.folder-item');
    const titleDropZone = e.target.closest('.folders-title-drop-zone');

    if (folderItem && folderItem !== draggedFolderItem) {
        // Move folder into another folder
        const draggedFolderId = draggedFolderItem.getAttribute('data-folder-id');
        const targetFolderId = folderItem.getAttribute('data-folder-id');

        if (draggedFolderId && targetFolderId) {
            moveFolderToFolder(draggedFolderId, targetFolderId);
        }
    } else if (titleDropZone) {
        // Move folder to root
        const draggedFolderId = draggedFolderItem.getAttribute('data-folder-id');
        if (draggedFolderId) {
            moveFolderToRoot(draggedFolderId);
        }
    }

    cleanupAllDropTargets();
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

    // Use the cleanup function to remove all drop indicators
    cleanupAllDropTargets();

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

    // Allow moving shared folders (editors can now move them)

    // Don't allow dropping on descendants
    const draggedId = draggedFolderItem.getAttribute('data-folder-id');
    const targetId = this.getAttribute('data-folder-id');

    if (isDescendant(draggedId, targetId)) {
        return false;
    }

    // Check depth limit (3 levels maximum)
    const targetDepth = getFolderDepth(this);
    if (targetDepth >= 2) { // 0-indexed: 0=root, 1=level1, 2=level2 (can't add level3)
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
    // Only remove drop-target if we're actually leaving this folder
    // Check if the related target (where we're going) is outside this folder
    if (!this.contains(e.relatedTarget)) {
        this.classList.remove('drop-target');
    }
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

    // Allow moving shared folders (editors can now move them)

    const draggedId = draggedFolderItem.getAttribute('data-folder-id');
    const targetId = this.getAttribute('data-folder-id');

    // Don't allow dropping on descendants
    if (isDescendant(draggedId, targetId)) {
        return false;
    }

    // Check depth limit (3 levels maximum)
    const targetDepth = getFolderDepth(this);
    if (targetDepth >= 2) { // 0-indexed: 0=root, 1=level1, 2=level2 (can't add level3)
        showCustomAlert('Cannot nest folders more than 3 levels deep');
        this.classList.remove('drop-target');
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

    // Allow moving shared folders (editors can now move them)

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

    // Allow moving shared folders (editors can now move them)

    const draggedId = draggedFolderItem.getAttribute('data-folder-id');

    this.classList.remove('drop-target');

    // Move the folder to root level (no parent)
    moveFolderToParent(draggedId, null);

    return false;
}

/**
 * Get the depth of a folder (0 = root level, 1 = first level, etc.)
 */
function getFolderDepth(folderElement) {
    const level = folderElement.getAttribute('data-level');
    return level ? parseInt(level, 10) : 0;
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
 * Show custom alert modal
 */
function showCustomAlert(message) {
    const messageElement = document.getElementById('customAlertMessage');
    const modal = document.getElementById('customAlertModal');

    if (messageElement && modal) {
        messageElement.textContent = message;
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    } else {
        // Fallback to regular alert if modal elements not found
        alert(message);
    }
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

    // Get current page
    const page = window.location.pathname.split('/')[1] || 'tasks';

    // Toggle visually immediately for better UX
    const isExpanded = folderItem.classList.contains('expanded');
    if (isExpanded) {
        folderItem.classList.remove('expanded');
        childrenContainer.classList.add('collapsed');
        icon.classList.remove('bi-chevron-down');
        icon.classList.add('bi-chevron-right');
    } else {
        folderItem.classList.add('expanded');
        childrenContainer.classList.remove('collapsed');
        icon.classList.remove('bi-chevron-right');
        icon.classList.add('bi-chevron-down');
    }

    // Update server state
    fetch(`/folders/toggle/${folderId}/${page}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            // Revert visual state if server update failed
            if (isExpanded) {
                folderItem.classList.add('expanded');
                childrenContainer.classList.remove('collapsed');
                icon.classList.add('bi-chevron-down');
                icon.classList.remove('bi-chevron-right');
            } else {
                folderItem.classList.remove('expanded');
                childrenContainer.classList.add('collapsed');
                icon.classList.remove('bi-chevron-down');
                icon.classList.add('bi-chevron-right');
            }
        }
    })
    .catch(error => {
        console.error('Error toggling folder:', error);
        // Revert visual state on error
        if (isExpanded) {
            folderItem.classList.add('expanded');
            childrenContainer.classList.remove('collapsed');
            icon.classList.add('bi-chevron-down');
            icon.classList.remove('bi-chevron-right');
        } else {
            folderItem.classList.remove('expanded');
            childrenContainer.classList.add('collapsed');
            icon.classList.remove('bi-chevron-down');
            icon.classList.add('bi-chevron-right');
        }
    });
}

/**
 * Get CSRF token from cookies
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

/**
 * Handle touch move for folder dragging
 */
function handleTouchMove(e) {
    if (!isDragging || !draggedFolderItem) return;

    e.preventDefault();

    const touch = e.touches[0];

    // Visual feedback during drag
    draggedFolderItem.style.opacity = '0.5';

    // Find element under touch point
    draggedFolderItem.style.pointerEvents = 'none';
    const elementBelow = document.elementFromPoint(touch.clientX, touch.clientY);
    draggedFolderItem.style.pointerEvents = 'auto';

    if (!elementBelow) return;

    // Clean up previous drop targets
    cleanupAllDropTargets();

    // Check if we're over a folder item
    const targetFolder = elementBelow.closest('.folder-item');
    if (targetFolder && targetFolder !== draggedFolderItem) {
        // Check if it's a valid drop target
        const draggedId = draggedFolderItem.getAttribute('data-folder-id');
        const targetId = targetFolder.getAttribute('data-folder-id');

        if (!isDescendant(draggedId, targetId) && getFolderDepth(targetFolder) < 2) {
            targetFolder.classList.add('drop-target');
            currentDropTarget = targetFolder;
        }
    }

    // Check if we're over the title drop zone
    const titleDropZone = elementBelow.closest('.folders-title-drop-zone');
    if (titleDropZone) {
        titleDropZone.classList.add('drop-target');
        currentDropTarget = titleDropZone;
    }
}

/**
 * Handle touch end for folder dragging
 */
function handleTouchEnd(e) {
    console.log('handleTouchEnd called, isDragging:', isDragging, 'draggedFolderItem:', draggedFolderItem);

    if (!isDragging || !draggedFolderItem) return;

    // Get the final touch position to find drop target
    const touch = e.changedTouches[0];
    console.log('Touch position:', touch.clientX, touch.clientY);

    // Find element under final touch point
    draggedFolderItem.style.pointerEvents = 'none';
    const elementBelow = document.elementFromPoint(touch.clientX, touch.clientY);
    draggedFolderItem.style.pointerEvents = 'auto';

    console.log('Element below touch:', elementBelow);

    // Reset visual state
    draggedFolderItem.style.opacity = '';
    draggedFolderItem.style.transform = '';

    let dropTarget = null;

    if (elementBelow) {
        // Check if we're over the title drop zone
        const titleDropZone = elementBelow.closest('.folders-title-drop-zone');
        if (titleDropZone && titleDropZone.classList.contains('drop-target')) {
            dropTarget = titleDropZone;
        } else {
            // Check if we're over a folder item
            const targetFolder = elementBelow.closest('.folder-item');
            if (targetFolder && targetFolder.classList.contains('drop-target')) {
                dropTarget = targetFolder;
            }
        }
    }

    // Handle drop if we have a valid target
    if (dropTarget) {
        const draggedId = draggedFolderItem.getAttribute('data-folder-id');
        console.log('Drop target found:', dropTarget, 'draggedId:', draggedId);

        if (dropTarget.classList.contains('folders-title-drop-zone')) {
            // Move to root
            console.log('Moving to root');
            moveFolderToRoot(draggedId);
        } else {
            // Move to folder
            const targetId = dropTarget.getAttribute('data-folder-id');
            console.log('Moving to folder:', targetId);
            moveFolderToFolder(draggedId, targetId);
        }
    } else {
        console.log('No drop target found');
    }

    // Clean up
    cleanupAllDropTargets();
    draggedFolderItem.classList.remove('dragging');
    draggedFolderItem.draggable = false;
    draggedFolderItem = null;
    isDragging = false;
    currentDropTarget = null;

    // Remove listeners
    document.removeEventListener('touchmove', handleTouchMove);
    document.removeEventListener('touchend', handleTouchEnd);
}

/**
 * Move folder to another folder
 */
function moveFolderToFolder(draggedFolderId, targetFolderId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const page = getCurrentPage();

    console.log('Moving folder', draggedFolderId, 'to folder', targetFolderId, 'on page', page);

    fetch(`/folders/move/${draggedFolderId}/${page}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            new_parent_id: targetFolderId
        })
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.success) {
            location.reload();
        } else {
            console.error('Server error:', data.error);
            alert('Error moving folder: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Network error:', error);
        alert('Error moving folder: ' + error.message);
    });
}

/**
 * Move folder to root
 */
function moveFolderToRoot(draggedFolderId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const page = getCurrentPage();

    console.log('Moving folder', draggedFolderId, 'to root on page', page);

    fetch(`/folders/move/${draggedFolderId}/${page}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            new_parent_id: null
        })
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.success) {
            location.reload();
        } else {
            console.error('Server error:', data.error);
            alert('Error moving folder: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Network error:', error);
        alert('Error moving folder: ' + error.message);
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Run after a small delay to ensure other scripts have finished
    setTimeout(() => {
        initializeFolderHierarchyDragDrop();
        initializeFolderExpandCollapse();
        // restoreFolderStates(); // Not needed - state is restored server-side

        // Mobile protection is handled in the main initialization function
    }, 100);

    // Global failsafe to clean up drop targets
    window.addEventListener('dragend', function() {
        cleanupAllDropTargets();
    });
});

// Re-initialize after HTMX updates
document.addEventListener('htmx:afterSwap', function(e) {
    // Only reinitialize if the target contains folder content
    if (e.target.id === 'folder-list' || e.target.closest('#folder-list')) {
        initializeFolderHierarchyDragDrop();
        initializeFolderExpandCollapse();
        // restoreFolderStates(); // Not needed - state is restored server-side
    }
});

// Also listen for afterSettle to ensure DOM is fully ready
document.addEventListener('htmx:afterSettle', function(e) {
    // Only reinitialize if the target contains folder content
    if (e.target.id === 'folder-list' || e.target.closest('#folder-list')) {
        initializeFolderHierarchyDragDrop();
        initializeFolderExpandCollapse();
    }
});
