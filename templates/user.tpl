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
    <img src="{% block userPic %}{% endblock %}">
  </div>
  <div class="contact block">
    <h3>contact</h3>
    {% block contactLinks %}{% endblock %}
  </div>
</div>
<div class="col wide">
  <h1>{% block UserName %}{% endblock %}</h1>
  <div class="about block">
    <h3>About Me</h3>
    {% block userAbout %}{% endblock %}
  </div>
  <div class="chars block">
  <h3>My Characters</h3>
    {% block userChar %}{% endblock %}
  </div>
  </div>
  </div>
<div class="footer">
{% block footer %}{% endblock %}
</div>
</body>
    
