{% extends 'layout.html' %}
{% block content %}
<div class="row">

	{% if  isset(edit)  %}
		{% include 'notes/create' %}
	{% else %}
		{% include 'notes/notes' %}
	{% endif %}

	<div id="folders" class="col-sm-3 col-sm-pull-9">
		{% include 'folders/list' %}
	</div>


</div>
{% endblock content %}
