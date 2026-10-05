#!/usr/bin/env python3
"""Validate source metadata, classification, version links, and local document links."""
import json
import re
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
CUTOFF = date(2026, 10, 5)
ERRORS = []

def require(condition, message):
    if not condition:
        ERRORS.append(message)

def read(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

def normalize(text):
    return re.sub('[^a-z0-9]', '', unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower())

def url_ok(url):
    value = urlsplit(url)
    return value.scheme == 'https' and bool(value.netloc) and not value.username and not value.password and not re.search(r'\s', url)

def main():
    papers = read('papers.json')
    supplements = read('supplementary.json')
    venues = {p['venue']: p for p in read('venues.json')}
    ids, dois, versions = set(), set(), set()
    for p in papers:
        label = p.get('id', '?')
        for field in ['id', 'title', 'authors', 'year', 'venue', 'ccf_grade', 'publication_type', 'scope', 'paper_url', 'source_urls', 'tag_basis', 'tags', 'checked_at', 'format_status']:
            require(field in p and p[field] not in ('', [], None), f'{label}: empty/missing {field}')
        require(label not in ids, f'Duplicate id: {label}')
        ids.add(label)
        require(p['venue'] in venues, f'{label}: venue not in verified registry')
        if p['venue'] in venues:
            require(p['ccf_grade'] == venues[p['venue']]['ccf_grade'], f'{label}: CCF grade mismatch')
            require(p['publication_type'] == venues[p['venue']]['publication_type'], f'{label}: venue type mismatch')
        require(p['ccf_grade'] in {'A', 'B'}, f'{label}: invalid CCF grade')
        require(isinstance(p['year'], int) and 2013 <= p['year'] <= CUTOFF.year, f'{label}: invalid year')
        require(p['scope'] in {'core', 'dataset', 'pretraining', 'temporal_evidence_qa'}, f'{label}: invalid scope')
        require(p['tag_basis'] in {'title', 'abstract_reviewed'}, f'{label}: invalid tag basis')
        require(p['format_status'] in {'journal_article', 'official_main_proceedings', 'main_proceedings_format_not_individually_audited'}, f'{label}: invalid publication format')
        require(p['checked_at'] <= CUTOFF.isoformat(), f'{label}: checked after cutoff')
        version = (normalize(p['title']), p['venue'], p['year'])
        require(version not in versions, f'{label}: duplicate publication version')
        versions.add(version)
        if p.get('doi'):
            doi = p['doi'].lower()
            require(doi not in dois, f'{label}: duplicate DOI')
            require(doi.startswith('10.') and '/' in doi, f'{label}: malformed DOI')
            dois.add(doi)
        dates = [date(v[0], v[1] if len(v) > 1 else 1, v[2] if len(v) > 2 else 1) for v in p.get('publication_dates', {}).values()]
        require(not dates or min(dates) <= CUTOFF, f'{label}: publication after cutoff')
        for u in p['source_urls'] + [p['paper_url']] + [p.get(k, '') for k in ['code_url', 'arxiv_url']]:
            if u: require(url_ok(u), f'{label}: malformed URL {u}')
        if p.get('code_url'):
            require(p.get('code_status') and p['code_status'] != 'not_verified', f'{label}: code link lacks verification status')
        require(not re.search(r'findings|workshop|doctoral|companion', p['venue'], re.I), f'{label}: special proceedings in main index')
    require(not ids.intersection(s['id'] for s in supplements), 'Supplement and main share IDs')
    for p in papers:
        for linked in p.get('related_record_ids', []):
            require(linked in ids and linked != p['id'], f'{p["id"]}: broken version relation')
    for p in supplements:
        require(bool(p.get('status')) and bool(p.get('exclusion_reason')), f'{p["id"]}: supplement status missing')
        require(url_ok(p['paper_url']), f'{p["id"]}: invalid supplement URL')
    # Check internal file targets and explicit anchors, without external requests in CI.
    for path in ROOT.rglob('*.md'):
        content = path.read_text(encoding='utf-8')
        require('/Users/' not in content, f'{path.relative_to(ROOT)}: private local path')
        for href in re.findall(r'\]\(([^\s)]+)\)', content) + re.findall(r'<(?:img|a)[^>]+(?:src|href)="([^"]+)"', content):
            href = href.strip('<>')
            if urlsplit(href).scheme:
                continue
            filename, _, anchor = href.partition('#')
            target = (path.parent / unquote(filename)).resolve() if filename else path
            require(target.is_relative_to(ROOT), f'{path.relative_to(ROOT)}: link leaves repository')
            require(target.exists(), f'{path.relative_to(ROOT)}: missing {href}')
            if anchor and target.exists() and target.suffix == '.md':
                body = target.read_text(encoding='utf-8')
                require(f'id="{anchor}"' in body or any(heading_anchor(h) == anchor for h in re.findall(r'^#+\s+(.+)$', body, re.M)), f'{path.relative_to(ROOT)}: missing anchor {href}')
    for svg in (ROOT / 'assets').glob('*.svg'):
        ElementTree.parse(svg)
    require('{{' not in (ROOT / 'README.md').read_text(encoding='utf-8'), 'Unexpanded README placeholder')
    stats = read('stats.json')
    require(stats['total'] == len(papers), 'Statistics out of sync')
    require(stats['supplementary'] == len(supplements), 'Supplement statistics out of sync')
    if ERRORS:
        raise SystemExit('\n'.join(ERRORS))
    print(f'Validated {len(papers)} main records, {len(supplements)} supplements, venue registry, version links, local links and SVG.')

def heading_anchor(text):
    text = re.sub(r'<[^>]*>|[\*_`]', '', text).lower()
    text = ''.join(c for c in text if c.isalnum() or c in '- _')
    return text.replace(' ', '-')

if __name__ == '__main__':
    main()
