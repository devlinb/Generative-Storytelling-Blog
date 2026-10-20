#!/usr/bin/env python3
"""Import public Hashnode Markdown and images into Hugo leaf bundles.

Run from the repository root. Raw responses are cached outside the repository.
Existing bundles are never overwritten. No Hashnode credentials are required.
"""
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HOST = 'https://meanderingthoughts.hashnode.dev'
CACHE = Path('/tmp/meandering-hashnode-export')
ROOT = Path(__file__).resolve().parents[1]


def fetch(url):
    key = hashlib.sha256(url.encode()).hexdigest()
    path = CACHE / key
    if not path.exists():
        req = urllib.request.Request(url, headers={'User-Agent': 'Personal-blog-migration/1.0'})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
            if not data:
                raise ValueError(f'Empty response: {url}')
            path.write_bytes(data)
    return path.read_bytes()


def metadata(source):
    chunks = []
    for match in re.finditer(r'self\.__next_f\.push\((\[1,.*?\])\)</script>', source):
        chunks.append(json.loads(match[1])[1])
    flight = ''.join(chunks)
    match = re.search(r'"post":(\{)', flight)
    if not match:
        raise ValueError('Post metadata missing')
    return json.JSONDecoder().raw_decode(flight[match.start(1):])[0]



def normalize_markdown(body):
    # Hashnode places alignment hints inside Markdown image destinations.
    body = re.sub(r'(!\[[^\]]*\]\([^\n]*?)\s+align="(?:left|center|right)"(\))', r'\1\2', body)
    body = re.sub(r'(!\[[^\]]*\]\([^\n]*?\))\s+align="(?:left|center|right)"', r'\1', body)
    # Convert legacy HTML footnote anchors to portable Markdown footnotes.
    body = re.sub(r'\[<sup(?: id="[0-9]+")?>([0-9]+)</sup>\]\(#ft[0-9]+\)', r'[^\1]', body)
    body = re.sub(r'^<span id="ft([0-9]+)"></span>[0-9]+\.\s*', r'[^\1]: ', body, flags=re.M)
    body = re.sub(r'^\\\[([0-9]+)\\\]\s*', r'[^\1]: ', body, flags=re.M)
    body = re.sub(r'\s*\[go back\]\(#[0-9]+\)', '', body)
    return body


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    sitemap = ET.fromstring(fetch(HOST + '/sitemap.xml'))
    urls = [node.text for node in sitemap.findall('{*}url/{*}loc')]
    urls = [url for url in urls if urllib.parse.urlsplit(url).path not in
            ('', '/', '/archive', '/recommendations') and '/page/' not in url]
    slugs = {url.rstrip('/').rsplit('/', 1)[1] for url in urls}
    report = []
    for url in urls:
        slug = url.rsplit('/', 1)[1]
        bundle = ROOT / 'content/posts' / slug
        if bundle.exists():
            raise FileExistsError(f'Refusing to overwrite {bundle}')
        source = fetch(url).decode()
        post = metadata(source)
        if post['slug'] != slug:
            raise ValueError(f'Unexpected slug for {url}')
        body = fetch(url + '.md').decode()
        if body.lstrip().startswith(('<!DOCTYPE', '<html')):
            raise ValueError(f'Markdown endpoint returned HTML: {url}')
        # Hugo already renders the title above the article.
        body = re.sub(r'^\s*# [^\n]+\n+', '', body, count=1)
        cover = post.get('coverImage') or {}
        cover_url = cover.get('url') if isinstance(cover, dict) else cover
        image_urls = set(re.findall(r'!\[[^\]]*\]\(\s*<?([^\s)>]+)', body))
        image_urls.update(re.findall(r'<img\b[^>]*\bsrc=[\"\x27]([^\"\x27]+)', body))
        if cover_url:
            image_urls.add(cover_url)
        images = {}
        pending = {}
        for image_url in sorted(image_urls):
            remote = urllib.parse.urljoin(url, html.unescape(image_url))
            if urllib.parse.urlsplit(remote).scheme not in ('https', 'http'):
                continue
            data = fetch(remote)
            ext = Path(urllib.parse.urlsplit(remote).path).suffix.lower()
            if not re.fullmatch(r'\.(png|jpe?g|gif|webp|svg|avif)', ext):
                if data.startswith(b'\x89PNG'): ext = '.png'
                elif data.startswith(b'\xff\xd8'): ext = '.jpg'
                elif data.startswith(b'GIF8'): ext = '.gif'
                elif data[:4] == b'RIFF': ext = '.webp'
                else: raise ValueError(f'Unrecognized image: {remote}')
            name = ('cover' if image_url == cover_url else 'image-' + hashlib.sha256(remote.encode()).hexdigest()[:12]) + ext
            pending[name] = data
            images[image_url] = name
        for original, local in sorted(images.items(), key=lambda item: -len(item[0])):
            body = body.replace(original, local)
        for target in sorted(slugs, key=len, reverse=True):
            body = re.sub(re.escape(HOST + '/' + target) + r'(?=[/#?\s)\]<>\"\x27]|$)',
                          '/blog/posts/' + target + '/', body)
        body = normalize_markdown(body)
        fields = {
            'title': post['title'], 'slug': slug, 'date': post['publishedAt'],
            'lastmod': post.get('updatedAt') or post['publishedAt'],
            'author': (post.get('author') or {}).get('name', 'Devlin Bentley'),
            'description': post.get('brief', ''),
            'tags': [tag['name'].strip() for tag in post.get('tags', [])],
            'draft': False, 'sourceURL': url,
        }
        if cover_url: fields['cover'] = images[cover_url]
        if post.get('subtitle'): fields['subtitle'] = post['subtitle']
        if post.get('series'): fields['hashnodeSeries'] = post['series']
        bundle.mkdir(parents=True)
        for name, data in pending.items(): (bundle / name).write_bytes(data)
        # JSON is valid YAML and safely quotes multiline text and punctuation.
        front = '\n'.join(f'{key}: {json.dumps(value, ensure_ascii=False)}' for key, value in fields.items())
        (bundle / 'index.md').write_text('---\n' + front + '\n---\n\n' + body.rstrip() + '\n')
        report.append({'slug': slug, 'source': url, 'images': images, 'title': post['title']})
        print(f'{slug}: {len(images)} images', flush=True)
    (ROOT / 'hashnode-migration.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'Imported {len(report)} posts, {sum(len(p["images"]) for p in report)} images')


if __name__ == '__main__':
    main()
