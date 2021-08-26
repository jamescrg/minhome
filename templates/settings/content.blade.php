{% extends 'layout.html' %}
{% block content %}
	<p>Settings</p>
	{% if user.google_token == null %}
		<a href="/settings/google/login">Log in to Google Apps</a>
	{% else %}
		<a href="/settings/google/logout">Log out of Google Apps</a>
	{% endif %}
{% endblock content %}
