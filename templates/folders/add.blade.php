
<form id="folderCreateForm" action="/folders/create/{{ page }}" method="post" style="display: none;">
	@csrf
	<input class="form-control" type="text" name="name" onchange="submit()" value="">
</form>
