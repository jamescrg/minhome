<li class="list-group-item" id="folderForm-{{ folder.id }}" style="display: none;">
	<a href="javascript:showHideFolder('{{ folder.id }}');">
		<span class="glyphicon glyphicon-folder-close" style=""></span>
	</a>
	<form class="editFolder" action="/folders/update/{{ folder.id }}/{{ page}}" method="post">
	@csrf
	<input class="form-horizontal"
		   autofocus
		   type="text"
		   name="name"
		   onchange="submit()"
		   value="{{ folder.name }}">
	</form>
	<ul id="folderInput-{{ folder.id }}" class="folderMenu">
		{% if page == 'favorites' %}
			<li><a href="/folders/home/{{ folder.id }}/{{ page}}"> @if (folder.home_column > 0) Remove from {% else %} Add to {% endif %} Home </a></li>
		{% endif %}
		<li><a href="/folders/delete/{{ folder.id }}/{{ page}}"
			   onclick="javascript: return confirm('Are you sure you want to delete this folder?')">Delete
			</a></li>
	</ul>
</li>
