
<form role="form" id="tasks-form" method="post" action="/tasks" >
	<input type="hidden" name="_token" value="{{ csrf_token() }}">
	<input type="hidden" name="folder_id" value="{{ activeFolder.id }}">
	<div class="input-group input-group-md">
		<input id="focal" class="form-control" type="text"  maxLength="255" name="title" autofocus>
		<div class="input-group-btn">
			<button type="submit" class="btn btn-default" id="btn-tasks-add"><span class="glyphicon glyphicon-plus"></span></button>
		</div>
	</div>
</form>
