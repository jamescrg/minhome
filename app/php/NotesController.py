

def index():
    user_id = request.user.id
    page = 'notes'
    folders = FoldersController::getAll(page)
    selectedFolder = Folder.objects.filter(user_id=user_id, page=page, selected=1).first()
    if selectedFolder:
        notes = Note.objects.filter(user_id=user_id, folder_id=selectedFolder.id).order_by('subject').get()
    else:
        notes = Note.objects.filter('user_id', user_id).where('folder_id', 0).order_by('subject').get()
    selectedNote =  Note.objects.filter(user_id=user_id, selected=1).first()
    return view('notes/content', context)


def show(id):
    user_id = request.user.id
    Note.objects.filter(user_id=user_id, selected=1).update(selected=0)
    Note.objects.filter(id=id, user_id=user_id).update(selected=1)
    return redirect('/notes/')


def create(id):
    user_id = request.user.id
    page = 'notes'
    action = '/notes'
    edit = false
    selectedFolderId = id
    selectedFolder = Folder.objects.filter(user_id=user_id, page=page, selected=1).first()
    folders = FoldersController::getAll('notes')
    note = new Note
    note.folder_id = id
    return view('notes/content', context)


def update(Requests\CreateNoteRequest request):
    input = request.all()
    input['user_id'] = request.user.id
    input['selected'] = 1
    Note.objects.filter(user_id=input['user_id'], selected=1).update(selected=0)
    Note::create(input)
    return redirect('/notes/')


def edit(id):
    user_id = request.user.id
    page = 'notes'
    edit = true
    action = '/notes/update/' . id
    folders = FoldersController::getAll('notes')
    selectedFolder = Folder.objects.filter(user_id=user_id, page=page, selected=1).first()
    note = Note::findOrFail(id)
    return view('notes/content', context)


def update(id, Requests\CreateNoteRequest request):
    input = request.all()
    input['user_id'] = request.user.id
    note = Note.objects.filter(id=id, user_id=input['user_id').first()
    note.update(input)
    return redirect('/notes/')


def destroy(id):
    user_id = request.user.id
    note = Note.objects.filter(id=id, user_id=user_id).first()
    note.delete()
    return redirect('/notes/')
