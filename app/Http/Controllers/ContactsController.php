<?php

namespace App\Http\Controllers;

use DB;
use Auth;

use App\Http\Controllers\Controller;
use App\Http\Controllers\FoldersController;

use App\Http\Requests;

use App\Models\Folder;
use App\Models\Contact;
use App\Models\GoogleContactHandler;

class ContactsController extends Controller
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
		$data['page'] = 'contacts';
		$data['folders'] = FoldersController::getAll($data['page']);
		$data['selectedFolder'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'selected' => 1])->first();
		if ($data['selectedFolder']) {
			$data['contacts'] = Contact::where([ 'user_id' => $user_id, 'folder_id' => $data['selectedFolder']->id ])->orderBy('name')->get();
		} else {
			$data['contacts'] = Contact::where('user_id', $user_id)->where('folder_id', 0)->orderBy('name')->get();
		}
		$data['selectedContact'] = Contact::where(['user_id' => $user_id, 'selected' => 1])->first();
		return view('contacts/content', $data);
	}

	public function show($id)
	{
		$user_id = Auth::user()->id;
		Contact::where(['user_id' => $user_id, 'selected' => 1])->update(['selected' => 0]);
		Contact::where(['id' => $id, 'user_id' => $user_id])->update(['selected' => 1]);
		return redirect('contacts');
	}

	public function create($id)
	{
		$user_id = Auth::user()->id;
		$data['page'] = 'contacts';
		$data['action'] = '/contacts';
		$data['edit'] = false;
		$data['activeFolderId'] = $id;
		$data['folders'] = FoldersController::getAll('contacts');
		$data['selectedFolder'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'selected' => 1])->first();
		$data['contact'] = new Contact;
		$data['contact']->folder_id = $id;
		return view('contacts/content', $data);
	}

	public function store(Requests\CreateContactRequest $request)
	{
		// validation runs first
        
        // capture the input from the user
		$input = $request->all();

        // add the user's id
		$input['user_id'] = Auth::user()->id;

        // make the contact that has been submitted the selected contact
		$input['selected'] = 1;

        // de-select the prior selected contact
		Contact::where(['user_id' => $input['user_id'], 'selected' => 1])->update(['selected' => 0]);

        // insert the new contact into the database
		Contact::create($input);

		// if google account is logged in
		// add to google contacts
		if (Auth::user()->google_token) {

            // retrieve the most recent contact id (the one just added above)
			$contactId = Contact::where('user_id', Auth::user()->id)->max('id');

            // retrieve the contact
			$contact = Contact::findOrFail($contactId);

            // submit the contact to google and save the google_id as a property of the contact
			$contact->google_id = GoogleContactHandler::add($contact);

            // save the contact with the google_id
			$contact->save();
		}

		return redirect('contacts');
	}

	public function edit($id)
	{
		$user_id = Auth::user()->id;
		$data['page'] = 'contacts';
		$data['edit'] = true;
		$data['action'] = '/contacts/update/' . $id;
		$data['folders'] = FoldersController::getAll('contacts');
		$data['selectedFolder'] = Folder::where(['user_id' => $user_id, 'page' => $data['page'], 'selected' => 1])->first();
		$data['contact'] = Contact::findOrFail($id);
		return view('contacts/content', $data);
	}

	public function update($id, Requests\CreateContactRequest $request)
	{

		echo 'update contact';
		$input = $request->all();
		$input['user_id'] = Auth::user()->id;
		$contact = Contact::where(['id' => $id, 'user_id' => $input['user_id']])->first();

		// update contact in database
		$contact->update($input);

		if (Auth::user()->google_token) {

			// delete from google contacts if has contact id
            if ($contact->google_id) {
                GoogleContactHandler::delete($contact->google_id);
            }

			// add to google contacts
			$input['google_id'] = GoogleContactHandler::add($contact);

			// update contact in database again (with google_id if logged in)
			$contact->update($input);
		}

		return redirect('contacts');
	}

	public function destroy($id)
	{
		$user_id = Auth::user()->id;
		$contact = Contact::where(['id' => $id, 'user_id' => $user_id])->first();
		if (Auth::user()->google_token) {

            if ($contact->google_id) {
                GoogleContactHandler::delete($contact->google_id);
            }
		}
		$contact->delete();
		return redirect('contacts');
	}
}
