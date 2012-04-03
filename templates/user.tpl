{% extends base.tpl %}
{% block title %}{{ user.username }}{% endblock %}
{% block includes %}
<link rel="stylesheet" type="text/css" href="../static/css/core.css"/>
<link rel="stylesheet" type="text/css" href="../static/css/head.css"/>
<link rel="stylesheet" type="text/css" href="../static/css/users.css"/>
{% endblock %}
{% block content %}
<div class="col narrow">
  <div class="userPic">
    <img src="{{ user.pic }}">
  </div>
  <div class="contact block">
    <h3>contact</h3>
    {% for link in user.contact %}
      <a class="contact" href="{{ link.href }}i">{{ link.type }}</a>
  </div>
</div>
<div class="col wide">
  <h1>{{ user.username }}</h1>
  <div class="about block">
    <h3>About Me</h3>
    {{ user.about }}
  </div>
  <div class="chars block">
  <h3>My Characters</h3>
  {% for char in user.chars %}
    <a href="{{ char.href }}"><img src="{{ char.pic }}"></a>
{% endfor %}
  </div>
  </div>

{% endblock %}
    
