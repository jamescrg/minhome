

def index():
    user_id = request.user.id
    page = 'favorites'
    folders = FoldersController::getAll(page)
    selectedFolder = Folder.objects.filter(user_id=user_id, page=page, selected=1).first()
    if selectedFolder == null: 
            selectedFolder = 0
        else:
            selectedFolder = selectedFolder.id
    
    favorites = Favorite.objects.filter(user_id=user_id, folder_id=selectedFolder)
                                            .order_by('name').get()
    return view('favorites/content', context)


def create(id):
    user_id = request.user.id
    page = 'favorites'
    action = '/favorites'
    edit = false
    selectedFolderId = id
    selectedFolder = Folder.objects.filter(user_id=user_id, page=page, selected=1).first()
    folders = FoldersController::getAll('favorites')
    favorite = new Favorite
    favorite.folder_id = id
    return view('favorites/content', context)


def edit(id):
    user_id = request.user.id
    page = 'favorites'
    edit = true
    action = '/favorites/update/' . id
    folders = FoldersController::getAll(page)
    selectedFolder = Folder.objects.filter(user_id=user_id, page=page, selected=1).first()
    favorite = Favorite::findOrFail(id)
    return view('favorites/content', context)


def update(id, Requests\CreateFavoriteRequest request):
    input = request.all()
    input['user_id'] = request.user.id
    favorite = Favorite.objects.filter(id=id, user_id=input['user_id').first()
    favorite.update(input)
    return redirect('/favorites')


def home(id):
    user_id = request.user.id
    favorite = Favorite.objects.filter(id=id, user_id=user_id).first()
    if (favorite.home_rank > 0) 
            favorite.home_rank = 0
        else 
            favorite.home_rank = 1
    
    favorite.save()
    return redirect('/favorites')


def destroy(id):
    user_id = request.user.id
    favorite = Favorite.objects.filter(id=id, user_id=user_id).first()
    favorite.delete()
    return redirect('/favorites')


