<!DOCTYPE html>
<html lang="en">
	<head>
	    <meta charset="UTF-8"content="">
	    <title>cloud-portal.com | {{$page}}</title>
		<link rel="shortcut icon" href="/images/icons/portal-dark.ico">
		<link rel="apple-touch-icon" href="/images/icons/portal-dark.png" />
		<!-- set viewport for mobile devices -->
		<meta name="viewport" content="width = device-width, initial-scale = 1">
		<!-- bootstrap stylesheet -->
		<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
		<!-- app stylesheets -->
		<link rel="stylesheet" href="/css/app.css">
		<link rel="stylesheet" href="/css/layout-app.css">
		<link rel="stylesheet" href="/css/forms.css">
		<link rel="stylesheet" href="/css/folders.css">
		<link rel="stylesheet" href="/css/{{$page}}.css">
		<!-- bootstrap javascript -->
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
		<script src="/js/javascript.js"></script>
	</head>
	<body>
	<div id="wrapper">
		@include('nav')
		<div class="container" id="content">
			@yield('content')
		</div>
		<div id="footer">
		@include('footer')
		</div>
	</div>
	</body>
</html>
