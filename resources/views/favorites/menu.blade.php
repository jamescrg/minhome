
<ul>
	<li>
		<a href="/favorites/edit/{{$favorite->id}}">Edit</a>
	</li>
	<li>
		<a href="/favorites/home/{{$favorite->id}}"> @if ($favorite->home_rank > 0) Remove from @else Add to @endif Home </a>
	</li>
	<li>
		<a href="/favorites/delete/{{$favorite->id}}"
		onclick="javascript: return confirm('Are you sure you want to delete this favorite?')">Delete
		</a>
	</li>
</ul>
