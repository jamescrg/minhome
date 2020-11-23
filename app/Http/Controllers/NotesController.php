<?php

namespace App\Http\Controllers;

use App\Http\Requests;
use App\Http\Controllers\Controller;
use App\Models\Folder;
use App\Http\Controllers\FoldersController;
use App\Models\Note;
use DB;
use Auth;


class NotesController extends Controller
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
		$data['page'] = 'notes';
		$data['folders'] = FoldersController::getAll($data['page']);
		$data['selectedFolder'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'selected' => 1])->first();
		if ( $data['selectedFolder']) {
			$data['notes'] = Note::where([ 'user_id' => $user_id, 'folder_id' => $data['selectedFolder']->id ])->orderBy('subject')->get();
		} else {
			$data['notes'] = Note::where('user_id', $user_id)->where('folder_id', 0)->orderBy('subject')->get();
		}

		$data['selectedNote'] =  Note::where(['user_id' => $user_id, 'selected' => 1])->first();
		//dd($data['selectedFolder']);
		return view('notes/content', $data);
	}

	public function show($id)
	{
		$user_id = Auth::user()->id;
		Note::where(['user_id' => $user_id, 'selected' => 1])->update(['selected' => 0]);
		Note::where(['id' => $id, 'user_id' => $user_id])->update(['selected' => 1]);
		return redirect('notes');
	}

	public function create($id)
	{
		$user_id = Auth::user()->id;
		$data['page'] = 'notes';
		$data['action'] = '/notes';
		$data['edit'] = false;
		$data['selectedFolderId'] = $id;
		$data['selectedFolder'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'selected' => 1])->first();
		$data['folders'] = FoldersController::getAll('notes');
		$data['note'] = new Note;
		$data['note']->folder_id = $id;
		return view('notes/content', $data);
	}

	public function store(Requests\CreateNoteRequest $request)
	{
		//validation runs first
		$input = $request->all();
		$input['user_id'] = Auth::user()->id;
		$input['selected'] = 1;
		Note::where(['user_id' => $input['user_id'], 'selected' => 1])->update(['selected' => 0]);
		Note::create($input);
		return redirect('notes');
	}

	public function edit($id)
	{
		$user_id = Auth::user()->id;
		$data['page'] = 'notes';
		$data['edit'] = true;
		$data['action'] = '/notes/update/' . $id;
		$data['folders'] = FoldersController::getAll('notes');
		$data['selectedFolder'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'selected' => 1])->first();
		$data['note'] = Note::findOrFail($id);
		return view('notes/content', $data);
	}

	public function update($id, Requests\CreateNoteRequest $request)
	{
		$input = $request->all();
		$input['user_id'] = Auth::user()->id;
		$note = Note::where(['id' => $id, 'user_id' => $input['user_id']])->first();
		$note->update($input);
		return redirect('notes');
	}

	public function destroy($id)
	{
		$user_id = Auth::user()->id;
		$note = Note::where(['id' => $id, 'user_id' => $user_id])->first();
		$note->delete();
		return redirect('notes');
	}
}
