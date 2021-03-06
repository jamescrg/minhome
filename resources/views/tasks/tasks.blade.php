<div class="section-title">
	Tasks
</div>

<div id="tasks">

@if ($errors->any())
	<ul class="alert alert-danger">
		@foreach ($errors->all() as $error)
		<li>{{$error}}</li>
		@endforeach
	</ul>
@endif
@if ( isset($activeFolder) )

	@include('tasks/taskform')

	<ul class="list-group task-list task-list-active">
		<li class="list-group-item task-list-title">{{$activeFolder->name}}</li>
		@if ( isset($activeFolderTasks) )
			@foreach ( $activeFolderTasks as $task )
				<li class="list-group-item">
					<a href="/tasks/complete/{{$task->id}}">
						@if ($task->status == 1)
						<img class="task-done" src="/images/icons/task-done.png">
						@else
						<img class="task-pending" src="/images/icons/task.png">
						@endif
					</a>&nbsp;&nbsp;<a href="/tasks/edit/{{$task->id}}" @if ($task->status == 1) style="text-decoration: line-through; color: gray;" @endif>{{$task->title}}</a>
				</li>
			@endforeach
		@endif
	</ul>

@endif

@foreach ( $selectedFolders as $folder )
	<ul class="list-group task-list">
		<li class="list-group-item task-list-title"><a href="/tasks/activate/{{$folder->id}}">{{$folder->name}}</a></li>
		@foreach ($selectedFolderTasks[$folder->id] as $task)
			<li class="list-group-item">
				<a href="/tasks/complete/{{$task->id}}">
					@if ($task->status == 1)
						<img class="task-done" src="/images/icons/task-done.png">
					@else
						<img class="task-pending" src="/images/icons/task.png">
					@endif
				</a>&nbsp;&nbsp;<a href="/tasks/edit/{{$task->id}}" @if ($task->status == 1) style="text-decoration: line-through; color: gray;" @endif>{{$task->title}}</a>
			</li>
		@endforeach
	</ul>
@endforeach

@if ( isset($activeFolder) )
<div class="page-control" id="clear">
	<a href="tasks/clear/{{$activeFolder->id}}" class="btn btn-default"><span class="glyphicon glyphicon-new-window"></span></a>
</div>
@endif

</div>
