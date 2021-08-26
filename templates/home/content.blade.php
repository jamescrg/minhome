{% extends 'layout.html' %}
{% block content %}

<form role="form" id="home-form" action="https://{{ searchEngine }}" method="get" class="hidden-xs">
	<div class="row row-centered">
		<div class="col-sm-8 col-sm-offset-2">
			<div class="input-group input-group-md">
				<input id="searchText" class="form-control" autofocus type="text"  maxLength="255" name="q" >
				<div class="input-group-btn">
					<button type="submit" class="btn btn-default" id="googleSearch" style=""><span class="glyphicon glyphicon-search"></span></button>
				</div>
			</div>
		</div>
	</div>
</form>

<form role="form" id="home-form" action="https://{{ searchEngine }}" method="get" class="hidden-sm hidden-md hidden-lg">
	<div class="row row-centered">
		<div class="col-sm-8 col-sm-offset-2">
			<div class="input-group input-group-md">
				<input id="searchText" class="form-control" type="text"  maxLength="255" name="q" >
				<div class="input-group-btn">
					<button type="submit" class="btn btn-default" id="googleSearch" style=""><span class="glyphicon glyphicon-search"></span></button>
				</div>
			</div>
		</div>
	</div>
</form>

<div class="row row-centered">

	<?php for ( counter = 1; counter <= 4; counter++ ) { ?>
		<div class="col-sm-3 col-centered">
			{% for  folders as folder  %}
			{% if folder.home_column == counter %}
				<ul class="list-group home-list">
				<li class="list-group-item home-folder-title">
						<div class="home-control-launch">
							<a href="javascript:showHideHomeControls('{{ folder.id }}');">
								<span class="glyphicon glyphicon-retweet"></span>
							</a>
						</div>
						<a href="/folders/{{ folder.id }}/favorites">{{ folder.name }}</a>
						<!-- home folder controls -.
						<div class="home-folder-controls home-folder-controls-{{ folder.id }}" style="display: none;">
							<a href="/home/folder/{{ folder.id }}/up"><span class="glyphicon glyphicon-arrow-up"></span></a>
							<a href="/home/folder/{{ folder.id }}/down"><span class="glyphicon glyphicon-arrow-down"></span></a>
							<a href="/home/folder/{{ folder.id }}/left"><span class="glyphicon glyphicon-arrow-left"></span></a>
							<a href="/home/folder/{{ folder.id }}/right"><span class="glyphicon glyphicon-arrow-right"></span></a>
						</div>
				</li>
				{% for favorites as favorite %}
					{% if  favorite.folder_id == folder.id  %}
						<li class="list-group-item home-item">
							<a class="home-link-controls-{{ folder.id }}" style="display:none;" href="/home/favorite/{{ favorite.id}}/up"><span class="glyphicon glyphicon-arrow-up"></span></a>
							<a class="home-link-controls-{{ folder.id }}" style="display:none;" href="/home/favorite/{{ favorite.id}}/down"><span class="glyphicon glyphicon-arrow-down"></span></a>
							<a class="home-link" href="{{ favorite.url }}">{{ favorite.name}}</a>
						</li>
					{% endif %}
				{% endforeach %}
				</ul>
			{% endif %}
			{% endforeach %}
		</div>
	<?php } // end for 4 ?>

	<div class="clear: both;">

    </div>

</div>

<div class="row row-centered">

    {% if user_id == 1 AND !tasks.isEmpty() %}

        <ul class="list-group task-list" style="margin: 0 10px;">

            <li class="list-group-item task-list-title"><a href="/tasks/activate/346">Current Tasks</a></li>

            {% for tasks as task %}
                <li class="list-group-item">
                    <a href="/tasks/complete/{{ task.id }}">
                        {% if task.status == 1 %}
                            <img class="task-done" src="/images/icons/task-done.png">
                        {% else %}
                            <img class="task-pending" src="/images/icons/task.png">
                        {% endif %}
                    </a>&nbsp;&nbsp;<a href="/tasks/edit/{{ task.id }}" @if (task.status == 1) style="text-decoration: line-through; color: gray;" {% endif %}>{{ task.title}}</a>
                </li>
            {% endforeach %}

        </ul>

    {% endif %}

</div>

{% endblock content %}
