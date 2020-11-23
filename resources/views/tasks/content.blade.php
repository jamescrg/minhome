@extends('app')
@section('content')

<div class="row">

	<div id="favorites" class="col-sm-9 col-sm-push-3">
		@if ( isset($edit) )
			@include('tasks/create')
		@else
			@include('tasks/tasks')
		@endif
	</div>

	<div id="lists" class="col-sm-3 col-sm-pull-9">
		@include('folders/list')
	</div>

</div>
@stop