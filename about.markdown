---
layout: page
title: About me
subtitle: Why me instead of a robot?
permalink: /about/
---

{% if site.data.me.about.qualities %}
Some of my best qualities:
{% for quality in site.data.me.about.qualities %}
- **{{ quality.name }}**: {{ quality.description }}
{% endfor %}
{% else %}
Why not ?
{% endif %}
