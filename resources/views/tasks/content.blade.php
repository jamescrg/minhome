@extends('layout-app')
@section('content')

<div class="row">

	<div id="favorites" class="col-sm-9">
		@if ( isset($edit) )
			@include('tasks/create')
		@else
			@include('tasks/tasks')
		@endif
	</div>

	<div id="lists" class="col-sm-3">
		@include('folders/list')
	</div>

</div>
@stop
