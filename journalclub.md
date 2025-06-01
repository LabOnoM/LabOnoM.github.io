---
layout: page
title: Journal Club
permalink: /journalclub/
---

<p>Welcome to our Journal Club posts! Here we present selected papers discussed in our reading group, along with summaries and insights.</p>

<ul class="post-list">
  {% assign posts = site.categories.journalclub | sort: 'date' | reverse %}
  {% for post in posts %}
    <li style="margin-bottom: 1.2em;">
      <h3 style="margin:0;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p style="color:#666; font-size: 0.9em;">{{ post.date | date: "%b %d, %Y" }}</p>
      <p>{{ post.excerpt | strip_html | truncate: 200 }}</p>
    </li>
  {% endfor %}
</ul>

