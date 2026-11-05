#!/usr/bin/env python3
"""个股诊断收尾自动验证器（挂 Step 7.5——清单自动验证，禁止人工勾选）
用法: python3 scripts/verify_diagnose.py <code> <YYYY-MM-DD>
exit 0=全过可push, exit 1=拦截（错误清单=修复指引）
设计原则：今天两次事故（漏push/view_state漏同步）的结构性防线——所有检查自动断言，不靠记忆。
"""
import sys, json, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
GRADES = ["偏多", "偏强", "中性偏强", "无方向", "中性偏弱", "偏弱", "偏空"]


def err_list():
    return []


def check_files(code, date, errs):
    a = f"{DATA}/diagnose_{code}.json"
    b = f"{DATA}/diagnose_{code}_{date.replace('-', '')}.json"
    if not os.path.exists(a):
        errs.append(f"缺文件 {a}")
        return None
    if not os.path.exists(b):
        errs.append(f"缺日期存档 {b}")
    da = json.load(open(a, encoding="utf-8"))
    if os.path.exists(b):
        db = json.load(open(b, encoding="utf-8"))
        if da != db:
            errs.append("diagnose_{code}.json 与日期存档内容不一致（双写撕裂）")
    return da


def check_dates(d, date, errs):
    if d.get("date") != date:
        errs.append(f"顶层date={d.get('date')} ≠ 入参{date}")
    meta = d.get("diagnose_meta", {})
    if str(meta.get("snapshot_time", ""))[:10] != date:
        errs.append(f"diagnose_meta.snapshot_time={meta.get('snapshot_time')} 非当日")
    hist = d.get("history", [])
    if hist and hist[-1].get("date") != date:
        errs.append(f"history末行date={hist[-1].get('date')} ≠ 当日（未追加今天）")
    tl = d.get("timeline", [])
    if tl and tl[-1].get("date") != date:
        errs.append(f"timeline末行date={tl[-1].get('date')} ≠ 当日")


def check_gate(d, errs):
    if not d.get("matrix_L1", {}).get("gene", {}).get("pattern"):
        errs.append("门禁①基因pattern空")
    cur = d.get("matrix_grid", {}).get("current", {})
    z, g = cur.get("z"), cur.get("g")
    if not (isinstance(z, int) and 0 <= z <= 4):
        errs.append(f"门禁②matrix_grid.z非法:{z}")
    if not (isinstance(g, int) and 0 <= g <= 6):
        errs.append(f"门禁②matrix_grid.g非法:{g}")
    direction = d.get("fusion", {}).get("direction")
    if direction not in GRADES:
        errs.append(f"门禁③direction非7档:{direction}")
    rep = d.get("matrix_L1", {}).get("report")
    if not rep:
        errs.append("门禁④report=null")
    elif "现场版" in str(rep.get("date", "")) and rep.get("weight_ranking"):
        errs.append("门禁④report为现场版且三字段非null（7.0b硬凑拦截）")


def check_schema(d, errs):
    L0 = d.get("matrix_L0", {})
    for k in ("v0", "a_macd"):
        if not isinstance(L0.get(k), dict):
            errs.append(f"schema:matrix_L0.{k}非对象封装")
    if not isinstance(L0.get("cell"), dict):
        errs.append("schema:matrix_L0.cell非对象")
    fu = d.get("fusion", {})
    if not fu.get("confidence"):
        errs.append("schema:fusion.confidence空")
    if not fu.get("form"):
        errs.append("schema:fusion.form空")
    vg = d.get("view_gene", {})
    if not isinstance(vg.get("patterns"), list) or not vg.get("patterns"):
        errs.append("schema:view_gene.patterns空")
    else:
        tot = sum(p.get("total_vars", 0) for p in vg["patterns"])
        if vg.get("total_vars") != tot:
            errs.append(f"schema:view_gene.total_vars({vg.get('total_vars')})≠各模式之和({tot})")
    vs = d.get("view_state", {})
    for k in ("zones", "judgment", "transitions"):
        if not isinstance(vs.get(k), list):
            errs.append(f"schema:view_state.{k}非数组")
    if not (isinstance(vs.get("current_idx"), int) and 0 <= vs["current_idx"] <= 4):
        errs.append(f"schema:view_state.current_idx非法:{vs.get('current_idx')}")
    dc = d.get("daily_chain", [])
    if not isinstance(dc, list) or len(dc) != 6:
        errs.append(f"schema:daily_chain非6节点({len(dc) if isinstance(dc,list) else type(dc)})")
    for i, h in enumerate(d.get("history", [])):
        for k in ("v0", "a_macd", "q_bias", "pred", "hit", "cell"):
            if k not in h:
                errs.append(f"schema:history[{i}]缺{k}")
    pr = d.get("prev_diagnose")
    if pr is not None and not isinstance(pr.get("prev_z"), int):
        errs.append("schema:prev_diagnose缺prev_z数值")
    vd = d.get("verdict", {})
    if not vd.get("summary"):
        errs.append("schema:verdict.summary空")
    else:
        dim = vd.get("dims_oneliner", {})
        for k in ("gene", "state", "report", "forecast"):
            if not dim.get(k):
                errs.append(f"schema:verdict.dims_oneliner缺{k}")


