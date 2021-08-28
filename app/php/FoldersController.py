

# get all folders for page
def getAll(page):
    user_id = request.user.id
    folders = Folder.objects.filter(user_id=user_id, page=page).order_by('name')
    return folders


# select a folder
def select(id, page):

    user_id = request.user.id

    if page != 'tasks':
        Folder.objects.filter(page=page, user_id=user_id).update(selected=0)
        if id > 0: 
            folder = Folder.objects.filter(id=id, user_id=user_id).first()
            folder.selected = 1
    
    if page == 'tasks':
        folder = Folder::findOrFail(id)
        if folder.active == 1:
            folder.active = 0

        if folder.selected == 1:
            folder.selected = 0
        else:
            folder.selected = 1

    folder.save()
    return redirect(f'/{page}/')


def home(id, page):
    user_id = request.user.id
    folder = Folder.objects.filter(id=id, user_id=user_id).first()
    if folder.home_column > 0: 
        folder.home_column = 0
        folder.home_rank = 0
    else: 
        folder.home_column = 4
        maxRank = Folder.objects.filter(user_id=user_id, home_column=4 ]).max('home_rank')
        folder.home_rank = maxRank + 1
    folder.save()
    return redirect(page)
