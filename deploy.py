#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""部署脚本：上传到 GitHub Pages 实现免电脑访问"""

import subprocess
import json
import sys
import os

def run(cmd):
    """运行命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def check_github():
    """检查 GitHub 配置"""
    print("🔍 检查 GitHub 配置...")
    rc, out, err = run("gh auth status")
    if rc != 0:
        print("❌ 未登录 GitHub")
        print("请运行: gh auth login")
        return False
    
    rc, out, err = run("gh repo list --limit 1")
    if "kindle-dashboard" in out:
        print("✅ 仓库已存在: kindle-dashboard")
        return True
    
    print("📦 创建 GitHub 仓库...")
    rc, out, err = run("gh repo create kindle-dashboard --public --push --source=. --remote=origin")
    if rc == 0:
        print("✅ 仓库创建成功")
        return True
    else:
        print(f"❌ 创建失败: {err}")
        return False

def deploy():
    """部署到 GitHub Pages"""
    print("\n🚀 开始部署...")
    
    # 检查分支
    current_branch = subprocess.run("git rev-parse --abbrev-ref HEAD", 
                                    capture_output=True, text=True).stdout.strip()
    
    if current_branch != "main" and current_branch != "master":
        print(f"⚠️ 当前分支: {current_branch}")
        print("建议切换到 main 分支后再部署")
    
    # 提交更改
    print("📝 提交更改...")
    run("git add .")
    run("git commit -m 'Add Kindle Dashboard v3: no computer needed'")
    
    # 推送
    print("📤 推送到 GitHub...")
    rc, out, err = run("git push origin main")
    if rc != 0:
        print(f"推送失败: {err}")
        return False
    
    # 启用 Pages
    print("🌐 启用 GitHub Pages...")
    rc, out, err = run("gh repo edit kindle-dashboard --add-topic kindle --set-homepage=true")
    
    print("\n✅ 部署完成！")
    print(f"📱 访问地址: https://17759.github.io/kindle-dashboard/")
    print("\n在 Kindle 浏览器输入: https://17759.github.io/kindle-dashboard/")
    print("无需电脑运行服务！")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'deploy':
        deploy()
    else:
        if check_github():
            deploy()
