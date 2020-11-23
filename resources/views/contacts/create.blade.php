
<div class="col-sm-9 col-sm-push-3">

	<div class="section-title">
		@if (!$edit)
			Add Contact
		@else
			Edit Contact
		@endif
	</div>

	@include('form-error')

	<form action="{{$action}}" class="form-horizontal" method="post" role="form">
		<input type="hidden" name="_token" value="{{ csrf_token() }}">
		<div class="form-group">
			<label class="control-label col-sm-2" for="folder_id">Folder</label>
			<div class="col-sm-10">
				<select class="form-control" name="folder_id" id="folder_id">
					@foreach ($folders as $folder)
						<option value="{{$folder->id}}" @if ($contact->folder_id == $folder->id) selected="selected" @endif>
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
				<input type="text" autofocus="autofocus" name="name" id="name"
				       class="form-control" value="{{$contact->name}}">
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="company">Company</label>
			<div class="col-sm-10">
				<input type="text" name="company" id="company" class="form-control" value="{{$contact->company}}">
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="address">Address</label>
			<div class="col-sm-10">
				<textarea name="address" id="address" class="form-control">{!!nl2br($contact->address)!!}</textarea>
			</div>
		</div>
		<?php $phoneLabels = array('Work', 'Mobile', 'Home', 'Fax', 'Other'); ?>
		<div class="form-group">
			<label class="control-label col-sm-2" for="phone1">Phone 1</label>
			<div class="col-sm-10">
				<input type="text" name="phone1" id="phone1" class="form-control"  value="{{$contact->phone1}}">
				<select id="phone1_label" name="phone1_label" class="form-control">
					@foreach ( $phoneLabels as $phoneLabel )
						<option	value="{{$phoneLabel}}" @if ($contact->phone1_label == $phoneLabel) selected="selected" @endif> {{$phoneLabel}} </option>
					@endforeach
				</select>
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="phone2">Phone 2</label>
			<div class="col-sm-10">
				<input type="text" name="phone2" id="phone2" class="form-control"  value="{{$contact->phone2}}">
				<select id="phone2_label" name="phone2_label" class="form-control">
					@foreach ( $phoneLabels as $phoneLabel )
						<option	value="{{$phoneLabel}}" @if ($contact->phone2_label == $phoneLabel) selected="selected" @endif> {{$phoneLabel}} </option>
					@endforeach
				</select>
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="phone3">Phone 3</label>
			<div class="col-sm-10">
				<input type="text" name="phone3" id="phone3" class="form-control" value="{{$contact->phone3}}">
				<select id="phone3_label" name="phone3_label" class="form-control">
					@foreach ( $phoneLabels as $phoneLabel )
						<option	value="{{$phoneLabel}}" @if ($contact->phone3_label == $phoneLabel) selected="selected" @endif> {{$phoneLabel}} </option>
					@endforeach
				</select>
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="email">Email</label>
			<div class="col-sm-10">
				<input type="text" name="email" id="email" class="form-control" value="{{$contact->email}}">
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="website">Website</label>
			<div class="col-sm-10">
				<input type="text" name="website" id="website" class="form-control" value="{{$contact->website}}">
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="map">Map URL</label>
			<div class="col-sm-10">
				<input type="text" name="map" id="map" class="form-control" value="{{$contact->map}}">
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-2" for="notes">Notes</label>
			<div class="col-sm-10">
				<textarea name="notes" id="notes" class="form-control">{{ $contact->notes }}</textarea>
			</div>
		</div>
		<div class="submit"><input type="submit" value="Submit" class="btn btn-default"></div>
	</form>
</div>
