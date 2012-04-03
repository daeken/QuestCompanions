<!DOCTYPE HTML>
<head>
<title>{% block title %}{% endblock %} -- QuestCompanions</title>
<link rel="stylesheet" type="text/css" href="../static/css/core.css"/>
<link rel="stylesheet" type="text/css" href="../static/css/head.css"/>
<link rel="stylesheet" type="text/css" href="../static/css/users.css"/>
</head>
<body>
<div class="header">
  <div class="logo"></div><div class="logotype"></div>
  <div class="nav">
    {% block nav %}{% endblock %}
  </div>
</div>
<div class="content">
<div class="col narrow">
  <div class="userPic">
    <img src="{% block avatar %}{% endblock %}">
  </div>
  <div class="contact block">
    <h3>Information</h3>
    <ul>
    <li>Server: {% block server %}{% endblock %}
    <li>Level: {% block Level %}{% endblock %}
    <li>Faction: {% block faction %}{% endblock %}
    </ul>
  </div>
</div>
<div class="col wide">
  <h1>{% block charName %}{% endblock %}</h1>
  <h2>{% block game %}{% endblock %} </h2>
  <div class="about block">
    <h3>Bio</h3>
    {% block charAbout %}{% endblock %}
  </div>
  <div class="equip block">
    {% block equipment %}{% endblock %}
  </div>
  </div>
  </div>
<div class="footer">
{% block footer %}{% endblock %}
</div>
</body>
