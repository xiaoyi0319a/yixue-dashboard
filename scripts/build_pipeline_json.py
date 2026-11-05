#!/usr/bin/env python3
"""预测管线数据组装器（灰度期=影子模式主力，切换后=主生成器）
输入: 槽位JSON（LLM只产可变值，面≈全量1/5） + 本文件内嵌常量模板
输出: 全量 pipeline JSON（必须过schema契约+算术一致性校验才落盘）
用法: python3 scripts/build_pipeline_json.py data/slots_YYYYMMDD.json [--out data/pipeline_shadow_YYYYMMDD.json]
"""
import sys, json, os, copy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============ 常量模板（每天不变块——LLM直写时这些就是漂移/偷懒重灾区，收归代码） ============
CONSTANTS = {
    "schema_version": "2.0",
    "rule_version": "V4.1",
    "macd": {
        "grade_label_map": {"-4": "极弱", "-3": "强空", "-2": "中空", "-1": "略偏空", "0": "无方向", "1": "略偏多", "2": "中多", "3": "偏多", "4": "极强"},
        "legend": "DIF/DEA/柱=同花顺收盘口径；dead_cross_day=死叉延续日数（交叉首日不计）"
    },
    "qimen": {
        "a_meaning": {"2": "a=+2 强同向推力", "1": "a=+1 弱同向推力", "0": "a=0 无油门输入，纯底座运行", "-1": "a=-1 弱反向对冲", "-2": "a=-2 强反向对冲"},
        "layer_coef": {"核心": 1.5, "力量": 1.0, "衍生": 0.5},
        "matrix_meta": {"穷举口径": 108, "说明": "13用神×8状态104格+全局行4格", "行数": 14},
        "matrix_def": "立体矩阵v2.5（42空格全立G93~G134），权威=《立体矩阵v2》穷举表",
        "channel_legend": "攻多=多方能量渠道（绿）/攻空=空方能量渠道（红）/结构=振幅与节奏渠道（蓝）——格存基础分，层间才加权",
        "formula_note": "奇门a：r=a_raw÷(攻多+攻空+结构)，|r|≥0.45→±2，≥0.20→±1，<0.20→0（表2-D占比制）",
        "roles_legend": "13角色=交易断局最小完备角色集（权威=立体矩阵v2.4十三用神序）"
    }
}

# 槽位→全量 的块映射（槽位键 → 全量落点）
SLOT_BLOCKS = ["date", "macd_date", "date_display", "ganzhi", "dun", "path", "rule_version",
               "macd", "matrix", "v0", "qimen", "fusion", "four_slots",
               "palace_table", "matrix_drop", "matrix_missing", "matrix_missing_note", "matrix_global",
               "shape", "volatility", "flip", "accel", "strong_bottom", "strong_bottom_note",
               "output", "nine_fields", "adjust", "calibration",
               "four_slots_4p", "four_slots_summary", "verification", "actual_curve"]


def deep_merge(base, overlay):
    """overlay 覆盖 base，dict 递归，其余直接替换"""
    if isinstance(base, dict) and isinstance(overlay, dict):
        out = copy.deepcopy(base)
        for k, v in overlay.items():
            out[k] = deep_merge(out[k], v) if k in out else copy.deepcopy(v)
        return out
    return copy.deepcopy(overlay)


