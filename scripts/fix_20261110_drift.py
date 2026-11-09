#!/usr/bin/env python3
"""2026-11-10 schema漂移修复：G9x全局行命名规范化 + fusion.path双写 + 禁null键省略。
依据=data/schema/pipeline.schema.json（修复模式=同步cron Step1.5门禁拦截话术规定的唯一合法修复路径）。
留痕：commit message 引用本脚本。"""
import json

def fix(path):
    d = json.load(open(path, encoding='utf-8'))
    n = 0
    for it in d.get('matrix_drop', []):
        if isinstance(it, dict) and 'read' not in it:
            g = str(it.get('g', ''))
            cell = str(it.get('cell', ''))
            if g.startswith('G9') and '×' not in cell:
                it['cell'] = '全局×' + cell
                n += 1
    if 'path' not in (d.get('fusion') or {}) and d.get('path'):
        d['fusion']['path'] = d['path']
    removed = []
    for k in ['four_slots_4p', 'strong_bottom_note']:
        if k in d and d[k] is None:
            del d[k]
            removed.append(k)
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'{path}: 规范化{n}个G9x格, fusion.path={d["fusion"].get("path")}, 删null键{removed}')

if __name__ == '__main__':
    fix('/root/.openclaw/workspace/yixue-dashboard/data/pipeline_20261110.json')
    fix('/root/.openclaw/workspace/yixue-dashboard/data/pipeline_latest.json')
