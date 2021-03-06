
<ul class="list-group">
	@if ($contacts)
		@foreach ($contacts as $contact)
			<li class="list-group-item">
				<a href="/contacts/{{ $contact->id }}" @if ( isset($selectedContact) && $selectedContact->id == $contact->id ) class="strong" @endif;>{{ $contact->name }}</a>
			</li>
		@endforeach
	@endif
</ul>

<div class="page-control">
	@if ($selectedFolder)
		<a href="/{{$page}}/create/{{$selectedFolder->id}}" class="btn btn-default" role="button"><span class="glyphicon glyphicon-plus"></span></a>
	@else
		<a href="/{{$page}}/create/0" class="btn btn-default" role="button"><span class="glyphicon glyphicon-plus"></span></a>
	@endif
</div>
