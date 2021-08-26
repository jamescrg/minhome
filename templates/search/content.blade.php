{% extends 'layout.html' %}
{% block content %}
	<div class="row">
		{% include 'search/form' %}
		{% if results %}
			{% include 'search/results' %}
		{% endif %}
	</div>
{% endblock content %}
