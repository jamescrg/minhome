@extends('layout-app')
@section('content')
<div class="row">

	@if ( isset($edit) )
		@include('contacts/create')
	@else
		@include('contacts/contacts')
	@endif

	<div id="folders" class="col-sm-3 col-sm-pull-9">
		@include('folders/list')
	</div>

</div>
@stop
