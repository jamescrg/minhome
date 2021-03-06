<div class="section-title">
	@if (!$edit)
		Add Task
	@else
		Edit Task
	@endif
</div>

@include('form-error')

<form action="{{$action}}" class="form-horizontal" method="post" role="form">

    @csrf

	<div class="form-group">
		<label class="control-label col-sm-2" for="folder_id">Folder</label>
		<div class="col-sm-10">
			<select class="form-control" name="folder_id" id="folder_id">
				@foreach ($folders as $folder)
					<option value="{{$folder->id}}" @if ($task->folder_id == $folder->id) selected @endif>
						{{$folder->name}}
					</option>
				@endforeach
			</select>
		</div>
	</div>
	<div class="form-group">
		<label class="control-label col-sm-2" for="subject">Task</label>
		<div class="col-sm-10">
			<input type="text" autofocus name="title" id="subject" class="form-control"
				   value="{{$task->title}}">
		</div>
	</div>
	<div class="submit"><input type="submit" value="Submit" class="btn btn-default"></div>
</form>
