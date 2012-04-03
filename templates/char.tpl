{% extends "base.tpl" %}
{% block title %}{{ char.name }}{% endblock %}
{% block includes %} <link rel="stylesheet" type="text/css" href="../static/css/users.css"/>
{% endblock %}
{% block content %}
<div class="col narrow">
  <div class="userPic">
    <img src="{{ char.pic }}">
  </div>
  <div class="contact block">
    <h3>Information</h3>
    <ul>
    <li>Server: {{ char.server }}
    {% if char.level is defined %}
    <li>Level: {{ char.level }}
    {% endif %}
    {% if char.level is defined %}
    <li>Faction: { char.faction }}
    {% endif %}
    {% if char.level is defined %}
    <li>Equipment level: {{ char.equipment }}
    {% endif %}
    </ul>
  </div>
</div>
<div class="col wide">
  <h1>{{ char.username }}</h1>
  <h2>{{ char.game }} </h2>
  <div class="about block">
    <h3>Bio</h3>
    {{ char.bio }}
  </div>
  </div>
{% endblock %}
