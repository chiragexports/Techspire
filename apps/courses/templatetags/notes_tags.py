import re
import html
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    if not dictionary or not isinstance(dictionary, dict):
        return None
    return dictionary.get(key)


@register.filter(name='render_notes')
def render_notes(content):
    """
    Renders structured Markdown notes into rich educational study material HTML with:
    - Styled callouts (Important, Pro Tip, Warning, Interview Insight, Example)
    - Code blocks with syntax highlighting headers & copy buttons
    - Responsive comparison tables
    - Clean typography headings and lists
    """
    if not content:
        return ""

    text = content.strip()
    
    # 1. Process fenced code blocks (```python ... ```)
    def replace_code_block(match):
        lang = match.group(1).strip() if match.group(1) else 'code'
        code_text = match.group(2).strip()
        escaped_code = html.escape(code_text)
        
        display_lang = lang.upper() if lang else 'CODE'
        icon_map = {
            'python': 'fab fa-python text-warning',
            'javascript': 'fab fa-js text-warning',
            'js': 'fab fa-js text-warning',
            'html': 'fab fa-html5 text-danger',
            'css': 'fab fa-css3-alt text-info',
            'sql': 'fas fa-database text-primary',
            'bash': 'fas fa-terminal text-success',
            'sh': 'fas fa-terminal text-success',
            'json': 'fas fa-brackets-curly text-warning',
            'excel': 'fas fa-file-excel text-success',
            'dax': 'fas fa-chart-pie text-warning',
            'prompt': 'fas fa-robot text-info',
        }
        icon_class = icon_map.get(lang.lower(), 'fas fa-code text-primary')

        return f'''
        <div class="ts-code-card my-4 rounded-3 overflow-hidden shadow-sm border">
            <div class="ts-code-header d-flex justify-content-between align-items-center px-3 py-2 bg-dark text-white" style="background-color: #0F172A !important;">
                <span class="small fw-bold d-flex align-items-center gap-2">
                    <i class="{icon_class}"></i> {display_lang}
                </span>
                <button type="button" class="btn btn-sm btn-outline-light py-0 px-2 rounded copy-code-btn" data-code="{html.escape(code_text)}" style="font-size: 0.75rem;">
                    <i class="far fa-copy me-1"></i> Copy
                </button>
            </div>
            <pre class="ts-code-body p-3 m-0 bg-dark text-light overflow-auto" style="background-color: #1E293B !important; font-family: 'Fira Code', 'Courier New', Courier, monospace; font-size: 0.88rem; line-height: 1.6;"><code>{escaped_code}</code></pre>
        </div>
        '''

    text = re.sub(r'```([a-zA-Z0-9_-]*)\n(.*?)```', replace_code_block, text, flags=re.DOTALL)

    # 2. Process Custom Callouts:
    # Pattern: > [!IMPORTANT], > [!TIP], > [!WARNING], > [!INTERVIEW], > [!NOTE], > [!EXAMPLE]
    callout_configs = {
        'IMPORTANT': {
            'class': 'ts-callout-important',
            'icon': 'fas fa-exclamation-circle text-danger',
            'title': 'CRITICAL CONCEPT / IMPORTANT',
            'badge': 'bg-danger text-white'
        },
        'TIP': {
            'class': 'ts-callout-tip',
            'icon': 'fas fa-lightbulb text-warning',
            'title': 'PRO TIP & BEST PRACTICE',
            'badge': 'bg-warning text-dark'
        },
        'WARNING': {
            'class': 'ts-callout-warning',
            'icon': 'fas fa-triangle-exclamation text-warning',
            'title': 'COMMON PITFALL & WARNING',
            'badge': 'bg-warning text-dark'
        },
        'INTERVIEW': {
            'class': 'ts-callout-interview',
            'icon': 'fas fa-briefcase text-primary',
            'title': 'TECHNICAL INTERVIEW INSIGHT',
            'badge': 'bg-primary text-white'
        },
        'NOTE': {
            'class': 'ts-callout-note',
            'icon': 'fas fa-info-circle text-info',
            'title': 'KEY NOTE',
            'badge': 'bg-info text-dark'
        },
        'EXAMPLE': {
            'class': 'ts-callout-example',
            'icon': 'fas fa-code-branch text-success',
            'title': 'REAL-WORLD SCENARIO',
            'badge': 'bg-success text-white'
        },
    }

    def replace_callout(match):
        ctype = match.group(1).upper()
        cbody = match.group(2).strip()
        cfg = callout_configs.get(ctype, callout_configs['NOTE'])
        
        # Format body lines
        body_html = "<br>".join([line.strip() for line in cbody.split("\n") if line.strip()])

        return f'''
        <div class="ts-callout {cfg['class']} p-3 p-md-4 my-3 rounded-3 shadow-sm">
            <div class="d-flex align-items-center gap-2 mb-2 fw-bold text-dark">
                <i class="{cfg['icon']} fs-5"></i>
                <span class="badge {cfg['badge']} rounded-pill text-uppercase px-2 py-1" style="font-size: 0.72rem;">{cfg['title']}</span>
            </div>
            <div class="ts-callout-content text-dark small" style="line-height: 1.7;">
                {body_html}
            </div>
        </div>
        '''

    text = re.sub(r'>\s*\[!(IMPORTANT|TIP|WARNING|INTERVIEW|NOTE|EXAMPLE)\]\s*\n((?:>.*(?:\n|$))+)', lambda m: replace_callout_multiline(m, callout_configs), text, flags=re.IGNORECASE)

    # 3. Process Markdown Tables
    def replace_table(match):
        table_text = match.group(0).strip()
        lines = [l.strip() for l in table_text.split('\n') if l.strip()]
        if len(lines) < 2:
            return table_text
        
        headers = [c.strip() for c in lines[0].strip('|').split('|')]
        # Skip separator line (line 1)
        data_rows = lines[2:] if len(lines) > 2 and '---' in lines[1] else lines[1:]

        table_html = ['<div class="table-responsive my-4"><table class="table table-hover table-bordered shadow-sm rounded-3 overflow-hidden bg-white">']
        table_html.append('<thead class="table-dark" style="background-color: #0F172A !important;"><tr>')
        for h in headers:
            table_html.append(f'<th class="py-2 px-3 fw-bold">{h}</th>')
        table_html.append('</tr></thead><tbody>')

        for row in data_rows:
            cols = [c.strip() for c in row.strip('|').split('|')]
            table_html.append('<tr>')
            for c in cols:
                table_html.append(f'<td class="py-2 px-3">{c}</td>')
            table_html.append('</tr>')

        table_html.append('</tbody></table></div>')
        return "".join(table_html)

    text = re.sub(r'((?:\|[^\n]+\|\n?){2,})', replace_table, text)

    # 4. Headings
    text = re.sub(r'^#### (.*?)$', r'<h5 class="fw-bold text-dark mt-4 mb-2"><i class="fas fa-angle-right text-primary me-2"></i>\1</h5>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*?)$', r'<h4 class="fw-bold text-dark mt-4 mb-3 pb-1 border-bottom"><i class="fas fa-chevron-circle-right text-primary me-2"></i>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h3 class="fw-bold text-primary-dark mt-4 mb-3 pb-2 border-bottom border-2"><i class="fas fa-bookmark text-warning me-2"></i>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h2 class="fw-bold text-dark mt-4 mb-3 pb-2 border-bottom border-primary"><i class="fas fa-graduation-cap text-primary me-2"></i>\1</h2>', text, flags=re.MULTILINE)

    # 5. Bold, Italic, Inline Code
    text = re.sub(r'`([^`]+)`', r'<code class="px-2 py-1 bg-light text-danger rounded small fw-semibold border" style="font-family: monospace;">\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

    # 6. Unordered lists
    def replace_bullet_list(match):
        items = match.group(0).strip().split('\n')
        list_items = []
        for it in items:
            it_clean = re.sub(r'^\s*[-*]\s+', '', it).strip()
            if it_clean:
                list_items.append(f'<li class="mb-2 d-flex align-items-start gap-2"><i class="fas fa-check-circle text-success mt-1 small"></i> <div>{it_clean}</div></li>')
        return f'<ul class="list-unstyled my-3 ps-2">{"".join(list_items)}</ul>'

    text = re.sub(r'((?:^\s*[-*]\s+[^\n]+\n?)+)', replace_bullet_list, text, flags=re.MULTILINE)

    # 7. Horizontal Rules
    text = re.sub(r'^---$', r'<hr class="my-4 border-secondary-subtle">', text, flags=re.MULTILINE)

    # 8. Paragraphs for standalone text lines
    paragraphs = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block.startswith('<h') or block.startswith('<div') or block.startswith('<ul') or block.startswith('<table') or block.startswith('<hr'):
            paragraphs.append(block)
        else:
            paragraphs.append(f'<p class="mb-3 text-secondary" style="line-height: 1.8; font-size: 1.02rem;">{block.replace(chr(10), "<br>")}</p>')

    return mark_safe("".join(paragraphs))


def replace_callout_multiline(match, configs):
    ctype = match.group(1).upper()
    raw_lines = match.group(2).split('\n')
    cleaned_lines = []
    for l in raw_lines:
        line_str = re.sub(r'^\s*>\s?', '', l).strip()
        if line_str:
            cleaned_lines.append(line_str)
    
    cfg = configs.get(ctype, configs['NOTE'])
    body_html = "<br>".join(cleaned_lines)

    return f'''
    <div class="ts-callout {cfg['class']} p-3 p-md-4 my-3 rounded-3 shadow-sm border-start border-4">
        <div class="d-flex align-items-center gap-2 mb-2 fw-bold text-dark">
            <i class="{cfg['icon']} fs-5"></i>
            <span class="badge {cfg['badge']} rounded-pill text-uppercase px-2 py-1" style="font-size: 0.72rem;">{cfg['title']}</span>
        </div>
        <div class="ts-callout-content text-dark" style="line-height: 1.7; font-size: 0.95rem;">
            {body_html}
        </div>
    </div>
    '''
