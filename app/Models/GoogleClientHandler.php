<?php 

namespace App\Models;

use Request;
use Google_Client;

class GoogleClientHandler
{

	public static function newClient($email = null)
	{
		$clientId = env('GOOGLE_CLIENT_ID', false);
		$clientSecret = env('GOOGLE_CLIENT_SECRET', false);
		$redirectURI = 'https://' . Request::server('HTTP_HOST') . '/settings/google/store';
		$client = new Google_Client();
		$client->setApplicationName('cloud-portal');
		$client->setClientId($clientId);
		$client->setClientSecret($clientSecret);
		$client->setRedirectUri($redirectURI);
		$client->setAccessType('offline');
		$client->setApprovalPrompt('force');
		if ($email != null) $client->setLoginHint($email);
		$client->setScopes(array('https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/contacts'));
		return $client;
	}

	public static function setAccessToken($client, $accessToken)
	{
		$client->setAccessToken($accessToken);
		$isExpired = $client->isAccessTokenExpired();
		if ( $isExpired ) {
			$refreshToken = $client->getRefreshToken();
			$client->refreshToken($refreshToken);
		}
		return $client;
	}

	public static function getAuthCode($client)
	{
		$authUrl = $client->createAuthUrl();
		header('Location: ' . $authUrl);
		die();
	}

	public static function getNewAccessToken($client, $authCode)
	{
		$client->authenticate($authCode);
		$accessToken = $client->getAccessToken($client);
		return $accessToken;
	}
}
