from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import CustomUser
from apps.folders.folders import get_task_folders, select_folder, get_breadcrumbs, get_folder_tree
from apps.folders.models import Folder
from apps.tasks.forms import TaskForm
from apps.tasks.models import Task


@login_required
def index(request):
    """Display a list of folders and one or more lists of tasks.

    Notes:
        * Always displays folders.
        * If a folder is selected, displays the tasks for that folder.
        * Allows the display of mulitple task folders.
        * Task folders are informally called "lists" but are part of the consolidated
          folder system for the whole site.
    """

    user = request.user
    selected_folder = select_folder(request, "tasks")
    
    # Get folder tree starting from selected folder
    folder_tree = get_folder_tree(request, "tasks", selected_folder)

    if selected_folder:
        # Get tasks from selected folder and all its descendants
        folder_ids = [selected_folder.id] + [f.id for f in selected_folder.get_descendants()]
        tasks = Task.objects.filter(folder__id__in=folder_ids).order_by("status", "title")
    else:
        tasks = Task.objects.filter(
            user=user, folder__isnull=True).order_by("status", "title")

    context = {
        "page": "tasks",
        "folder_tree": folder_tree,
        "selected_folder": selected_folder,
        "tasks": tasks,
    }

    return render(request, "tasks/content.html", context)


@login_required
def status(request, id, origin="tasks"):
    """Update a task status to complete / not complete

    Args:
        id (int): a task id
        origin (str): the page from which the request originated and should return

    Notes:
        Tasks may be updated from the home or the task page,
        in which case, the user should be returned to the page of origin.
    """

    task = get_object_or_404(Task, pk=id)
    if task.status == 1:
        task.status = 0
    else:
        task.status = 1
    task.save()
    return redirect(origin)


@login_required
def add(request):
    """Add a new task.

    Notes:
        GET: There is no get method for this view.
             The task form is always visible via "index".
        POST: Add task to database.
    """

    if request.method == "POST":
        task = Task()

        task.user = request.user
        task.title = request.POST.get("title")
        task.title = task.title[0].upper() + task.title[1:]

        try:
            folder = Folder.objects.filter(pk=request.POST.get("folder_id")).get()
            task.folder = folder
            task.save()

        except ValueError:
            task.save()

        return redirect("tasks")


@login_required
def edit(request, id):
    """Edit a task.

    Args:
        id (int): A Task instance id

    Notes:
        GET: Display task edit form.
        POST: Update task in database.
    """

    user = request.user

    if request.method == "POST":
        try:
            task = Task.objects.filter(pk=id).get()
        except ObjectDoesNotExist:
            raise Http404("Record not found.")

        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.title = task.title[0].upper() + task.title[1:]
            task.save()

        return redirect("tasks")

    else:
        task = get_object_or_404(Task, pk=id)
        folders = get_task_folders(request)
        try:
            selected_folder = folders.filter(id=task.folder.id).get()
        except AttributeError:
            selected_folder = None

        if selected_folder:
            form = TaskForm(instance=task, initial={"folder": selected_folder.id})
        else:
            form = TaskForm(instance=task)

        form.fields["folder"].queryset = folders

        context = {
            "page": "tasks",
            "edit": True,
            "folders": folders,
            "selected_folder": selected_folder,
            "action": f"/tasks/{id}/edit",
            "form": form,
        }

        return render(request, "tasks/content.html", context)


@login_required
def clear(request):
    """Delete all completed tasks in the active folder.

    Args:
        folder_id (int): the folder where tasks should be deleted
    """

    selected_folder = select_folder(request, "tasks")

    if selected_folder:
        tasks = Task.objects.filter(folder=selected_folder, status=1)
    else:
        tasks = Task.objects.filter(
            user=request.user, folder__isnull=True, status=1)

    for task in tasks:
        task.delete()

    return redirect("/tasks/")


@login_required
def add_editor(request, folder_id, user_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    user = get_object_or_404(CustomUser, pk=user_id)
    folder.editors.add(user)
    folder.save()
    return redirect("/tasks/")


@login_required
def remove_editor(request, folder_id, user_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    user = get_object_or_404(CustomUser, pk=user_id)
    folder.editors.remove(user)
    folder.save()
    return redirect("/tasks/")
