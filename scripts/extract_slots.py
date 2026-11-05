#!/usr/bin/env python3
"""从全量pipeline JSON反抽槽位视图（回放验证用：全量→槽位→组装→应还原等价全量）"""
import json, sys

SLOT_KEYS = ["date", "macd_date", "date_display", "ganzhi", "dun", "path", "rule_version",
             "macd", "matrix", "v0", "qimen", "fusion", "four_slots",
             "shape", "volatility", "flip", "accel", "strong_bottom", "strong_bottom_note",
             "output", "nine_fields", "adjust", "calibration",
             "palace_table", "matrix_drop", "matrix_missing", "matrix_missing_note", "matrix_global",
             "four_slots_4p", "four_slots_summary", "verification", "actual_curve"]

src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding="utf-8"))
slots = {k: d[k] for k in SLOT_KEYS if k in d}
json.dump(slots, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"槽位抽取完成：{len(slots)} 块 → {dst}")
