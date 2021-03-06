
<div class="col-sm-9 col-sm-push-3">

	<div class="section-title">
		@if (!$edit)
			Add Note
		@else
			Edit Note
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
						<option value="{{$folder->id}}" @if ($note->folder_id == $folder->id) selected @endif>
							{{$folder->name}}
						</option>
					@endforeach
					<option value="0" @if ($selectedFolder == null) selected="selected" @endif>Uncategorized</option>
				</select>
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="subject">Subject</label>
			<div class="col-sm-10">
				<input type="text" autofocus="autofocus" name="subject" id="subject" class="form-control"
				       value="{{old('subject', $note->subject)}}" required>
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="note">Note</label>
			<div class="col-sm-10">
				<textarea name="note" id="note" class="form-control"i required>{{old('note', $note->note)}}</textarea>
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="email"></label>
			<div class="col-sm-10">
		        <input type="submit" value="Submit" class="btn btn-default">
            </div>
        </div>
	</form>
</div>
