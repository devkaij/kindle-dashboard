#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自动更新任务 - Windows 计划任务
设置后电脑开机时自动运行，生成并发送最新数据
"""

import os
import sys
import subprocess
from datetime import datetime

def run_generate():
    """运行生成脚本"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 开始自动更新...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    generate_script = os.path.join(script_dir, 'generate.py')
    
    try:
        result = subprocess.run(
            [sys.executable, generate_script],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(result.stdout)
        if result.stderr:
            print(f"错误: {result.stderr}")
        
        if result.returncode == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 更新完成!")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 更新失败")
            
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 异常: {e}")

if __name__ == '__main__':
    run_generate()
