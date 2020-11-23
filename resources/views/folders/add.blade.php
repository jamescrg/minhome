
<form id="folderCreateForm" action="/folders/create/{{$page}}" method="post" style="display: none;">
	<input type="hidden" name="_token" value="{{ csrf_token() }}">
	<input class="form-control" type="text" name="name" onchange="submit()" value="">
</form>