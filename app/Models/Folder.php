<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Folder extends Model
{
    public $timestamps = false;

	protected $fillable = [
		'user_id',
		'page',
		'name',
		'home',
		'home_column',
		'home_rank',
		'selected',
		'active'
	];

	public function user()
	{
		return $this->belongsTo('App\User');
	}

}
