#!/usr/bin/env python3
"""
早上系统可靠性数据同步脚本
用法:
    python3 /root/.openclaw/workspace/yixue-dashboard/tools/sync_system_status.py

功能:
    1. 读取 memory/选股反馈/system-status.json
    2. 复制到 yixue-dashboard/data/system-status.json
    3. git add + commit + push

此脚本应在每天早上 07:00 网站更新任务中执行，在方向整理完成后、git push 之前调用。
"""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime

SRC = "/root/.openclaw/workspace/memory/选股反馈/system-status.json"
DST = "/root/.openclaw/workspace/yixue-dashboard/data/system-status.json"
REPO = "/root/.openclaw/workspace/yixue-dashboard"


def main():
    print("[sync_system_status] 开始同步系统可靠性数据...")

    if not os.path.exists(SRC):
        print(f"[ERROR] 源文件不存在: {SRC}")
        print("[HINT] 请确保下午复盘任务已执行并生成了 system-status.json")
        sys.exit(1)

    # 读取确认
    with open(SRC, "r", encoding="utf-8") as f:
        data = json.load(f)
    date = data.get("date", "unknown")
    badge = data.get("badge", {}).get("text", "unknown")
    print(f"  源数据日期: {date}")
    print(f"  系统状态: {badge}")

    # 复制
    shutil.copy2(SRC, DST)
    print(f"  已复制到: {DST}")

    # git 操作
    os.chdir(REPO)
    subprocess.run(["git", "add", "data/system-status.json"], check=True)
    
    # 检查是否有变更
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode == 0:
        print("  无变更，跳过 commit")
        return

    subprocess.run(
        ["git", "commit", "-m", f"系统状态更新: {date} {badge}"],
        check=True,
    )
    subprocess.run(["git", "push", "origin", "gh-pages"], check=True)
    print("  已推送到 gh-pages")
    print(f"[sync_system_status] 完成")


if __name__ == "__main__":
    main()
