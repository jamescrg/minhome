

# get the favorite to be moved
origin_favorite = get_model_or_404(Favorite, pk=id)
folder_id = origin_favorite.folder_id

# make sure the favorites are sequential and adjacent
favorites = Favorites.objects.filter(user_id=user_id, folder_id=folder_id,home_rank__gt=0)
favorites = favorites.orderBy('home_rank')

count = 1
for favorite in favorites:
    favorite.home_rank = count
    favorite.save()
    count++

# identify the origin rank as modified by the sequence operation
origin_favorite = get_model_or_404(Favorite, pk=id)
origin_rank = origin_favorite.home_rank

# identify the destination rank
if direction == 'up':
    destination_rank = originRank - 1
if direction == 'down':
    destination_rank = originRank + 1

# identify the favorite to be displaced
displaced_favorite = Favorite.objects.filter(user_id=user_id, 
        folder_id=folder_id, home_rank=destination_rank).first()

# if a favorite is being displaced, move it and the original favorite
# otherwise, we are at the end of the column, make no changes
origin_favorite.home_rank = destination_rank
origin_favorite.save()

if displaced_favorite:
    displaced_favorite.home_rank = origin_rank
    displaced_favorite.save()

return redirect('/home/')
