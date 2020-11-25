<!DOCTYPE html>
<html lang="en">
    <head>
	    <meta charset="UTF-8"content="">
	    <title>cloud-portal.com</title>
		<link rel="shortcut icon" href="/images/icons/portal-dark.ico">
		<link rel="apple-touch-icon" href="/images/icons/portal-dark.png" />
		<!-- set viewport for mobile devices -->
		<meta name="viewport" content="width = device-width, initial-scale = 1">
		<!-- bootstrap stylesheet -->
		<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
		<!-- app stylesheets -->
		<link rel="stylesheet" href="/css/app.css">
		<link rel="stylesheet" href="/css/layout-error.css">
		<!-- bootstrap javascript -->
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
		<script src="/js/javascript.js"></script>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

    </head>

	<body>
		<div class="container vertical-center">
            <div class="error-card">

                <div class="error-title">
                    {{ config('app.name') }}
                </div>

                <div class="error-code">
                    @yield('code'): @yield('message')
                </div>

                <div class="contact-message">
                    Please contact the site administrator if the problem persists.
                </div>

            </div>

        </div>
    </body>

</html>
