<div id="note" class="col-sm-6 col-sm-push-6">
	@if ( isset($selectedNote) )
		@include('notes/note')
	@endif
</div>

<div id="notes" class="col-sm-3 col-sm-pull-3">
	<div class="section-title">
		Notes
	</div>
	@if ( isset($notes) )
		@include('notes/list')
	@else
	<ul class="list-group">
		<li class="list-group-item">No notes selected.</li>
	</ul>
	@endif
</div>

