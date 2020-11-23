<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Contact extends Model
{
	public $timestamps = false;

	protected $fillable = [
		'user_id',
		'folder_id',
		'name',
		'company',
		'address',
		'phone1',
		'phone1_label',
		'phone2',
		'phone2_label',
		'phone3',
		'phone3_label',
		'email',
		'website',
		'map',
		'notes',
		'google_id'
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
