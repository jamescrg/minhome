/**
 * Folder Tree Expand/Collapse Functions
 * Server-side state persistence via htmx
 */

/**
 * Get all descendant folder IDs for a given folder
 * @param {number} folderId - The parent folder ID
 * @returns {Array} Array of descendant folder IDs
 */
function getDescendantIds(folderId) {
    const descendants = [];
    const directChildren = document.querySelectorAll(`[data-parent-id="${folderId}"]`);

    directChildren.forEach(child => {
        const childId = child.id.replace('folder-', '');
        descendants.push(childId);
        descendants.push(...getDescendantIds(childId));
    });

    return descendants;
}

/**
 * Toggle a folder's expand/collapse state
 * @param {number} folderId - The folder ID to toggle
 * @param {string} page - The current page (tasks, favorites, contacts, notes)
 */
function toggleFolder(folderId, page) {
    const caretIcon = document.getElementById('caret-' + folderId);
    const children = document.querySelectorAll(`[data-parent-id="${folderId}"]`);

    if (!caretIcon || children.length === 0) return;

    const isCurrentlyHidden = children[0].style.display === 'none';

    if (isCurrentlyHidden) {
        // Expand - show direct children only
        children.forEach(child => {
            child.style.display = '';
        });
        caretIcon.classList.remove('bi-caret-right-fill');
        caretIcon.classList.add('bi-caret-down-fill');
    } else {
        // Collapse - hide all descendants
        const allDescendantIds = getDescendantIds(folderId);
        allDescendantIds.forEach(descId => {
            const descItem = document.getElementById('folder-' + descId);
            if (descItem) {
                descItem.style.display = 'none';
            }
            // Also collapse expanded descendants visually
            const descCaret = document.getElementById('caret-' + descId);
            if (descCaret) {
                descCaret.classList.remove('bi-caret-down-fill');
                descCaret.classList.add('bi-caret-right-fill');
            }
        });
        caretIcon.classList.remove('bi-caret-down-fill');
        caretIcon.classList.add('bi-caret-right-fill');
    }

    // Persist state to server
    htmx.ajax('POST', `/folders/${folderId}/${page}/toggle-expand`);
}
