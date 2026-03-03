import re

html_chunk = '<div class="chapter-footnotes"><div class="footnote">\\n\\n<ol>'
html_chunk = html_chunk.replace('\\n', '\n')

def repl_ol(m):
    return f'{m.group(1)} start="13"{m.group(2)}'

html2 = re.sub(
    r'(<div class="footnote"[^>]*>.*?<ol)([^>]*>)',
    repl_ol,
    html_chunk,
    count=1,
    flags=re.IGNORECASE | re.DOTALL
)

print(html2)
