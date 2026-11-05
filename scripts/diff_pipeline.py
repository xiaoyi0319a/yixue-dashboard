#!/usr/bin/env python3
"""预测管线数据语义对账器（灰度期：影子组装版 vs LLM直写版 逐字段比对）
用法: python3 scripts/diff_pipeline.py <A.json> <B.json> [--tolerance 0.01] [--json out.json]
exit 0=语义全等, exit 1=有差异（差异清单打印stdout）
"""
import sys, json, os

def flatten(o, prefix="", out=None):
    if out is None: out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            flatten(v, f"{prefix}.{k}" if prefix else str(k), out)
    elif isinstance(o, list):
        # list 按索引展开；dict元素含cell/g的（matrix_drop类）按格坐标索引，顺序无关
        keyed = all(isinstance(x, dict) and ("g" in x or "cell" in x or "grid" in x) for x in o) if o else False
        if keyed:
            for x in o:
                key = x.get("g") or x.get("cell") or x.get("grid") or str(x)
                flatten(x, f"{prefix}[{key}]", out)
        else:
            for i, v in enumerate(o):
                flatten(v, f"{prefix}[{i}]", out)
    else:
        out[prefix] = o
    return out


def close(a, b, tol):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= tol
    return a == b


def main():
    if len(sys.argv) < 3:
        print("用法: diff_pipeline.py <A.json> <B.json> [--tolerance 0.01]")
        sys.exit(2)
    pa, pb = sys.argv[1], sys.argv[2]
    tol = 0.01
    if "--tolerance" in sys.argv:
        tol = float(sys.argv[sys.argv.index("--tolerance") + 1])
    A = flatten(json.load(open(pa, encoding="utf-8")))
    B = flatten(json.load(open(pb, encoding="utf-8")))

    only_a = sorted(set(A) - set(B))
    only_b = sorted(set(B) - set(A))
    diff = sorted(k for k in set(A) & set(B) if not close(A[k], B[k], tol))

    total = len(set(A) | set(B))
    same = total - len(only_a) - len(only_b) - len(diff)
    print(f"对账结果：{same}/{total} 字段一致 ｜ 仅A有 {len(only_a)} ｜ 仅B有 {len(only_b)} ｜ 值不同 {len(diff)}")
    if only_a:
        print("\n--- 仅A有 ---")
        for k in only_a[:30]: print(f"  A: {k} = {str(A[k])[:80]}")
    if only_b:
        print("\n--- 仅B有 ---")
        for k in only_b[:30]: print(f"  B: {k} = {str(B[k])[:80]}")
    if diff:
        print("\n--- 值不同 ---")
        for k in diff[:30]: print(f"  {k}: A={str(A[k])[:60]}  B={str(B[k])[:60]}")
    if len(only_a) + len(only_b) + len(diff) > 90:
        print(f"... 其余 {len(only_a)+len(only_b)+len(diff)-90} 条省略")
    sys.exit(0 if (not only_a and not only_b and not diff) else 1)


if __name__ == "__main__":
    main()
