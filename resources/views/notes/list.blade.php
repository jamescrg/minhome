
<ul class="list-group">
	@foreach ($notes as $note)
		<li class="list-group-item">
			<a href="/notes/{{ $note->id }}" @if ( isset($selectedNote) && $selectedNote->id == $note->id ) class="strong" @endif;>{{ $note->subject }}</a>
		</li>
	@endforeach
</ul>

<div class="page-control">
	@if ($selectedFolder)
		<a href="/{{$page}}/create/{{$selectedFolder->id}}" class="btn btn-default" role="button"><span class="glyphicon glyphicon-plus"></span></a>
	@else
		<a href="/{{$page}}/create/0" class="btn btn-default" role="button"><span class="glyphicon glyphicon-plus"></span></a>
	@endif
</div>