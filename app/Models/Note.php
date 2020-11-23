<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Note extends Model
{
	public $timestamps = false;

	protected $fillable = [
		'user_id',
		'folder_id',
		'subject',
		'note'
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
