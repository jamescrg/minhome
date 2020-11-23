<?php

namespace App\Http\Controllers;

use App\Http\Requests;
use App\Http\Controllers\Controller;
use App\Models\Folder;
use App\Http\Controllers\FoldersController;
use App\Models\Favorite;
use DB;
use Auth;


class FavoritesController extends Controller
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
		$data['page'] = 'favorites';
		$data['folders'] = FoldersController::getAll($data['page']);
		$data['selectedFolder'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'selected' => 1])->first();
		if ( $data['selectedFolder'] == null ) {
			$selectedFolder = 0;
		} else {
			$selectedFolder = $data['selectedFolder']->id;
		}
		$data['favorites'] = Favorite::where([ 'user_id' => $user_id, 'folder_id' => $selectedFolder])
							->orderBy('name')->get();
		return view('favorites/content', $data);
	}

	public function create($id)
	{
		$user_id = Auth::user()->id;
		$data['page'] = 'favorites';
		$data['action'] = '/favorites';
		$data['edit'] = false;
		$data['selectedFolderId'] = $id;
		$data['selectedFolder'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'selected' => 1])->first();
		$data['folders'] = FoldersController::getAll('favorites');
		$data['favorite'] = new Favorite;
		$data['favorite']->folder_id = $id;
		return view('favorites/content', $data);
	}

	public function store(Requests\CreateFavoriteRequest $request)
	{
		// validation runs first
		$input = $request->all();
		$input['user_id'] = Auth::user()->id;
		Favorite::create($input);
		return redirect('favorites');
	}

	public function edit($id)
	{
		$user_id = Auth::user()->id;
		$data['page'] = 'favorites';
		$data['edit'] = true;
		$data['action'] = '/favorites/update/' . $id;
		$data['folders'] = FoldersController::getAll($data['page']);
		$data['selectedFolder'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'selected' => 1])->first();
		$data['favorite'] = Favorite::findOrFail($id);
		return view('favorites/content', $data);
	}

	public function update($id, Requests\CreateFavoriteRequest $request)
	{
		$input = $request->all();
		$input['user_id'] = Auth::user()->id;
		$favorite = Favorite::where(['id' => $id, 'user_id' => $input['user_id']])->first();
		$favorite->update($input);
		return redirect('favorites');
	}

	public function home($id)
	{
		$user_id = Auth::user()->id;
		$favorite = Favorite::where(['id' => $id, 'user_id' => $user_id])->first();
		if ($favorite->home_rank > 0) {
			$favorite->home_rank = 0;
		} else {
			$favorite->home_rank = 1;
		}
		$favorite->save();
		return redirect('favorites');
	}

	public function destroy($id)
	{
		$user_id = Auth::user()->id;
		$favorite = Favorite::where(['id' => $id, 'user_id' => $user_id])->first();
		$favorite->delete();
		return redirect('favorites');
	}
}
