@extends('layout-app')
@section('content')

<div class="row">

	<div id="favorites" class="col-sm-9 col-sm-push-3">
		@if ( isset($edit) )
			@include('favorites/create')
		@else
			@include('favorites/list')
		@endif
	</div>

	<div id="folders" class="col-sm-3 col-sm-pull-9">
		@include('folders/list')
	</div>

</div>
@stop
