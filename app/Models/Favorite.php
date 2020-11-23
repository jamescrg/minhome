<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Favorite extends Model
{
	public $timestamps = false;

	protected $fillable = [
		'user_id',
		'folder_id',
		'home',
		'home_rank',
		'name',
		'url',
		'description',
		'login',
		'root',
		'passkey'
	];

	public function user()
	{
		return $this->belongsTo('App\User');
	}

	public function folder()
	{
		return $this->belongsTo('App\Folder');
	}
}