def assemble(slots):
    out = {}
    # 1. 常量先行
    out = deep_merge(out, {"schema_version": CONSTANTS["schema_version"], "rule_version": CONSTANTS["rule_version"],
                           "macd": {"grade_label_map": CONSTANTS["macd"]["grade_label_map"], "legend": CONSTANTS["macd"]["legend"]},
                           "qimen": {k: v for k, v in CONSTANTS["qimen"].items()}})
    # 2. 槽位覆盖
    for k in SLOT_BLOCKS:
        if k in slots and slots[k] is not None:
            out[k] = deep_merge(out.get(k, {}), slots[k]) if isinstance(slots[k], dict) and k in ("macd", "qimen", "fusion") else slots[k]
    # 3. 派生字段（组装器保证结构完整——LLM直写时的漏写字段由这里补）
    out.setdefault("matrix_drop", [])
    out.setdefault("palace_table", [])
    # 顶层path=fusion.path 双写（11-04事故防线：schema要求顶层path，历史只写fusion.path）
    if "fusion" in out and isinstance(out["fusion"], dict):
        fp = out["fusion"].get("path")
        if fp and out.get("path") != fp:
            out["path"] = fp
        # 九字段冗余层（若有nine_fields，同步fusion核心值）
        nf = out.get("nine_fields")
        if isinstance(nf, dict):
            for src, dst in [("v0_grade", None), ("a_macd", None), ("qimen_a", None), ("b_value", "b_value"), ("path", None)]:
                if src in nf and dst and dst not in out["fusion"]:
                    out["fusion"][dst] = nf[src]
    # shape兜底（缺块时补空壳，schema required会再卡内容）
    out.setdefault("shape", {})
    out.setdefault("volatility", {})
    return out


def check_arithmetic(d):
    """算术一致性校验（纯恒等式，不碰业务压级规则）"""
    errs = []
    f = d.get("fusion", {})
    q = d.get("qimen", {})
    def num(x):
        try: return float(x)
        except (TypeError, ValueError): return None
    v0, at, bx, vf = num(f.get("v0_int")), num(f.get("a_total")), num(f.get("b_value")), num(f.get("v_final"))
    vc = num(f.get("v_cross"))
    if None not in (v0, at, vc) and abs((v0 + at) - vc) > 0.01:
        errs.append(f"v_cross({vc}) ≠ v0_int({v0})+a_total({at})")
    if None not in (vc, bx, vf) and abs((vc + bx) - vf) > 0.01:
        errs.append(f"v_final({vf}) ≠ v_cross({vc})+b_value({bx})")
    qa, am = num(q.get("a_total")), num(f.get("a_macd"))
    if None not in (qa, am) and f.get("a_total") is not None and abs(qa - num(f.get("a_total"))) > 0.01:
        errs.append(f"fusion.a_total({f.get('a_total')}) ≠ qimen.a_total({qa})")
    m = d.get("macd", {})
    dif, dea, bar = num(m.get("dif")), num(m.get("dea")), num(m.get("bar"))
    if None not in (dif, dea, bar) and abs((dif - dea) * 2 - bar) > 0.06:
        errs.append(f"macd.bar({bar}) ≠ (DIF-DEA)×2({round((dif-dea)*2,3)})")
    if d.get("path") and f.get("path") and d["path"] != f["path"]:
        errs.append(f"顶层path({d['path']}) ≠ fusion.path({f['path']})")
    return errs


def main():
    if len(sys.argv) < 2:
        print("用法: build_pipeline_json.py <slots.json> [--out <输出路径>]")
        sys.exit(2)
    slots_path = sys.argv[1]
    out_path = None
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]
    slots = json.load(open(slots_path, encoding="utf-8"))
    d = assemble(slots)

    arith = check_arithmetic(d)
    if arith:
        print("❌ 算术一致性校验失败：")
        for e in arith: print(f"  ✗ {e}")
        sys.exit(1)

    # schema 校验
    try:
        import jsonschema
        from jsonschema import Draft7Validator
        schema = json.load(open(os.path.join(ROOT, "data", "schema", "pipeline.schema.json"), encoding="utf-8"))
        errors = sorted(Draft7Validator(schema).iter_errors(d), key=lambda e: list(e.absolute_path))
        if errors:
            print(f"❌ schema 校验失败：{len(errors)} 处")
            for e in errors[:20]:
                print(f"  ✗ {'.'.join(str(p) for p in e.absolute_path) or '(根)'}: {e.message}")
            sys.exit(1)
    except ImportError:
        print("⚠️ 缺 jsonschema，跳过 schema 校验（仅算术校验通过）")

    if out_path:
        json.dump(d, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"✅ 组装+校验通过 → {out_path} ｜ matrix_drop {len(d.get('matrix_drop',[]))}格 ｜ final_grade={d.get('fusion',{}).get('final_grade')}")
    else:
        print(json.dumps(d, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
