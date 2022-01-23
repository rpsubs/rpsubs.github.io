import sys
import json
import os.path
import html

MAX_ITEMS = 20

filename = os.path.basename(sys.argv[1])
title, ext = os.path.splitext(filename)

with open(sys.argv[1], 'r') as f:
  jsonp = f.read()

data = json.loads(jsonp[10:-1])

items = []
versions = set()

while len(items) < MAX_ITEMS and len(data) > 0:
  item = data.pop(0)

  if not item.get('zipUrl'):
    continue
  if item.get('version') in versions:
    continue

  items.append(item)
  versions.add(item.get('version'))

feed = {
  'version': 'https://jsonfeed.org/version/1',
  'title': f"{title} downloads",
  'feed_url': f"https://rpsubs.github.io/atlassian/downloads/{filename}",
  'items': [{
    'id': item.get('zipUrl'),
    'url': item.get('zipUrl'),
    'title': f"{title} {item.get('version')} ({item.get('released')})",
    'content_html': (
      '<p><a href="%s">Release notes</a></p>' % html.escape(item.get('releaseNotes')) 
      if item.get('releaseNotes') else '<p>No release notes</p>'
    )
  } for item in items]
}

with open(sys.argv[1], 'w') as f:
  f.write(json.dumps(feed, ensure_ascii=False, indent=2))
