<?php 

namespace App\Models;

use App\Models\GoogleClientHandler;
use Auth;
use Google_Service_PeopleService;
use Google_Service_PeopleService_Person;
use Google_Service_PeopleService_Name;
use Google_Service_PeopleService_EmailAddress;
use Google_Service_PeopleService_PhoneNumber;

class GoogleContactHandler
{

	private static function generateClient()
	{
		$accessToken = Auth::user()->google_token;
		$client = GoogleClientHandler::newClient();
		$client = GoogleClientHandler::setAccessToken($client, $accessToken);
		return $client;
	}

	public static function add($contact)
	{

        // get an authenticated client, then create a people service connection
		$client = self::generateClient();
		$user_email = Auth::user()->email;
        $service = new Google_Service_PeopleService($client);

        // create a new person object
        $person = new Google_Service_PeopleService_Person();

        // set the person's name
        $name = new Google_Service_PeopleService_Name();
        $name->setUnstructuredName($contact->name);
        $person->setNames($name);

        // set the person's email
        if ($contact->email) {
            $email1 = new Google_Service_PeopleService_EmailAddress();
            $email1->setValue($contact->email);
            $person->setEmailAddresses($email1);
        }

        // set multiple phone numbers as an array
        $phoneNumbers = [];

        if ($contact->phone1) {
            $phone1 = new Google_Service_PeopleService_PhoneNumber();	
            $phone1->setValue($contact->phone1);
            $phone1->setType($contact->phone1_label);
            array_push($phoneNumbers, $phone1);
        }

        if ($contact->phone2) {
            $phone2 = new Google_Service_PeopleService_PhoneNumber();	
            $phone2->setValue($contact->phone2);
            $phone2->setType($contact->phone2_label);
            array_push($phoneNumbers, $phone2);
        }

        if ($contact->phone3) {
            $phone3 = new Google_Service_PeopleService_PhoneNumber();	
            $phone3->setValue($contact->phone3);
            $phone3->setType($contact->phone3_label);
            array_push($phoneNumbers, $phone3);
        }

        $person->setPhoneNumbers($phoneNumbers);

        // execute the api call with the person
        $googleContact = $service->people->createContact($person);

        // capture and return the record id number in the google database
        $googleResourceName = $googleContact->resourceName;
        $googleContactId = str_replace('people/', '', $googleResourceName);
        return $googleContactId;

	}

	public static function delete($googleContactId)
	{
		$client = self::generateClient();
		$user_email = Auth::user()->email;

        // get an authenticated client, then create a people service connection
        $service = new Google_Service_PeopleService($client);
        
        $resourceName = 'people/' . $googleContactId; 

        // execute the deletion method
        $result = $service->people->deleteContact($resourceName);
	}

}




