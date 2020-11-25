@extends('layout-app')
@section('content')
	<div class="row">
		@include('search/form')
		@if($results)
			@include('search/results')
		@endif
	</div>
@stop
