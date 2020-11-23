<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Http\Requests;
use App\Http\Controllers\Controller;
use App\Models\Folder;
use DB;
use Auth;

class FoldersController extends Controller
{
	// checks current user auth status
	// if not auth, redirect to login
	public function __construct()
	{
		$this->middleware('auth');
	}

    // get all folders for page
	public static function getAll($page)
	{
		$user_id = Auth::user()->id;
		$folders = Folder::where([ 'user_id' => $user_id, 'page' => $page ])->orderBy('name')->get();
		return $folders;
	}

	// get all folders for page
	public function select($id, $page)
	{
		$user_id = Auth::user()->id;

		if ( $page != 'tasks' ) {
			Folder::where(['page' => $page, 'user_id' => $user_id])->update(['selected' => 0]);
			if ( $id > 0 ) {
				$folder = Folder::where(['id' => $id, 'user_id' => $user_id])->first();
				$folder->selected = 1;
				$folder->save();
			}
		}
		if ( $page == 'tasks' ) {
			$folder = Folder::findOrFail($id);
			if ($folder->active == 1 ) $folder->active = 0;
			if ($folder->selected == 1) {
				$folder->selected = 0;
			} else {
				$folder->selected = 1;
			}
			$folder->save();
		}
		return redirect($page);
	}

	public function activate($id, $page)
	{
		if ( $page == 'tasks' ) {
			//
		}
	}

	public function store($page, Requests\CreateFolderRequest $request)
	{
		// validation runs first
		$input = $request->all();
		$input['user_id'] = Auth::user()->id;
		$input['page'] = $page;
		Folder::create($input);
		return redirect($page);
	}

	public function update($id, $page, Requests\CreateFolderRequest $request)
	{
		$input = $request->all();
		$input['user_id'] = Auth::user()->id;
		$folder = Folder::where(['id' => $id, 'user_id' => $input['user_id']])->first();
		$folder->update($input);
		return redirect($page);
	}

	public function home($id, $page)
	{
		$user_id = Auth::user()->id;
		$folder = Folder::where(['id' => $id, 'user_id' => $user_id])->first();
		if ($folder->home_column > 0) {
			$folder->home_column = 0;
			$folder->home_rank = 0;
		} else {
			$folder->home_column = 4;
			$maxRank = Folder::where([ 'user_id' => $user_id, 'home_column' => 4 ])->max('home_rank');
			$folder->home_rank = $maxRank + 1;
		}
		$folder->save();
		return redirect($page);
	}

	public function destroy($id, $page)
	{
		$user_id = Auth::user()->id;
		$folder = Folder::where(['id' => $id, 'user_id' => $user_id])->first();
		$folder->delete();
		return redirect($page);
	}
}
