<?php

namespace App\Http\Requests;
use App\Http\Requests\Request;

class CreateFavoriteRequest extends Request
{
    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    public function rules()
    {
        return [
            'folder_id' => 'integer|nullable',
            'name' => 'required|min:3|max:100',
	        'url' => 'required|min:5|url|max:500|nullable',
	        'description' => 'max:500',
	        'login' => 'max:30',
	        'root' => 'max:20',
	        'passkey' => 'max:20'
        ];
    }
}
