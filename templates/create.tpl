{% extends "loggedOut.tpl" %}
{% block title %}Create Account{% endblock %}
{% block content %}
  <span class="Welcome"><!-- TODO Create a "welcome message" for here --></span>
  <div class="form">
    <span class="label">Username: </span><input id="name" type="text" placeholder="Username">
    <br/>
    <span class="label">Password: </span><input id="pass" type="password" placeholder="Password">
    <br/>
    <span class="label">Email: </span><input id="email" type="email" placeholder="Email">
    <br/>
    <button id="submit">Enlist!</button>
  </div>
{% endblock %}
