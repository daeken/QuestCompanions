<!DOCTYPE HTML>
<head>
<title>{% block title %}{% endblock %} -- QuestCompanions</title>
<link rel="stylesheet" type="text/css" href="../static/css/core.css"/>
<link rel="stylesheet" type="text/css" href="../static/css/head.css"/>
<script src="/scripts/jquery-1.6.4.js"></script>
<script src="/rpc.js"></script>
{% block includes %}{% endblock %}
</head>
<body>
<div class="header">
  <div class="logo"></div><div class="logotype"></div>
  <div class="nav">
    {% for item in navigation %}
      <a class="button" href="{{ item.href }}">{{ item.title }}</a>
    {% endfor %}
  </div>
</div>
<div class="content">
{% block content %}{% endblock %}
</div>
<div class="footer">
{% for item in footer %}
  <a href="{{ item.href }}">{{ item.title }}</a>
{% endfor %}
</div>
</body>
    
