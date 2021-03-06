<div class="section-title">
	@if ( $selectedFolder != null )
		{{$selectedFolder->name}}
	@else
		Uncategorized
	@endif
</div>
<ul class="list-group">
	@foreach ($favorites as $favorite)
		<li class="list-group-item">
			<div class="favorite-icon">
					<a href="javascript:showHide('favoriteMenu-{{$favorite->id}}');">
						<span class="glyphicon glyphicon-bookmark" @if ( $favorite->home_rank > 0 ) style="color: #760f13;" @endif>
						</span>
					</a>
			</div>
			<div class="favorite-text">
				<div class="link">
					<a href="{{ $favorite->url }}">{{ $favorite->name }}</a>
				</div>
				<div class="description">
					{{ $favorite->description }}
				</div>
				<div id="favoriteMenu-{{$favorite->id}}" class="favoriteMenu" style="display: none;">
					@include('favorites/menu')
				</div>
			</div>
			@if ( $favorite->login != null )
				<div class="credentials">
					<div id="credentialHint-{{$favorite->id}}">
						<a href="javascript:showHideCredentials('{{$favorite->id}}');"><span  class="glyphicon glyphicon-briefcase"></span></a>
					</div>
					<div id="credentialData-{{$favorite->id}}" class="credentialData" style="display:none;">
						{{$favorite->login}} | {{$favorite->root}} {{$favorite->passkey}}
					</div>
				</div>
			@endif
			<div style="clear:both"></div>
		</li>
	@endforeach
</ul>

<div class="page-control">
	<a href="/favorites/create/@if($selectedFolder != null){{$selectedFolder->id}}@else{{0}}@endif"  class="btn btn-default" role="button"><span class="glyphicon glyphicon-plus"></span></a>
</div>