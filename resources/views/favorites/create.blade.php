
	<div class="section-title">
		@if (!$edit)
			Add Favorite
		@else
			Edit Favorite
		@endif
	</div>

	@include('form-error')

	<form action="{{$action}}" class="form-horizontal" method="post" role="form">
		<input type="hidden" name="_token" value="{{ csrf_token() }}">
		<div class="form-group">
			<label class="control-label col-sm-2" for="folder_id">Folder</label>
			<div class="col-sm-10">
				<select class="form-control" name="folder_id" id="folder_id">
					<option value="">
					@foreach ($folders as $folder)
						<option value="{{$folder->id}}" @if ($favorite->folder_id == $folder->id) selected="selected" @endif>
							{{$folder->name}}
						</option>
					@endforeach
					<option value="0" @if ($selectedFolder == null) selected="selected" @endif>Uncategorized</option>
				</select>
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="name">Name</label>
			<div class="col-sm-10">
				<input type="text" autofocus="autofocus" name="name" id="name" class="form-control"
				       value="{{$favorite->name}}">
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="url">Url</label>
			<div class="col-sm-10">
				<input type="text" name="url" id="url" class="form-control" value="{{$favorite->url}}">
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="description">Description</label>
			<div class="col-sm-10">
				<textarea name="description" id="description" class="form-control">{{$favorite->description}}</textarea>
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="login">Login</label>
			<div class="col-sm-10">
				<input type="text" name="login" id="login" class="form-control" value="{{$favorite->login}}">
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="root">Root</label>
			<div class="col-sm-10">
				<input type="text" name="root" id="root" class="form-control" value="{{$favorite->root}}">
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="passkey">Key</label>
			<div class="col-sm-10">
				<input type="text" name="passkey" id="passkey" class="form-control" value="{{$favorite->passkey}}">
			</div>
		</div>
		<div class="submit"><input type="submit" value="Submit" class="btn btn-default"></div>
	</form>
