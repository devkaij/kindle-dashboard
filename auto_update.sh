#!/bin/bash
# Kindle Dashboard 自动更新 - macOS/Linux 版本
# 添加到 crontab: 0 8,12,18,22 * * * /path/to/kindle-dashboard/auto_update.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始自动更新..."

python3 generate.py

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 更新完成!"
