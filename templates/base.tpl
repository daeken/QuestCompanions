<!DOCTYPE HTML>
<head>
<title>{% block title %}{% endblock %} -- QuestCompanions</title>
<link rel="stylesheet" type="text/css" href="../static/css/core.css"/>
<link rel="stylesheet" type="text/css" href="../static/css/head.css"/>
</head>
<body>
<div class="header">
  <div class="logo"></div><div class="logotype"></div>
  <div class="nav">
    {% block nav %}{% endblock %}
  </div>
</div>
<div class="content">
{% block content %}{% endblock %}
</div>
<div class="footer">
{% block footer %}{% endblock %}
</div>
</body>
    
