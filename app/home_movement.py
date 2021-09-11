

def horizontal(folder):
    # get the folder to be moved
    # identify the column to which it belongs
    origin_folder = folder
    origin_column = origin_folder.home_column

    # make sure the folders are sequential and ajdacent
    folders = Folder.objects.filter(user_id=user_id, home_column=origin_column) 
    folders = folders.order_by('home_rank')
    count = 1
    for folder in folders:
        folder.home_rank = count
        folder.save()
        count += 1

    # identify the origin rank as modified by the sequence operation
    origin_folder = get_object_or_404(Folder, pk=id)
    origin_rank = origin_folder.home_rank

    # identify the destination rank
    if direction == 'up':
        destination_rank = origin_rank - 1
    if direction == 'down':
        destination_rank = origin_rank + 1

    # identify the folder to be displaced
    try:
        displaced_folder = Folder.objects.filter(
                user_id=user_id, 
                home_column=origin_column, home_rank=destination_rank).get() 
    except Folder.DoesNotExist:
        raise Http404('No folder matches the given query.')

    # if a folder is being displaced, move it and the original folder
    # otherwise, we are at the end of the column, make no changes
    origin_folder.home_rank = destination_rank
    origin_folder.save()

    if displaced_folder:
        displaced_folder.home_rank = origin_rank
        displaced_folder.save()

def vertical(folder):
    # get the folder to be moved, along with its column and rank
    origin_folder = folder
    origin_column = origin_folder.home_column
    origin_rank = origin_folder.home_rank

    if direction == 'left' and origin_column > 1:
        destination_column = origin_column - 1
    elif direction == 'right' and origin_column < 4: 
        destination_column = origin_column + 1
    else:
        destination_column = destination_column

    # move over origin folder to destination column
    origin_folder.home_column = destination_column
    origin_folder.save()
