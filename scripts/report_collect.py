#!/usr/bin/env python3
"""报告库自动归集器（根治"报告产出但页面不可见"——reports.json手动维护必漏）

数据源（两源，均为个股分析工作流V4.6的标准产出落盘点，原工作流零改动）：
  SRC1: /root/.openclaw/workspace/memory/个股分析/{code}_个股分析_{YYYYMMDD}.md
  SRC2: yixue-dashboard/reports/*.md

收录动作（幂等，可反复跑）：
  ① _reports/{code}.md 不存在 → 复制+补Jekyll YAML头（已有头直接用）
  ② reports.json 无该code 或 条目date < 文件date → 开头插入/更新条目（一code一条，最新覆盖）
  同code多份取最新date——Jekyll permalink /stock-:name.html 一code一页，天然如此。

用法:
  python3 report_collect.py            # dry-run，输出将收录清单
  python3 report_collect.py --exec     # 实际执行文件操作（git add/commit/push 由调用方负责）
"""
import json, re, os, sys, shutil, glob

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SRC1 = os.path.join(WS, 'memory', '个股分析')
SRC2 = os.path.join(ROOT, 'reports')
DST = os.path.join(ROOT, '_reports')
JSON_F = os.path.join(ROOT, 'reports.json')
INDEX_F = os.path.join(WS, 'memory', '个股诊断档案', 'INDEX.json')

TPL_HEAD = """---
code: {code}
title: {title}
subtitle: {subtitle}
date: {date}
version: {version}
analyst: 小羿
---

"""


def norm_date(s):
    s = re.sub(r'\D', '', str(s))[:8]
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if len(s) == 8 else "2026-01-01"


def extract_code_date(path):
    base = os.path.basename(path)
    # 格式A: {code}_个股分析_{YYYYMMDD}.md / {名字}_{code}_个股分析_{YYYYMMDD}.md
    m = re.search(r'(\d{6})_个股分析_(\d{8})', base)
    if m:
        return m.group(1), norm_date(m.group(2))
    # 格式B: {YYYYMMDD}-{code}-完整报告.md（3月批次）
    m = re.search(r'(\d{8})-(\d{6})-', base)
    if m:
        return m.group(2), norm_date(m.group(1))
    return None, None


def extract_tags_from_report(text):
    """从报告内容自动提取标签：subtitle 分片 + 价值等级"""
    tags = []
    # 1. 从 YAML subtitle 提取（· 或 ：分隔，取前3-4个核心短语）
    m = re.search(r'^subtitle:\s*["\']?(.+?)["\']?\s*$', text, re.M)
    if m:
        sub = m.group(1).strip()
        if sub and sub != '待补充':
            # 按 · 或 ： 分隔
            parts = re.split(r'[·：:，,]', sub)
            for p in parts:
                p = p.strip().strip('·')
                if p and len(p) > 2 and not p.startswith('待'):
                    # 截断过长的片段
                    if len(p) > 15:
                        p = p[:15]
                    tags.append(p)
                if len(tags) >= 4:
                    break
    # 2. 从正文提取价值等级
    m2 = re.search(r'\*\*投资价值(?:评估)?\*\*\s*[：:]\s*([高低无][-中高低]*价值)', text)
    if m2:
        tags.append(m2.group(1))
    else:
        # 宽松匹配
        m3 = re.search(r'投资价值[：:]\s*([高低无][-中高低]*价值)', text)
        if m3:
            tags.append(m3.group(1))
    return tags if tags else ["待补充", "待评级"]


def load_name_map():
    try:
        idx = json.load(open(INDEX_F))
        return {k: v.get('name', k) for k, v in idx.items() if isinstance(v, dict)}
    except Exception:
        return {}


def has_yaml(text):
    return text.lstrip().startswith('---')


def ensure_yaml(text, code, date, names):
    if has_yaml(text):
        return text
    title = names.get(code, code)
    body = text
    h1 = re.search(r'^#\s+(.+)$', text, re.M)
    if h1:
        body = text.replace(h1.group(0), '', 1).lstrip()
    return TPL_HEAD.format(code=code, title=title, subtitle='待补充',
                           date=date, version='V4.6') + body


def scan_sources():
    out = {}
    for src in (SRC1, SRC2):
        for f in glob.glob(os.path.join(src, '*.md')):
            code, date = extract_code_date(f)
            if not code:
                continue
            if code not in out or out[code]['date'] < date:
                out[code] = {'file': f, 'date': date}
    return out


def main():
    exec_mode = '--exec' in sys.argv
    names = load_name_map()
    items = json.load(open(JSON_F)) if os.path.exists(JSON_F) else []
    by_code = {str(e.get('code')): e for e in items}

    sources = scan_sources()
    actions = []
    for code, info in sorted(sources.items()):
        f, date = info['file'], info['date']
        existing = by_code.get(code)
        need_json = existing is None or str(existing.get('date', '')) < date
        dst_md = os.path.join(DST, f'{code}.md')
        need_md = not os.path.exists(dst_md)
        if need_json or need_md:
            actions.append((code, date, f, need_md, need_json,
                            existing.get('date') if existing else None))

    print(f'扫描到产出物 {len(sources)} 份（SRC1={len(glob.glob(os.path.join(SRC1,"*.md")))} SRC2={len(glob.glob(os.path.join(SRC2,"*.md")))}），待收录 {len(actions)} 只:')
    for code, date, f, need_md, need_json, old_date in actions:
        flags = ('[新建MD]' if need_md else '') + ('[更新JSON]' if need_json else '')
        print(f'  {code} {names.get(code, "")} {date} {flags}  旧条目:{old_date}')

    if not exec_mode:
        print('\nDRY-RUN：加 --exec 执行')
        return 0
    if not actions:
        print('QUEUE_EMPTY')
        return 0

    for code, date, f, need_md, need_json, old_date in actions:
        dst_md = os.path.join(DST, f'{code}.md')
        if need_md:
            text = open(f, encoding='utf-8').read()
            open(dst_md, 'w', encoding='utf-8').write(
                ensure_yaml(text, code, date, names))
        if need_json:
            # 从报告内容自动提取标签
            text = open(dst_md, encoding='utf-8').read()
            auto_tags = extract_tags_from_report(text)
            entry = {"code": code, "name": names.get(code, code), "date": date,
                     "file": f"/yixue-dashboard/stock-{code}.html",
                     "tags": auto_tags}
            if code in by_code:
                items[items.index(by_code[code])] = entry
            else:
                items.insert(0, entry)
            by_code[code] = entry
    json.dump(items, open(JSON_F, 'w'), ensure_ascii=False, indent=2)
    print(f'EXEC_DONE 收录{len(actions)}只，reports.json现{len(items)}条')
    return 0


if __name__ == '__main__':
    sys.exit(main())
