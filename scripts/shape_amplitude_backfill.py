#!/usr/bin/env python3
"""shape实体/振幅幅度回填（11-26退化数据修复·一次性）
口径：amplitude_grade 取当日 volatility.range；body_grade 近十字净位移口径0.3~0.8%（v_final=-1无方向·拉锯震荡）
"""
import json, sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix(path):
    d = json.load(open(path, encoding='utf-8'))
    s = d.get('shape') or {}
    changed = []
    if s.get('amplitude_grade') in ('中', '小', '大') or (s.get('amplitude_grade') and '%' not in str(s['amplitude_grade'])):
        rng = (d.get('volatility') or {}).get('range', '0.8%~1.6%')
        rng = rng.replace('%~', '~').replace('%', '%')
        s['amplitude_grade'] = f"中档（{rng}）"
        changed.append('amplitude_grade')
    if s.get('body_grade') in ('中', '小', '大') or (s.get('body_grade') and '%' not in str(s['body_grade'])):
        s['body_grade'] = "实体小（近十字·净位移预估0.3~0.8%）"
        changed.append('body_grade')
    if changed:
        json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"✅ {os.path.basename(path)} 回填 {','.join(changed)} → body={s['body_grade']} | amp={s['amplitude_grade']}")
    else:
        print(f"— {os.path.basename(path)} 无需回填")
    return changed

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, 'data/pipeline_20261126.json')
    fix(target)
