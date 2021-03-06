<?php

namespace App\Http\Requests;
use App\Http\Requests\Request;

class CreateContactRequest extends Request
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
            'name' => 'required|min:2',
            'phone1' => 'max:20',
            'phone2' => 'max:20',
            'phone3' => 'max:20',
            'email' => 'max:30|email|nullable',
            'notes' => 'max:500'
        ];
    }
}
