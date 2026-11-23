#!/usr/bin/env python3
"""V4.7补跑队列扫描器（根治"承诺悬空"机制层）

用法:
  python3 v47_queue.py scan          # 扫描队列，输出待补跑清单（exit0=队列空/exit2=有队列）
  python3 v47_queue.py done <code>   # 标记某只已完成（补跑session成功后调用）
  python3 v47_queue.py state         # 查看进度状态文件

队列判定: diagnose_{code}.json 中 report_update.trigger 含 "V4.7" 且 report.standing 含 "现场版"
状态文件: data/v47_backfill_state.json  {code: {status: pending/done, date, report_date}}
"""
import json, sys, glob, os, re

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
STATE_FILE = os.path.join(DATA, 'v47_backfill_state.json')


def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}


def save_state(s):
    json.dump(s, open(STATE_FILE, 'w'), ensure_ascii=False, indent=1)


def find_queue():
    """扫描待补跑队列"""
    queue = []
    for f in sorted(glob.glob(os.path.join(DATA, 'diagnose_*.json'))):
        base = os.path.basename(f)
        if re.match(r'diagnose_\d{6}_\d{8}\.json$', base):  # 跳过日期存档
            continue
        try:
            d = json.load(open(f))
        except Exception:
            continue
        ru = d.get('matrix_L1', {}).get('report_update', {})
        report = d.get('matrix_L1', {}).get('report', {})
        trigger = str(ru.get('trigger', ''))
        standing = str(report.get('standing', ''))
        if 'V4.7' in trigger and '现场版' in standing:
            code = d.get('stock', '').split()[0]
            queue.append({
                'code': code,
                'name': d.get('stock', ''),
                'date': d.get('date'),
                'trigger': trigger,
            })
    return queue


def cmd_scan():
    state = load_state()
    queue = find_queue()
    pending = [q for q in queue if state.get(q['code'], {}).get('status') != 'done']
    if not pending:
        print('QUEUE_EMPTY')
        return 0
    print(f'QUEUE {len(pending)}只待补跑:')
    for q in pending:
        print(f"  {q['code']} {q['name']} (诊断日{q['date']})")
    return 2


def cmd_done(code):
    state = load_state()
    state[code] = {'status': 'done', 'done_at': 'auto'}
    save_state(state)
    # 清掉JSON里的现场版标记（补跑完成信号）
    import pathlib
    for f in glob.glob(os.path.join(DATA, f'diagnose_{code}.json')):
        d = json.load(open(f))
        st = d.get('matrix_L1', {}).get('report', {}).get('standing', '')
        if '现场版' in st:
            d['matrix_L1']['report']['standing'] = st.replace('（现场版，V4.7明早补跑）', '').replace('(现场版，V4.7明早补跑)', '').replace('（现场版', '').strip()
            json.dump(d, open(f, 'w'), ensure_ascii=False, indent=1)
            print(f'{code}: 现场版标记已清除')
    print(f'{code}: marked done')
    return 0


def cmd_state():
    print(json.dumps(load_state(), ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'scan':
        sys.exit(cmd_scan())
    elif cmd == 'done' and len(sys.argv) >= 3:
        sys.exit(cmd_done(sys.argv[2]))
    elif cmd == 'state':
        sys.exit(cmd_state())
    else:
        print(__doc__)
        sys.exit(1)
