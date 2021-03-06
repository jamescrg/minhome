
<div class="section-title">
	{{ $selectedNote->subject }}
</div>

<div class="note">
	{!! nl2br($selectedNote->note) !!}

</div>

<div class="page-control">
	<a href="/notes/edit/{{$selectedNote->id}}" class="btn btn-default" role="button">
		<span class="glyphicon glyphicon-pencil"></span>
	</a>
	<a href="/notes/delete/{{$selectedNote->id}}" class="btn btn-default" role="button"
	   onclick="javascript: return confirm('Are you sure you want to delete this note?')">
		<span class="glyphicon glyphicon-remove"></span>
	</a>
</div>