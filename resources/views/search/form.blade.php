<div class="vertical-center hidden-xs">
	<form role="form" id="search-form" action="/search" method="post" >
		@csrf
		<div class="search-title">

		</div>
		<div class="row row-centered">
			<div class="col-sm-8 col-sm-offset-2">
				<div class="input-group input-group-md">
					<input id="searchText" class="form-control" autofocus type="text"  maxLength="255" name="searchText" >
					<div class="input-group-btn">
						<button type="submit" class="btn btn-default" id="textSearch" style=""><span class="glyphicon glyphicon-search"></span></button>
					</div>
				</div>
			</div>
		</div>
	</form>
</div>

<div class="vertical-center hidden-sm hidden-md hidden-lg">
	<form role="form" id="search-form" action="/search" method="post" >
		<input type="hidden" name="_token" value="{{ csrf_token() }}">
		<div class="search-title">

		</div>
		<div class="row row-centered">
			<div class="col-sm-8 col-sm-offset-2">
				<div class="input-group input-group-md">
					<input id="searchText" class="form-control" type="text"  maxLength="255" name="searchText" >
					<div class="input-group-btn">
						<button type="submit" class="btn btn-default" id="textSearch" style=""><span class="glyphicon glyphicon-search"></span></button>
					</div>
				</div>
			</div>
		</div>
	</form>
</div>

