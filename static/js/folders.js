

function showEditFolderForm(folderId){


    // get the folder list item
    var folderItem = document.querySelector('#folder-' + folderId);

    // hide the folder icon and link
    var folderLink = folderItem.querySelector('.folder-link');
    folderLink.style.display = 'none';

    // display the folder edit form and delete icon
    var editFolder = folderItem.querySelector('.edit-folder');
    editFolder.style.display = 'flex';

    // focus on the edit folder input
    var input = editFolder.querySelector('.form-control');
    input.focus();

    // show the folder menu
    var folderMenu = folderItem.querySelector('.folder-menu');
    folderMenu.style.display = 'block';

}


function hideEditFolderForm(){

    // get the folder list item
    var parentElement = event.target.parentElement.parentElement.parentElement;

    setTimeout(function () {

        // hide the folder
        var child = parentElement.querySelector('.show-folder');
        child.style.display = 'inline';

        // display the folder edit form and delete icon
        var child = parentElement.querySelector('.edit-folder');
        child.style.display = 'none';

    }, 500);
}


function showAddFolderForm() {
    addFolderItem = document.querySelector('#add-folder-item');
    addFolderItem.style.display = 'flex';
    addFolderItem.querySelector('.edit-folder').style.display = 'flex';
    addFolderItem.querySelector('#add-folder-input').focus();
}


function hideAddFolderForm(){

    var parentElement = event.target.parentElement.parentElement.parentElement;

    setTimeout(function () {
        var elementId = 'add-folder-item';
        hide(elementId);
    }, 500);
}

