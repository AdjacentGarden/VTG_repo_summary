#!/usr/bin/env python3
"""Build repository indexes from checked-in metadata. No network or dependencies."""
import argparse
import csv
import io
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED = '2026-10-05'
GROUPS = ['综述与基准', '经典模型', '统一定位与高亮', '多模态大模型', '长视频与训练自由', '强化学习与新任务']

def load(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

def esc(text):
    return str(text).replace('|', '\\|').replace('\n', ' ').replace('[', '\\[').replace(']', '\\]')

def links(p):
    out = [f"[Paper]({p['paper_url']})"]
    if p.get('arxiv_url') and p['arxiv_url'] != p['paper_url']:
        out.append(f"[arXiv]({p['arxiv_url']})")
    if p.get('code_url'):
        out.append(f"[Code]({p['code_url']})")
    return ' · '.join(out)

def table(papers, anchors=False):
    lines = ['| 年份 | 会议／期刊 | 论文 | 方向 | 资源 |', '| --- | --- | --- | --- | --- |']
    for p in papers:
        scope = '（时序证据 QA）' if p.get('scope') == 'temporal_evidence_qa' else ''
        anchor = f'<a id="{p["id"]}"></a>' if anchors else ''
        lines.append(f"| {p['year']} | {esc(p['venue'])} · {p['ccf_grade']} | {anchor}[{esc(p['title'])}]({p['paper_url']}){scope} | {esc('、'.join(p['tags']))} | {links(p)} |")
    return '\n'.join(lines) + '\n'

def bibvalue(s):
    # Preserve Unicode names; escape only TeX-reserved punctuation.
    s = s.replace('\\', r'\textbackslash{}')
    for char, replacement in [('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('_', r'\_')]:
        s = s.replace(char, replacement)
    return s.replace('{', '').replace('}', '').replace('\n', ' ')

def build():
    papers = sorted(load('papers.json'), key=lambda p: (-p['year'], p['venue'], p['title'].lower()))
    supplements = sorted(load('supplementary.json'), key=lambda p: (-p['year'], p['title'].lower()))
    stats = {
        'checked_at': CHECKED, 'total': len(papers),
        'ccf_grades': dict(sorted(Counter(p['ccf_grade'] for p in papers).items())),
        'publication_types': dict(sorted(Counter(p['publication_type'] for p in papers).items())),
        'by_year': dict(sorted(Counter(str(p['year']) for p in papers).items(), reverse=True)),
        'by_venue': dict(sorted(Counter(p['venue'] for p in papers).items())),
        'scope': dict(sorted(Counter(p['scope'] for p in papers).items())),
        'with_code_link': sum(bool(p.get('code_url')) for p in papers),
        'with_chinese_summary': sum(bool(p.get('summary_zh')) for p in papers),
        'supplementary': len(supplements),
    }
    out = {'data/stats.json': json.dumps(stats, ensure_ascii=False, indent=2) + '\n'}
    nav = '[首页](../README.md) · [年份](by-year.md) · [会议与期刊](by-venue.md) · [方向](by-topic.md) · [补充](supplementary.md)\n\n'
    note = '分级按 CCF 第七版（2026）；条目统计包含独立会议版／期刊版以及标注的相关数据、综述和时序证据任务。标签是导航信息；出版类型核验程度与来源见 [覆盖说明](../docs/coverage.md)。\n\n'
    years = sorted({p['year'] for p in papers}, reverse=True)
    s = '# 按年份浏览\n\n' + nav + note
    s += ' · '.join(f'[{y}](#year-{y})' for y in years) + '\n\n'
    for y in years:
        xs = [p for p in papers if p['year'] == y]
        s += f'<a id="year-{y}"></a>\n\n## {y}（{len(xs)}）\n\n' + table(xs, anchors=True) + '\n'
    out['papers/by-year.md'] = s
    s = '# 按会议与期刊浏览\n\n' + nav + note
    for kind, name in [('conference', '会议'), ('journal', '期刊')]:
        s += f'## {name}\n\n'
        for v in sorted({p['venue'] for p in papers if p['publication_type'] == kind}):
            xs = [p for p in papers if p['venue'] == v and p['publication_type'] == kind]
            s += f'### {v} · CCF {xs[0]["ccf_grade"]}（{len(xs)}）\n\n' + table(xs) + '\n'
    out['papers/by-venue.md'] = s
    s = '# 按研究方向浏览\n\n' + nav + note + '一篇论文可属于多个方向，因此本页各分类数量不能相加作为论文总数。`tag_basis=title` 表示标题推断，`abstract_reviewed` 表示经摘要／原始介绍核实。\n\n'
    for tag in sorted({t for p in papers for t in p['tags']}):
        xs = [p for p in papers if tag in p['tags']]
        s += f'## {tag}（{len(xs)}）\n\n' + table(xs) + '\n'
    out['papers/by-topic.md'] = s
    s = '# 补充论文与发表状态\n\n' + nav + '这些记录不计入 CCF A/B 主索引。作者项目的录用声明不会自动替代正式会议录。\n\n'
    for p in supplements:
        s += f"### {esc(p.get('display_name', p['title']))}\n\n**{esc(p['title'])}**\n\n{p['year']} · {p['status']}\n\n{links(p)}\n\n"
        if p.get('summary_zh'):
            s += p['summary_zh'] + '\n\n'
        s += p.get('exclusion_reason', '') + '\n\n'
        if p.get('eligibility_source'):
            s += f"[出版类型依据]({p['eligibility_source']})\n\n"
    out['papers/supplementary.md'] = s
    stream = io.StringIO(newline='')
    fields = ['id', 'year', 'venue', 'ccf_grade', 'publication_type', 'scope', 'title', 'authors', 'doi', 'paper_url', 'arxiv_url', 'code_url', 'tags', 'tag_basis', 'summary_zh', 'pages', 'format_status', 'source_urls', 'checked_at']
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    for p in papers:
        writer.writerow({k: ' ; '.join(p.get(k, [])) if isinstance(p.get(k), list) else p.get(k, '') for k in fields})
    out['papers/papers.csv'] = stream.getvalue()
    bibs = []
    for p in papers:
        kind = 'article' if p['publication_type'] == 'journal' else 'inproceedings'
        fields = {'title': p['title'], 'author': ' and '.join(p['authors']), 'year': str(p['year']), 'journal' if kind == 'article' else 'booktitle': p['venue'], 'url': p['paper_url']}
        if p['doi']: fields['doi'] = p['doi']
        if p.get('pages'): fields['pages'] = p['pages'].replace('-', '--')
        if p.get('arxiv_url'): fields['note'] = 'Preprint: ' + p['arxiv_url']
        bibs.append('@' + kind + '{' + p['id'] + ',\n' + ',\n'.join('  ' + k + ' = {' + bibvalue(v) + '}' for k, v in fields.items() if v) + '\n}\n')
    out['papers/references.bib'] = '\n'.join(bibs)
    a, b = stats['ccf_grades'].get('A', 0), stats['ccf_grades'].get('B', 0)
    count = f"**主索引 {len(papers)} 条**：CCF A {a} 条、CCF B {b} 条；会议 {stats['publication_types'].get('conference',0)} 条、期刊 {stats['publication_types'].get('journal',0)} 条。另有 {len(supplements)} 条补充记录；{stats['with_chinese_summary']} 条主索引记录提供中文方法／资源摘要，{stats['with_code_link']} 条关联已核实的代码入口。\n\n"
    count += '| 年份 | 条目 |\n| --- | --- |\n' + '\n'.join(f'| [{y}](papers/by-year.md#year-{y}) | {stats["by_year"][str(y)]} |' for y in years) + '\n'
    cards = ''
    for group in GROUPS:
        xs = [p for p in papers if p.get('card_group') == group]
        cards += f'### {group}\n\n'
        for p in sorted(xs, key=lambda p: (p['year'], p['venue'], p['title'])):
            cards += f"- **[{p.get('display_name', p['title'])}]({p['paper_url']})** · {p['venue']} {p['year']} · CCF {p['ccf_grade']}\n\n  {p['summary_zh']}\n\n  {links(p)} · [索引记录](papers/by-year.md#{p['id']})\n\n"
    template = (ROOT / 'docs' / 'README.template.md.in').read_text(encoding='utf-8')
    out['README.md'] = template.replace('{{STATISTICS}}', count).replace('{{PAPER_CARDS}}', cards)
    return {name: content.rstrip("\n") + "\n" for name, content in out.items()}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail when generated files differ; do not write')
    args = parser.parse_args()
    mismatches = []
    for relative, content in build().items():
        path = ROOT / relative
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                mismatches.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
    if mismatches:
        raise SystemExit('Stale generated files: ' + ', '.join(mismatches))
    print('Generated files are current.' if args.check else 'Catalogue generated.')

if __name__ == '__main__':
    main()
