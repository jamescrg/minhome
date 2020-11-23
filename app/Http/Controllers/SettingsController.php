<?php namespace App\Http\Controllers;

use Request;

use App\Models\User;
use App\Models\GoogleClientHandler;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Auth;

class SettingsController extends Controller
{
	// checks current user auth status
	// if not auth, redirect to login
	public function __construct()
	{
		$this->middleware('auth');
	}

	public function index()
	{
		$data['page'] = 'settings';
		$user_id = Auth::user()->id;
		$data['user'] = User::findOrFail($user_id);
		return view('settings/content', $data);
	}

	public function googleLogin()
	{
		$data['page'] = 'settings';
		$gmail = Auth::user()->email;
		$client = GoogleClientHandler::newClient($gmail);
		GoogleClientHandler::getAuthCode($client);
	}

	public function googleStore()
	{
		$code = Request::input('code');
		$client = GoogleClientHandler::newClient(Auth::user()->email);
		$accessToken = GoogleClientHandler::getNewAccessToken($client, $code);
		$user_id = Auth::user()->id;
		$user = User::findOrFail($user_id);
		$user->google_token = $accessToken;
		$user->save();
		return redirect('/settings');
	}

	public function googleLogout()
	{
		$user_id = Auth::user()->id;
		$user = User::findOrFail($user_id);
		$user->google_token = null;
		$user->save();
		return redirect('/settings');
	}

}
