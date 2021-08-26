
<div class="section-title">
	{{ selectedContact.name }}
</div>

<div class="contact">

	<div class="contact-item">
		{{ selectedContact.name }} <br>
		{% if selectedContact.company %} 
      {{ selectedContact.company }} 	<br> 
    {% endif %}
		{% if selectedContact.address %}
      {!! nl2br(selectedContact.address) !!} <br> 
    {% endif %}
	</div>

	{% if selectedContact.phone1 %}
    <div class="contact-item"> {{ selectedContact.phone1 }} - {{ lcfirst(selectedContact.phone1_label) }} </div>
  {% endif %}
	{% if selectedContact.phone2 %}
    <div class="contact-item"> {{ selectedContact.phone2 }} - {{ lcfirst(selectedContact.phone2_label) }} </div>
  {% endif %}
	{% if selectedContact.phone3  %}
    <div class="contact-item"> {{ selectedContact.phone3 }} - {{ lcfirst(selectedContact.phone3_label) }} </div>
  {% endif %}
	{% if selectedContact.email != null %}
    <div class="contact-item"> {{ selectedContact.email }}  </div>
  {% endif %}
	{% if selectedContact.website %}
    <div class="contact-item"> <a href="{{ selectedContact.website }}"> {{ selectedContact.website  }} </a> </div>
  {% endif %}
	{% if selectedContact.map %}
    <div class="contact-item"> <a href="{{ selectedContact.map }}"> Map </a>  </div>
  {% endif %}
	{% if selectedContact.notes %}
    <div class="contact-item"> {!! nl2br(selectedContact.notes) !!}  </div>
  {% endif %}
	{% if !selectedContact.google_id %}
    <div class="contact-item"> (Not included in Google contacts.)  </div>
  {% endif %}
	</div>

<div class="page-control">

	<a href="/contacts/edit/{{ selectedContact.id }}" class="btn btn-default" role="button">
		<span class="glyphicon glyphicon-pencil"></span>
	</a>

	<a href="/contacts/delete/{{ selectedContact.id }}" class="btn btn-default" role="button"
	   onclick="javascript: return confirm('Are you sure you want to delete this contact?')">
		<span class="glyphicon glyphicon-remove"></span>
	</a>

</div>
