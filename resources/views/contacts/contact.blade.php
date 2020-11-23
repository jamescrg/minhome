
<div class="section-title">
	{{ $selectedContact->name }}
</div>

<div class="contact">

	<div class="contact-item">
		{{ $selectedContact->name }} <br>
		@if ( $selectedContact->company != null ) {{ $selectedContact->company  }} 	<br> @endif
		@if ( $selectedContact->address != null ){!! nl2br($selectedContact->address) !!} <br> @endif
	</div>
	@if ( $selectedContact->phone1 != null ) <div class="contact-item"> {{ $selectedContact->phone1  }} - {{ lcfirst($selectedContact->phone1_label)  }} </div> @endif
	@if ( $selectedContact->phone2 != null ) <div class="contact-item"> {{ $selectedContact->phone2  }} - {{ lcfirst($selectedContact->phone2_label)  }} </div> @endif
	@if ( $selectedContact->phone3 != null ) <div class="contact-item"> {{ $selectedContact->phone3  }} - {{ lcfirst($selectedContact->phone3_label)  }} </div> @endif
	@if ( $selectedContact->email != null ) <div class="contact-item"> {{ $selectedContact->email  }}  </div> @endif
	@if ( $selectedContact->website != null ) <div class="contact-item"> <a href="{{$selectedContact->website}}"> {{ $selectedContact->website  }} </a> </div> @endif
	@if ( $selectedContact->map != null ) <div class="contact-item"> <a href="{{$selectedContact->map}}"> Map </a>  </div> @endif
	@if ( $selectedContact->notes != null ) <div class="contact-item"> {!! nl2br($selectedContact->notes)  !!}  </div> @endif
	@if ( $selectedContact->google_id == null ) <div class="contact-item"> (Not included in Google contacts.)  </div> @endif
	</div>
<div class="page-control">
	<a href="/contacts/edit/{{$selectedContact->id}}" class="btn btn-default" role="button">
		<span class="glyphicon glyphicon-pencil"></span>
	</a>
	<a href="/contacts/delete/{{$selectedContact->id}}" class="btn btn-default" role="button"
	   onclick="javascript: return confirm('Are you sure you want to delete this contact?')">
		<span class="glyphicon glyphicon-remove"></span>
	</a>
</div>