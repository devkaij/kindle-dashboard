#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kindle Dashboard - 一键生成并发送邮件到 Kindle"""

import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import subprocess

# ============ 配置区域 ============
# Kindle 邮箱地址（从亚马逊账户设置获取）
KINDLE_EMAIL = ""  # 请在这里填写你的 Kindle 邮箱，例如: yourkindle@kindle.com

# 发件邮箱配置
SMTP_SERVER = "smtp.qq.com"  # 或其他 SMTP 服务器
SMTP_PORT = 587
SMTP_USER = ""
SMTP_PASSWORD = ""
# =================================

def get_kindle_email():
    """获取 Kindle 邮箱"""
    global KINDLE_EMAIL
    if KINDLE_EMAIL:
        return KINDLE_EMAIL
    
    print("📧 请输入你的 Kindle 邮箱地址：")
    print("   (在亚马逊账户页面查看，以 @kindle.com 或 @kindle.cn 结尾)")
    email = input("> ").strip()
    
    if email and '@' in email:
        KINDLE_EMAIL = email
        # 保存到配置文件
        save_config()
        return email
    else:
        print("❌ 邮箱格式不正确")
        return None

def save_config():
    """保存配置到本地文件"""
    config = f"KINDLE_EMAIL = '{KINDLE_EMAIL}'\n"
    with open(os.path.join(os.path.dirname(__file__), 'config.py'), 'w', encoding='utf-8') as f:
        f.write(config)

def load_config():
    """加载配置"""
    global KINDLE_EMAIL
    config_path = os.path.join(os.path.dirname(__file__), 'config.py')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            exec(f.read(), globals())

def generate_html():
    """生成 HTML 文件"""
    print("🔄 正在调用 generate.py 生成 HTML...")
    result = subprocess.run(
        ['python3', 'generate.py'],
        cwd=os.path.dirname(__file__),
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(f"错误: {result.stderr}")
        return None
    
    # 获取最新的 HTML 文件
    files = [f for f in os.listdir(os.path.dirname(__file__)) 
             if f.startswith('kindle_dashboard_') and f.endswith('.html')]
    if not files:
        print("❌ 未找到生成的 HTML 文件")
        return None
    
    latest_file = max(files)  # 最新生成的文件
    return os.path.join(os.path.dirname(__file__), latest_file)

def send_email(html_file, recipient_email):
    """发送邮件到 Kindle"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['Subject'] = f"Kindle Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        msg['To'] = recipient_email
        
        # 读取 HTML 文件内容
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 添加 HTML 正文
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 添加文件附件
        attachment = MIMEBase('application', 'octet-stream')
        with open(html_file, 'rb') as f:
            attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(html_file)}"')
        msg.attach(attachment)
        
        # 发送邮件
        print(f"📤 正在发送邮件到 {recipient_email}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, recipient_email, msg.as_string())
        server.quit()
        
        print("✅ 邮件发送成功！")
        print(f"📱 Kindle 将在几分钟后收到更新")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("  Kindle Dashboard 一键生成与发送")
    print("=" * 50)
    
    # 加载配置
    load_config()
    
    # 获取 Kindle 邮箱
    if not KINDLE_EMAIL:
        kindle_email = get_kindle_email()
        if not kindle_email:
            sys.exit(1)
    else:
        print(f"✅ 使用已保存的 Kindle 邮箱: {KINDLE_EMAIL}")
        kindle_email = KINDLE_EMAIL
    
    # 生成 HTML
    html_file = generate_html()
    if not html_file:
        sys.exit(1)
    
    print(f"📄 生成文件: {html_file}")
    print("\n发送选项:")
    print("1. 发送邮件到 Kindle")
    print("2. 仅生成文件，不发送")
    print("3. 退出")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice == '1':
        if not SMTP_USER or not SMTP_PASSWORD:
            print("\n⚠️  请先配置发件邮箱信息：")
            print("   1. 打开 generate.py 文件")
            print("   2. 修改 SMTP_SERVER, SMTP_USER, SMTP_PASSWORD")
            print("   (建议使用 QQ 邮箱或 163 邮箱)")
            print("\n或者手动将文件发送到 Kindle")
            return
        
        send_email(html_file, kindle_email)
    elif choice == '2':
        print(f"\n✅ 文件已生成，请手动发送到 Kindle")
        print(f"📁 文件位置: {html_file}")
    else:
        print("\n已取消")

if __name__ == '__main__':
    main()
