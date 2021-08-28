

def index():
    user_id = request.user.id
    page = 'tasks'
    folders = FoldersController::getAll(page)
    selected_folders = Folder.objects.filter(user_id=user_id, page=page, selected=1, active=0).get()
    active_folder = Folder.objects.filter(user_id=user_id, page=page, active=1).first()

    if active_folder:
        active_folder_tasks = Task.objects.filter(folder_id=active_folder.id)
                .order_by('status')
                .order_by('title')
        for folder in selected_folders:
                selected_folder_tasks[folder.id] = Task.objects.filter('folder_id', folder.id)
                        .order_by('status')
                        .order_by('title')
                        .get()
        
    return view('tasks/content', context)


def activate(id):
    Folder.objects.filter(user_id=1, active=1).update(active=0)
    Folder.objects.filter(user_id=1, id=id).update(active=1)
    return redirect('/tasks/')


def status(id):
    task = Task::findOrFail(id)
    if task.status == 1:
        task.status = 0
    else: 
        task.status = 1
    task.save()
    return redirect('/tasks/')


def insert(Requests\CreateTaskRequest request):
    input = request.all()
    input['user_id'] = request.user.id
    Task::create(input)
    return redirect('/tasks/')


def edit(id):
    page = 'tasks'
    edit = true
    activeFolderId = id
    action = '/tasks/update/' . id
    folders = FoldersController::getAll(page)
    task = Task::findOrFail(id)
    return view('tasks/content', context)


def update(id, Requests\CreateTaskRequest request):
    input = request.all()
    input['user_id'] = request.user.id
    task = Task.objects.filter(id=id, user_id=input['user_id']).first()
    task.update(input)
    return redirect('/tasks/')


def clear(folder_id) :
    user_id = request.user.id
    Task.objects.filter(user_id=user_id, folder_id=folder_id, status=1).delete()
    return redirect('/tasks/')
