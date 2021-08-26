<div id="contact" class="col-sm-6 col-sm-push-6">
	{% if selectedContact %}
		{% include 'contacts/contact' %}
	{% endif %}
</div>

<div id="contacts" class="col-sm-3 col-sm-pull-3">
	<div class="section-title">
		Contacts
	</div>
	{% if contacts %}
		{% include 'contacts/list' %}
	{% else %}
	<ul class="list-group">
		<li class="list-group-item">No contacts selected.</li>
	</ul>
	{% endif %}
</div>
