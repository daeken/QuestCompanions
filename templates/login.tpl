{% extends "loggedOut.tpl" %}
{% block title %}Login{% endblock %}
{% block content %}
    <div id="loginForm" class="col left">
      <input id="uName" type="text" placeholder="Username">
      <br/>
      <input id="uPass" type="password" placeholder="Password">
      <br/>
      <button id="submit">Log in</button>
      <span class="noAcc">Don't have an account? <a href="#">Enlist today!</a></span>
    </div>
    <div id="loginFB" class="col right">
      <div id="FBBox">
        INSERT FACEBOOK CONNECT STUFF HERE
      </div>
    </div>
{% endblock %}
