---
layout: home
title: Journal Club
permalink: /journalclub/  
articles:
  data_source: site.categories.journalclub
  type: item
  show_cover: true
  show_excerpt: true
  show_readmore: true
  show_info: true
  excerpt_type: html
---

<p>Welcome to our Journal Club posts! Here we present selected papers discussed in our reading group.</p>

<ul class="post-list">
  {% assign posts = site.categories.journalclub | sort: 'date' | reverse %}
  {% for post in posts %}
    <li style="margin-bottom: 1.2em;">
      <h3 style="margin:0;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p style="color:#666; font-size: 0.9em;">{{ post.date | date: "%b %d, %Y" }}</p>
      <p>{{ post.excerpt | strip_html }}</p>
    </li>
  {% endfor %}
</ul>