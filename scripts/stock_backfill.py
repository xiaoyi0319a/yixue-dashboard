#!/usr/bin/env python3
"""个股对账批量回填（根治history"待回填"堆积——老师11-23截图批评实证：10行7行空）

职责分工：
  scan  : 扫出待回填清单（code/诊断日/pred/需要次日日期）——agent据此调东财mx拉收盘价
  judge : 纯函数判定 pred定级 vs 实际涨跌幅 → ✅/⚠️/❌（口径唯一权威，可单测）
  write : 把actual/hit写回 diagnose_{code}.json history行（幂等，已填跳过）

口径（七档映射涨跌幅带）：
  ≥+5%偏多 | +2~+5%偏强 | +0.5~+2%中性偏强 | ±0.5%内无方向
  -0.5~-2%中性偏弱 | -2~-5%偏弱 | ≤-5%偏空
判定：实际档==预测→✅ | 相邻档(±1)→⚠️ | 差≥2档或反向→❌ | 预测无方向→带内✅带外⚠️/❌按差档

用法:
  python3 stock_backfill.py scan            # 输出待回填清单JSON
  python3 stock_backfill.py judge 偏弱 -3.2  # → ⚠️/❌/✅
  python3 stock_backfill.py write 002984 20261123 "+5.34%(偏多)" "✅"   # agent拉数后写回
"""
import json, os, sys, glob, re


def sync_archives(code):
    """双写一致性维护：live history 已回填的 actual/hit 同步到该 code 全部日期存档。
    只升级不降级：live 未回填的行不动存档；verification 仅当 live 有值时镜像。"""
    f = os.path.join(DATA, f'diagnose_{code}.json')
    if not os.path.exists(f):
        return
    live = json.load(open(f))
    lhist = {str(h.get('date')): h for h in live.get('history', [])}
    ver = live.get('verification')
    for fn in sorted(glob.glob(os.path.join(DATA, f'diagnose_{code}_*.json'))):
        d = json.load(open(fn))
        changed = False
        for h in d.get('history', []):
            lh = lhist.get(str(h.get('date')))
            if lh is None:
                continue
            if str(lh.get('actual', '')) in ('--', '待回填', ''):
                continue  # live 未回填，不动存档
            for k in ('actual', 'hit'):
                if h.get(k) != lh.get(k):
                    h[k] = lh[k]
                    changed = True
        if ver and d.get('verification') != ver:
            d['verification'] = ver
            changed = True
        if changed:
            json.dump(d, open(fn, 'w'), ensure_ascii=False, indent=1)
            print(f'SYNC {os.path.basename(fn)}')

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
GRADES = ["偏多", "偏强", "中性偏强", "无方向", "中性偏弱", "偏弱", "偏空"]
BANDS = [  # (下界, 上界, 档)
    (5.0, 999.0, "偏多"), (2.0, 5.0, "偏强"), (0.5, 2.0, "中性偏强"),
    (-0.5, 0.5, "无方向"), (-2.0, -0.5, "中性偏弱"), (-5.0, -2.0, "偏弱"),
    (-999.0, -5.0, "偏空"),
]


def pct_to_grade(pct):
    for lo, hi, g in BANDS:
        if lo <= pct < hi:
            return g
    return "无方向"


def judge(pred, pct):
    g = pct_to_grade(pct)
    if pred not in GRADES:
        return "❌", g
    di = GRADES.index(pred)
    dg = GRADES.index(g)
    if pred == "无方向":
        return ("✅", g) if g == "无方向" else (("⚠️", g) if abs(dg - di) == 1 else ("❌", g))
    d = abs(dg - di)
    if d == 0:
        return "✅", g
    if d == 1:
        return "⚠️", g
    return "❌", g


def scan():
    idx_f = os.path.join(DATA, 'diagnoses_index.json')
    out = []
    for s in json.load(open(idx_f)).get('stocks', []):
        code = s['code']
        f = os.path.join(DATA, f'diagnose_{code}.json')
        if not os.path.exists(f):
            continue
        d = json.load(open(f))
        hist = d.get('history', [])
        for h in hist:
            pred = str(h.get('pred', ''))
            actual = str(h.get('actual', ''))
            if pred in GRADES and (actual in ('--', '待回填', '')):
                hd = re.sub(r'\D', '', str(h.get('date', '')))[:8]
                if len(hd) != 8:
                    continue
                from datetime import date, timedelta
                t1 = date(int(hd[:4]), int(hd[4:6]), int(hd[6:8])) + timedelta(days=1)
                out.append({'code': code, 'name': s.get('name', ''),
                            'hist_date': h.get('date'), 'pred': pred,
                            'need_date': t1.strftime('%Y%m%d')})
    return out


def write(code, hist_date, actual_str, hit):
    f = os.path.join(DATA, f'diagnose_{code}.json')
    if not os.path.exists(f):
        print(f'NOFILE {code}')
        return 1
    d = json.load(open(f))
    done = False
    for h in d.get('history', []):
        if str(h.get('date')) == str(hist_date):
            if str(h.get('actual', '')) not in ('--', '待回填', ''):
                print(f'SKIP {code} {hist_date} 已回填')
                sync_archives(code)
                return 0
            h['actual'] = actual_str
            h['hit'] = hit
            done = True
    if not done:
        print(f'NOROW {code} {hist_date}')
        return 1
    hits = [h.get('hit') for h in d.get('history', [])
            if h.get('hit') in ('✅', '⚠️', '❌')]
    d['verification'] = {
        'hit': hit,
        'note': f'批量回填：历史{len(hits)}次对账 ' +
                f"✅{hits.count('✅')}/⚠️{hits.count('⚠️')}/❌{hits.count('❌')}"
    }
    json.dump(d, open(f, 'w'), ensure_ascii=False, indent=1)
    print(f'OK {code} {hist_date} → {actual_str} {hit}')
    sync_archives(code)
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'scan':
        r = scan()
        print(json.dumps(r, ensure_ascii=False, indent=1))
        print(f'TOTAL {len(r)}')
    elif cmd == 'judge' and len(sys.argv) >= 4:
        hit, g = judge(sys.argv[2], float(sys.argv[3]))
        print(hit)
    elif cmd == 'write' and len(sys.argv) >= 6:
        sys.exit(write(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
    else:
        print(__doc__)
        sys.exit(1)
