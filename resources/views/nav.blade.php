
<nav class="navbar navbar-default navbar-fixed-top">
	<div class="container" style="padding-left: 0;">
		<button type="button" id="navButton" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
		</button>
		<div class="collapse navbar-collapse" id="myNavbar" style="margin-left: 0; padding-left: 0;">
			<ul class="nav navbar-nav" id="left-menu">
				<li @if ($page == 'home') class="active" @endif ><a href="/home">Home</a></li>
				<li @if ($page == 'favorites') class="active" @endif><a href="/favorites">Favorites</a></li>
				<li @if ($page == 'tasks') class="active" @endif><a href="/tasks">Tasks</a></li>
				<li @if ($page == 'contacts') class="active" @endif><a href="/contacts">Contacts</a></li>
				<li @if ($page == 'notes') class="active" @endif><a href="/notes">Notes</a></li>
			</ul>
			<ul class="nav navbar-nav navbar-right">
				<li @if ($page == 'search') class="active" @endif>

				<a href="/search">
					Search&nbsp;
					<span class="glyphicon glyphicon-search" style="color: #f4f4f4;"></span>
				</a>
				</li>

			</ul>
		</div>
	</div>
</nav>
