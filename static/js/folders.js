

function showAddFolderForm() {
    addFolderItem = document.querySelector('#add-folder');
    addFolderItem.style.display = 'flex';
    addFolderItem.querySelector('#add-folder-input').focus();
}


function hideAddFolderForm(){

    setTimeout(function () {
        element = document.querySelector('#add-folder');
        element.style.display = 'none';
    }, 1000);
}


function showEditFolderForm(folderId){


    // get the folder list item
    folderItem = document.querySelector('#folder-' + folderId);

    // hide the folder icon and link
    var folderLink = folderItem.querySelector('.folder-link');
    folderLink.style.display = 'none';

    // display the folder edit form and delete icon
    var editFolder = folderItem.querySelector('.edit-folder');
    editFolder.style.display = 'flex';

    // focus on the edit folder input
    var input = editFolder.querySelector('.form-control');
    input.focus();

}


function hideEditFolderForm(folderId){

    // get the folder list item
    folderItem = document.querySelector('#folder-' + folderId);

    setTimeout(function () {

        // hide the folder icon and link
        var folderLink = folderItem.querySelector('.folder-link');
        folderLink.style.display = 'inline';

        // display the folder edit form and delete icon
        var editFolder = folderItem.querySelector('.edit-folder');
        editFolder.style.display = 'none';

    }, 1000);
}
