<?php

namespace App\Http\Controllers;

use App\Http\Requests;
use App\Http\Controllers\Controller;
use App\Http\Controllers\FoldersController;
use App\Models\Folder;
use App\Models\Task;
use DB;
use Auth;

class TasksController extends Controller
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
		$data['page'] = 'tasks';
		$data['folders'] = FoldersController::getAll($data['page']);
		$data['selectedFolders'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'selected' => 1, 'active' => 0])->get();
		$data['activeFolder'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'active' => 1])->first();
		if ( $data['activeFolder'] != null ) {
			$data['activeFolderTasks'] = Task::where('folder_id', $data['activeFolder']->id)
				->orderBy('status')
				->orderBy('title', 'asc')->get();
		}
		foreach ($data['selectedFolders'] as $folder) {
			$data['selectedFolderTasks'][$folder->id] = Task::where('folder_id', $folder->id)
				->orderBy('status')
				->orderBy('title', 'asc')
				->get();
		}
		return view('tasks/content', $data);
	}

	public function activate($id)
	{
		Folder::where('user_id', 1)->where('active', 1)->update(['active' => 0]);
		Folder::where('user_id', 1)->where('id', $id)->update(['active' => 1]);
		return redirect('tasks');
	}

	public function status($id)
	{
		$task = Task::findOrFail($id);
		if ($task->status == 1) {
			$task->status = 0;
		} else {
			$task->status = 1;
		}
		$task->save();
		return redirect('tasks');
	}

	public function store(Requests\CreateTaskRequest $request)
	{
		$input = $request->all();
		$input['user_id'] = Auth::user()->id;
		Task::create($input);
		return redirect('tasks');
	}

	public function edit($id)
	{
		$data['page'] = 'tasks';
		$data['edit'] = true;
		$data['activeFolderId'] = $id;
		$data['action'] = '/tasks/update/' . $id;
		$data['folders'] = FoldersController::getAll($data['page']);
		$data['task'] = Task::findOrFail($id);
		return view('tasks/content', $data);
	}

	public function update($id, Requests\CreateTaskRequest $request)
	{
		$input = $request->all();
		$input['user_id'] = Auth::user()->id;
		$task = Task::where(['id' => $id, 'user_id' => $input['user_id']])->first();
		$task->update($input);
		return redirect('tasks');
	}

	public function clear($folder_id) {
		$user_id = Auth::user()->id;
		Task::where(['user_id' => $user_id, 'folder_id' => $folder_id, 'status' => 1])->delete();
		return redirect('tasks');
	}

}
