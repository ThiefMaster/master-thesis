{% extends 'base.html' %}
{% block title %}Beispiel{% endblock %}
{% block content %}
  <a href="{% url 'example' example.id %}">
    {{ example.title }}
  </a>
{% endblock %}
