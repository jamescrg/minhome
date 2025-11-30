from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import CustomUser
from apps.folders.folders import get_task_folders, select_folder
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
    folders = get_task_folders(request)

    selected_folder = select_folder(request, "tasks")

    if selected_folder:
        tasks = Task.objects.filter(
            folder=selected_folder, is_recurring=False
        ).order_by("status", "title")
    else:
        tasks = Task.objects.filter(
            user=user, folder__isnull=True, is_recurring=False
        ).order_by("status", "title")

    context = {
        "page": "tasks",
        "folders": folders,
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

        # Check if this task was already recurring before the edit
        was_recurring = task.is_recurring

        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.title = task.title[0].upper() + task.title[1:]

            # Handle recurrence from the dropdown
            recurrence = form.cleaned_data.get("recurrence")
            if recurrence:
                task.is_recurring = True
                task.recurrence_type = recurrence

                # Set recurrence_day based on due_date
                if task.due_date:
                    if recurrence == "daily":
                        task.recurrence_day = None
                    elif recurrence == "monthly":
                        task.recurrence_day = task.due_date.day
                    elif recurrence == "weekly":
                        task.recurrence_day = task.due_date.weekday()
                    elif recurrence == "yearly":
                        task.recurrence_day = task.due_date.day
                        task.recurrence_month = task.due_date.month
            else:
                task.is_recurring = False
                task.recurrence_type = None
                task.recurrence_day = None
                task.recurrence_month = None

            task.save()

            # If task just became recurring, create the first instance immediately
            if task.is_recurring and not was_recurring:
                from datetime import date

                Task.objects.create(
                    user=task.user,
                    folder=task.folder,
                    title=task.title,
                    status=0,
                    due_date=task.due_date,
                    due_time=task.due_time,
                    parent_task=task,
                )
                task.last_generated = date.today()
                task.save(update_fields=["last_generated"])

            # If editing a recurring template, update the most recent incomplete instance
            elif task.is_recurring and was_recurring:
                latest_instance = (
                    Task.objects.filter(parent_task=task, status=0)
                    .order_by("-due_date")
                    .first()
                )
                if latest_instance:
                    latest_instance.folder = task.folder
                    latest_instance.title = task.title
                    latest_instance.due_time = task.due_time
                    latest_instance.save()

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

        # Hide recurrence field for generated instances (they have a parent_task)
        if task.parent_task:
            del form.fields["recurrence"]

        context = {
            "page": "tasks",
            "edit": True,
            "folders": folders,
            "selected_folder": selected_folder,
            "action": f"/tasks/{id}/edit",
            "task": task,
            "form": form,
        }

        return render(request, "tasks/content.html", context)


@login_required
def delete(request, id):
    """Delete a task.

    Args:
        id (int): A Task instance id
    """
    task = get_object_or_404(Task, pk=id, user=request.user)
    task.delete()
    return redirect("tasks")


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
        tasks = Task.objects.filter(user=request.user, folder__isnull=True, status=1)

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
