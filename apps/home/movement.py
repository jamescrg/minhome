from apps.folders.models import Folder


def sequence(user, column):
    folders = Folder.objects.filter(user=user, page="favorites", home_column=column)
    folders = folders.order_by("home_rank")
    count = 1
    for folder in folders:
        folder.home_rank = count
        folder.save()
        count += 1
    return folders
