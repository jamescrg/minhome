
function showHide(elementId)
{
    var item = document.getElementById(elementId);
    if (item) {
        if (item.style.display == 'none') {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    }
}

function showHideFolder(folder_id)
{
    var elementId = "folderItem-"+folder_id;
    showHide(elementId);
    var elementId = "folderForm-"+folder_id;
    showHide(elementId);
    var elementId = "folderInput-"+folder_id;
    document.getElementById(elementId).focus();
}

function showHideHomeFolderControls(folder_id)
{
    var x = document.getElementsByClassName("home-folder-controls-"+folder_id);
    var i;
    for (i = 0; i < x.length; i++) {
        if ( x[i].style.display == 'none' ) {
            x[i].style.display = 'block';
        } else {
            x[i].style.display = 'none';
        }
    }
}

function showHideHomeLinkControls(folder_id)
{
    var x = document.getElementsByClassName("home-link-controls-"+folder_id);
    var i;
    for (i = 0; i < x.length; i++) {
        if ( x[i].style.display == 'none' ) {
            x[i].style.display = 'inline';
        } else {
            x[i].style.display = 'none';
        }
    }
}

function showHideHomeControls(folder_id)
{
    showHideHomeFolderControls(folder_id);
    showHideHomeLinkControls(folder_id);
}

function showHideCredentials(favorite_id)
{
    var elementId = "credentialHint-"+favorite_id;
    showHide(elementId);
    var elementId = "credentialData-"+favorite_id;
    showHide(elementId);

}