def check_consistency(d, errs):
    """⭐状态一致性（11-05 view_state漏同步事故防线）——同一状态多字段必须相等"""
    z_grid = d["matrix_grid"]["current"]["z"]
    g_grid = d["matrix_grid"]["current"]["g"]
    vs = d.get("view_state", {})
    if isinstance(vs.get("current_idx"), int) and vs["current_idx"] != z_grid:
        errs.append(
            f"⭐一致性:view_state.current_idx({vs['current_idx']}) ≠ matrix_grid.z({z_grid})"
            " ——区间蓝框与矩阵坐标撕裂（18:47事故同款）"
        )
    direction = d.get("fusion", {}).get("direction")
    if direction and isinstance(g_grid, int) and g_grid < len(GRADES):
        expect = GRADES[g_grid]
        if direction != expect:
            errs.append(f"⭐一致性:fusion.direction({direction}) ≠ grades[g]({expect})")
    # zones[current_idx] 的 name 应与 matrix_grid.current.label 的区间名对应（宽松校验：横盘整理↔横盘整理区）
    label = d["matrix_grid"]["current"].get("label", "")
    zones = vs.get("zones", [])
    if zones and isinstance(vs.get("current_idx"), int) and vs["current_idx"] < len(zones):
        zone_name = zones[vs["current_idx"]].get("name", "")
        core = zone_name.replace("区", "")
        if core and core not in label:
            errs.append(f"⭐一致性:matrix_grid.label({label})不含当前区名({zone_name})")


def check_judgment_fresh(d, code, date, errs):
    """judgment 不允许残留任何历史快照价（18:47 view_state旧值事故防线——锚点=全历史快照价集合）"""
    import re
    hist_prices = set()
    for fn in os.listdir(DATA):
        m = re.match(rf"diagnose_{re.escape(code)}_(\d{{8}})\.json", fn)
        if m and m.group(1) != date.replace("-", ""):
            try:
                p2 = json.load(open(os.path.join(DATA, fn), encoding="utf-8"))
                sp = p2.get("diagnose_meta", {}).get("snapshot_price")
                if sp is not None:
                    hist_prices.add(str(sp))
            except Exception:
                pass
    if not hist_prices:
        return
    meta = d.get("diagnose_meta", {})
    new_price = str(meta.get("snapshot_price"))
    for j in d.get("view_state", {}).get("judgment", []):
        v = str(j.get("value", ""))
        hits = [hp for hp in hist_prices if hp in v and new_price not in v]
        if hits:
            errs.append(
                f"⭐新鲜度:judgment[{j.get('dim')}]含历史快照价{hits}——疑似旧数据残留"
            )


def check_git(code, errs):
    r = subprocess.run(
        ["git", "-C", ROOT, "log", "origin/gh-pages..gh-pages", "--oneline",
         "--", f"data/diagnose_{code}"],
        capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        n = len(r.stdout.strip().splitlines())
        errs.append(f"⭐git:{code}诊断数据有{n}个commit未push——线上还是旧数据（18:37事故同款）")


def main():
    if len(sys.argv) < 3:
        print("用法: verify_diagnose.py <code> <YYYY-MM-DD>")
        sys.exit(2)
    code, date = sys.argv[1], sys.argv[2]
    errs = []
    d = check_files(code, date, errs)
    if d:
        check_dates(d, date, errs)
        check_gate(d, errs)
        check_schema(d, errs)
        check_consistency(d, errs)
        check_judgment_fresh(d, code, date, errs)
    check_git(code, errs)
    if errs:
        print(f"❌ verify_diagnose 拦截 {len(errs)} 项：")
        for e in errs:
            print(f"  ✗ {e}")
        print("\n全部修复后重跑本脚本，exit 0 才可 push。")
        sys.exit(1)
    print(f"✅ verify_diagnose 全过（{code} {date}）——可 push")
    sys.exit(0)


if __name__ == "__main__":
    main()
