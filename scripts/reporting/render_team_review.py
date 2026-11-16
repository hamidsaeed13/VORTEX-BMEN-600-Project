"""Render the local review as a standalone HTML document with contributor tabs."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'docs/reviews/TEAM_REVIEW.md'


def inline(value):
    value = html.escape(value)
    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', value)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)


def render(text):
    lines = text.splitlines()
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('```'):
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                block.append(lines[i]); i += 1
            result.append('<pre><code>' + html.escape('\n'.join(block)) + '</code></pre>')
            i += 1
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    tag = 'th' if not rows else 'td'
                    rows.append('<tr>' + ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells) + '</tr>')
                i += 1
            result.append('<div class="table"><table>' + ''.join(rows) + '</table></div>')
        elif line.startswith('## '):
            result.append('<h2>' + inline(line[3:]) + '</h2>'); i += 1
        elif line.startswith('- '):
            result.append('<p class="item">• ' + inline(line[2:]) + '</p>'); i += 1
        else:
            para = []
            quote = line.startswith('>')
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(('## ', '|', '```', '- ')):
                para.append(lines[i].lstrip('> ')); i += 1
            tag = 'blockquote' if quote else 'p'
            result.append(f'<{tag}>' + inline(' '.join(para)) + f'</{tag}>')
    return '\n'.join(result)


def main():
    source = SOURCE.read_text()
    headings = ['Ella — PRs 13 and 14', 'Setayesh — PR 15',
                'Shared decisions before integration', 'Proposed patches and validation']
    labels = ['Ella', 'Setayesh', 'Shared decisions', 'Fixes & validation']
    panels = []
    for i, heading in enumerate(headings):
        start = source.index('## ' + heading)
        end = source.index('## ' + headings[i+1]) if i+1 < len(headings) else len(source)
        panels.append(f'<section id="panel{i}" role="tabpanel" aria-labelledby="tab{i}" '
                      f'{"hidden" if i else ""}>' + render(source[start:end]) + '</section>')
    tabs = ''.join(f'<button id="tab{i}" role="tab" aria-controls="panel{i}" '
                   f'aria-selected="{str(i == 0).lower()}" onclick="selectTab({i})">{html.escape(label)}</button>'
                   for i, label in enumerate(labels))
    document = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Team contribution review</title>
<style>
:root{color-scheme:light dark;font-family:system-ui,sans-serif;line-height:1.55}
body{max-width:1200px;margin:32px auto;padding:0 24px}h1{margin-bottom:6px}
.muted{opacity:.75}.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:24px 0}
button{font:inherit;padding:10px 18px;border:1px solid #8888;border-radius:8px;cursor:pointer}
button[aria-selected=true]{background:#2167b0;color:white;border-color:#2167b0}
table{border-collapse:collapse;width:100%;font-size:.92rem}th,td{border:1px solid #8886;padding:12px;vertical-align:top;text-align:left}
th{background:#8882}.table{overflow-x:auto}a{color:light-dark(#165aab,#88baff)}
code{font-size:.9em;background:#8882;border-radius:3px;padding:2px 4px}pre{padding:16px;background:#8881;overflow:auto}
blockquote{border-left:3px solid #2167b0;margin-left:0;padding:8px 18px;background:#8881}
.notice{padding:14px 18px;border:1px solid #8886;border-radius:8px}
@media print{section[hidden]{display:block!important}.tabs{display:none}}
</style><h1>Team contribution review</h1><p class="muted">November 16, 2026 · Local review of PRs 13–15</p>
<p class="notice">The reported principal counts and Ella’s main AUROCs reproduced.
The tabs distinguish fixes from study-design decisions. Proposed patches were tested locally;
no changes or messages have been sent to the contributors’ branches.</p>
<a href="TEAM_REVIEW.md">Full Markdown review</a>
<nav class="tabs" role="tablist" aria-label="Review sections">''' + tabs + '</nav>' + '\n'.join(panels) + '''
<script>
function selectTab(index){document.querySelectorAll('[role=tab]').forEach((tab,i)=>{
tab.setAttribute('aria-selected',String(i===index));document.getElementById('panel'+i).hidden=i!==index;});}
document.querySelectorAll('[role=tab]').forEach((tab,i)=>tab.addEventListener('keydown',event=>{
if(event.key==='ArrowRight'||event.key==='ArrowLeft'){
event.preventDefault();const next=(i+(event.key==='ArrowRight'?1:3))%4;
selectTab(next);document.getElementById('tab'+next).focus();}}));
</script></html>'''
    SOURCE.with_suffix('.html').write_text(document)


if __name__ == '__main__':
    main()
