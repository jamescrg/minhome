<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Http\Requests;
use App\Http\Controllers\Controller;
use App\Models\Favorite;
use App\Models\Contact;
use App\Models\Note;
use DB;
use Auth;

class SearchController extends Controller
{
	// checks current user auth status
	// if not auth, redirect to login
	public function __construct()
	{
		$this->middleware('auth');
	}

	public function index()
	{
		$data['page'] = 'search';
		$data['results'] = false;
		return view('search/content', $data);
	}

	public function nothing()
	{
		$data['page'] = 'search';
		$data['results'] = true;
		return view('search/content', $data);
	}

	public function search(Request $request)
	{
		$data['page'] = 'search';
		$data['results'] = true;

		$user_id = Auth::user()->id;
		$text = $request->searchText;

		$query =    'SELECT favorites.id,
							favorites.folder_id,
							favorites.name as favoriteName,
							url, description, login, root, passkey,
							folders.name as folderName
					FROM favorites
					LEFT JOIN folders	ON favorites.folder_id = folders.id
					WHERE favorites.user_id = "'. $user_id .'" AND
						(
						favorites.name LIKE "%'. $text .'%"
						OR url LIKE "%'. $text .'%"
						OR description LIKE "%'. $text .'%"
						)';

		$data['favorites'] = DB::select($query);

		$query =    'SELECT
							contacts.id as contactId,
							folder_id,
							contacts.name as contactName,
							company, phone1, email, LEFT(notes, 70),
							folders.id as foldId,
							folders.name as contactFolder
					FROM contacts
					LEFT JOIN folders
					ON folder_id = folders.id
					WHERE contacts.user_id = "'. $user_id .'"
						AND (contacts.name LIKE "%'. $text .'%"
						OR company LIKE "%'. $text .'%"
						OR address LIKE "%'. $text .'%"
						OR phone1 LIKE "%'. $text .'%"
						OR phone2 LIKE "%'. $text .'%"
						OR phone3 LIKE "%'. $text .'%"
						OR email LIKE "%'. $text .'%"
						OR website LIKE "%'. $text .'%"
						OR notes LIKE "%'. $text .'%"
						)';
		$data['contacts'] = DB::select($query);

		$query = 'SELECT notes.id as noteId, subject, folder_id, LEFT(note, 50) as note, folders.name
						FROM notes
						LEFT JOIN folders
						ON folder_id = folders.id
						WHERE notes.user_id = "'. $user_id .'"
						AND (subject LIKE "%'. $text .'%"
						OR note LIKE "%'. $text .'%")';
		$data['notes'] = DB::select($query);

		return view('search/content', $data);
	}
}
