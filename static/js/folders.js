

function showAddFolderForm() {
    addFolderItem = document.querySelector('#folder-add');
    addFolderItem.style.display = 'flex';
    addFolderItem.querySelector('#folder-add-input').focus();
}


function hideAddFolderForm(){

    setTimeout(function () {
        element = document.querySelector('#folder-add');
        element.style.display = 'none';
    }, 1000);
}


function showEditFolderForm(folderId){


    // get the folder list item
    folderItem = document.querySelector('#folder-' + folderId);
    folderItem.classList.add('li-folder-edit');

    // hide the folder icon and link
    var folderLink = folderItem.querySelector('.folder-link');
    folderLink.style.display = 'none';

    // display the folder edit form and delete icon
    var editFolder = folderItem.querySelector('.folder-edit');
    editFolder.style.display = 'block';

    // focus on the edit folder input
    var input = editFolder.querySelector('.form-control');

    event.preventDefault();

}


function hideEditFolderForm(folderId){

    // get the folder list item
    folderItem = document.querySelector('#folder-' + folderId);

    setTimeout(function () {

        // hide the folder icon and link
        var folderLink = folderItem.querySelector('.folder-link');
        folderLink.style.display = 'inline';

        // display the folder edit form and delete icon
        var editFolder = folderItem.querySelector('.folder-edit');
        editFolder.style.display = 'none';

        folderItem.classList.remove('li-folder-edit');

    }, 1000);
}
