#!/usr/bin/env python3
"""预测管线看板数据契约校验器（schema2.0 验收基准）
用法: python3 scripts/validate_pipeline.py <json文件> [--quiet]
exit 0=通过, exit 1=失败（错误报告打印到stdout）
"""
import sys, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(ROOT, "data", "schema", "pipeline.schema.json")

def main():
    if len(sys.argv) < 2:
        print("用法: validate_pipeline.py <json文件> [--quiet]")
        sys.exit(2)
    target = sys.argv[1]
    quiet = "--quiet" in sys.argv

    try:
        import jsonschema
        from jsonschema import Draft7Validator
    except ImportError:
        print("❌ 缺少 jsonschema 库：pip3 install jsonschema")
        sys.exit(2)

    schema = json.load(open(SCHEMA_PATH, encoding="utf-8"))
    try:
        data = json.load(open(target, encoding="utf-8"))
    except Exception as e:
        print(f"❌ JSON 解析失败：{e}")
        sys.exit(1)

    v = Draft7Validator(schema)
    errors = sorted(v.iter_errors(data), key=lambda e: list(e.absolute_path))

    if not errors:
        md = data.get("matrix_drop", [])
        fg = (data.get("fusion") or {}).get("final_grade")
        slots = [s.get("grade") for s in data.get("four_slots", []) if isinstance(s, dict)]
        if not quiet:
            print(f"✅ schema 校验通过 ｜ matrix_drop {len(md)}格 ｜ final_grade={fg} ｜ 四时段={'/'.join(str(s) for s in slots)}")
        sys.exit(0)

    # 错误分组报告
    print(f"❌ schema 校验失败：{len(errors)} 处错误\n")
    for e in errors:
        path = ".".join(str(p) for p in e.absolute_path) or "(根)"
        # 生产端偷懒/漂移的直白提示
        hint = ""
        if "matrix_drop" in path and "is not of type" in e.message:
            hint = " ← 11-05事故同款：matrix_drop 必须是结构化数组，禁止'见报告第N节'式偷懒"
        if "final_grade" in path and "is not of type" in e.message:
            hint = " ← 11-05事故同款：final_grade 必须是表4-A档名字符串（无方向/略偏多...），禁止数字编码"
        print(f"  ✗ {path}: {e.message}{hint}")
    print(f"\n文件：{target}")
    sys.exit(1)

if __name__ == "__main__":
    main()
