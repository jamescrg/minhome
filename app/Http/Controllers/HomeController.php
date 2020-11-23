<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Http\Requests;
use App\Http\Controllers\Controller;
use App\Models\Folder;
use App\Models\Favorite;
use App\Models\Task;
use Auth;
use Input;

class HomeController extends Controller
{

	// checks current user auth status
	// if not auth, redirect to login
	public function __construct()
	{
		$this->middleware('auth');
	}

	public function index()
	{
		$user_id = Auth::user()->id;
        $data['user_id'] = $user_id;
		$data['page'] = 'home';
        $data['searchEngine'] = 'google.com/search';
        // if ( $user_id == 1 ) $data['searchEngine'] = 'duckduckgo.com';
		$data['folders'] = Folder::where('user_id', $user_id)->where('home_column', '>', '0')->orderBy('home_rank')->get();
		$data['favorites'] = Favorite::where('user_id', $user_id)->where('home_rank', '>', '0')->orderBy('home_rank')->get();
        $data['tasks'] = Task::where('user_id', $user_id)->where('folder_id', '346')->orderBy('title', 'asc')->get();
		return view('home/content', $data);
	}

	public function folder($id, $direction){

			$user_id = Auth::user()->id;

			// if the stack order is being changed
			if ($direction == 'up' || $direction == 'down') {

				// get the folder to be moved
				// identify the column to which it belongs
				$originFolder = Folder::findOrFail($id);
				$originColumn = $originFolder->home_column;

				// make sure the folders are sequential and adjacent
				$folders = Folder::where(['user_id' => $user_id, 'home_column' => $originColumn])->orderBy('home_rank', 'asc')->get();
				$count = 1;
				foreach ($folders as $folder){
					$folder->home_rank = $count;
					$folder->save();
					$count++;
				}

				// identify the origin rank as modified by the sequence operation
				$originFolder = Folder::findOrFail($id);
				$originRank = $originFolder->home_rank;

				// identify the destination rank
				if ($direction == 'up') $destinationRank = $originRank - 1;
				if ($direction == 'down') $destinationRank = $originRank + 1;

				// identify the folder to be displaced
				$displacedFolder = Folder::where([ 'user_id' => $user_id, 'home_column' => $originColumn, 'home_rank' => $destinationRank ])
					->first();

				// if a folder is being displaced, move it and the original folder
				// otherwise, we are at the end of the column, make no changes
				$originFolder->home_rank = $destinationRank;
				$originFolder->save();

				if ($displacedFolder) {
					$displacedFolder->home_rank = $originRank;
					$displacedFolder->save();
				}
			}

			// if the column is being changed
			if ($direction == 'left' || $direction == 'right') {

				// get the folder to be moved, along with its column and rank
				$originFolder = Folder::findOrFail($id);
				$originColumn = $originFolder->home_column;
				$originRank = $originFolder->home_rank;

				if ( $direction == 'left' && $originColumn > 1 ) {
					$destinationColumn = $originColumn - 1;
				} else if ($direction == 'right' && $originColumn < 4 ) {
					$destinationColumn = $originColumn + 1;
				} else {
					return redirect('home');
				}

				// move over origin folder to destination column
				$originFolder->home_column = $destinationColumn;
				$originFolder->save();

			}

		    return redirect('home');

		}

		public function favorite($id, $direction){

			$user_id = Auth::user()->id;

			// get the favorite to be moved
			$originFavorite = Favorite::findOrFail($id);
			$folder_id = $originFavorite->folder_id;

			// make sure the favorites are sequential and adjacent
			$favorites =    Favorite::where('user_id', $user_id)
							->where('folder_id', $folder_id)
							->where('home_rank', '>', 0)
							->orderBy('home_rank', 'asc')->get();
			$count = 1;
			foreach ($favorites as $favorite){
				$favorite->home_rank = $count;
				$favorite->save();
				$count++;
			}

			// identify the origin rank as modified by the sequence operation
			$originFavorite = Favorite::findOrFail($id);
			$originRank = $originFavorite->home_rank;

			// identify the destination rank
			if ($direction == 'up') $destinationRank = $originRank - 1;
			if ($direction == 'down') $destinationRank = $originRank + 1;

			// identify the favorite to be displaced
			$displacedFavorite = Favorite::where([ 'user_id' => $user_id, 'folder_id' => $folder_id, 'home_rank' => $destinationRank ])
				->first();

			// if a favorite is being displaced, move it and the original favorite
			// otherwise, we are at the end of the column, make no changes
			$originFavorite->home_rank = $destinationRank;
			$originFavorite->save();

			if ($displacedFavorite) {
				$displacedFavorite->home_rank = $originRank;
				$displacedFavorite->save();
			}

		    return redirect('home');
	}
}
