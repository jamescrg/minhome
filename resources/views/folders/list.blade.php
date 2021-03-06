<div class="section-title">
	@if ($page == 'tasks')
		Lists
	@else
		Folders
	@endif
</div>
<ul class="list-group">
	@foreach ($folders as $folder)

		<!-- ------------------------------------------------------ -->
		<!-- normal display, show folder -->
		<!-- ------------------------------------------------------ -->
		<li class="list-group-item" id="folderItem-{{$folder->id}}" style="display:block;">
			<a href="javascript:showHideFolder('{{$folder->id}}');">
				@if ($page == 'tasks')
					<span class="glyphicon glyphicon-th-list"></span>
				@else
					<span class="glyphicon glyphicon-folder-close"></span>
				@endif
			</a>
			<a class="folderLink" href="/folders/{{ $folder->id }}/{{ $page }}" @if ( $folder->selected == 1 ) style="font-weight: bold;"@endif;>
				{{$folder->name }}
				@if ( $folder->home_column > 0 )
					&nbsp;*
				@endif
			</a>
		</li>

		<!-- ------------------------------------------------------ -->
		<!-- form to edit a folder -->
		<!-- ------------------------------------------------------ -->
		@include('folders/edit')

	@endforeach

	@if ($page != 'tasks')
		<li class="list-group-item" style="border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;">
			<span class="glyphicon glyphicon-folder-close"></span>
			<a class="folderLink" href="/folders/0/{{ $page }}" @if ( $selectedFolder == null ) style="font-weight: bold;"@endif;>
				Uncategorized
			</a>
		</li>
	@endif

	@include('folders/add')

</ul>

<div class="page-control">
	<a href="javascript:showHide('folderCreateForm');" class="btn btn-default" role="button"><span class="glyphicon glyphicon-plus"></span></a>
</div>