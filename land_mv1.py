# -*- coding: utf-8 -*-
"""2026-10-20 21:30 老师确认：奇门层彻底数据化——MV1格定义表+A_MEANING+GRADE_LABEL_MAP 全部进JSON
MV1从页面JS提取（键名加引号转JSON），页面改读d.qimen.matrix_def"""
import json, re

# 1. 从页面提取 MV1
s = open('pipeline.html', encoding='utf-8').read()
m = re.search(r'const MV1=\{c:(\[.*?\]),r:(\[.*?\])\};', s, re.S)
assert m, 'MV1未找到'
c_js, r_js = m.group(1), m.group(2)

def js_to_json(js):
    # 键名加引号 + true/false 处理（本数据无布尔）
    return re.sub(r'([{,])([a-zA-Z_][a-zA-Z0-9_]*):', r'\1"\2":', js)

mv1 = {'c': json.loads(js_to_json(c_js)), 'r': json.loads(js_to_json(r_js))}
print(f'MV1提取：{len(mv1["c"])}列 × {len(mv1["r"])}行')
assert len(mv1['r']) == 14, f'行数应为14，实际{len(mv1["r"])}'

# 2. 迁移数据
for f in ['data/pipeline_20261020.json', 'data/pipeline_latest.json']:
    d = json.load(open(f, encoding='utf-8'))
    d['qimen']['matrix_def'] = mv1
    d['qimen']['a_meaning'] = {'2': '多方加速·强烈同向推动', '1': '多方缓速·弱同向推动',
                               '0': '多空平衡·无方向性增量', '-1': '空方减速·弱反向对冲',
                               '-2': '空方急刹·强反向对冲'}
    d['macd']['grade_label_map'] = {"-4": "极弱", "-3": "偏弱", "-2": "偏空", "-1": "略偏空",
                                    "0": "无方向", "1": "略偏多", "2": "偏多", "3": "偏强", "4": "极强"}
    json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f, '→ matrix_def(14行)+a_meaning+grade_label_map 已落地')
