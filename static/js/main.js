
function hide(elementId){
    var item = document.getElementById(elementId);
    item.style.display = 'none';
}


function show(elementId){
    var item = document.getElementById(elementId);
    item.style.display = 'block';
}


function showHide(elementId)
{
    var item = document.getElementById(elementId);
    console.log(item)
    if (item) {
        if (item.style.display == 'none') {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    }
}


function showHideHomeFolderControls(folder_id)
{
    var x = document.getElementsByClassName("folder-"+folder_id);
    var i;
    for (i = 0; i < x.length; i++) {
        if ( x[i].style.display == 'none' ) {
            x[i].style.display = 'flex';
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
    var elementId = "credential-hint-"+favorite_id;
    showHide(elementId);
    var elementId = "credential-data-"+favorite_id;
    showHide(elementId);

}

