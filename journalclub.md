---
layout: page
title: Journal Club
permalink: /journalclub/
---

Welcome to our Journal Club posts!

{% assign posts = site.categories.journalclub %}
<ul>
  {% for post in posts %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
