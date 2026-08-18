# Kindle Dashboard 使用说明

## 📦 快速开始

### 方式一：网页访问（无需电脑）
```
https://devkaij.github.io/kindle-dashboard/
```
Kindle 浏览器直接打开，数据每30分钟自动刷新。

### 方式二：生成 HTML 文件发送
```bash
# 1. 生成 HTML
python3 generate.py

# 2. 发送文件到 Kindle 邮箱
python3 send_to_kindle.py
```

---

## 📋 文件说明

| 文件 | 说明 |
|------|------|
| `kindle_dashboard_v3.html` | 在线版（需保持页面打开） |
| `generate.py` | 生成静态 HTML |
| `send_to_kindle.py` | 一键发送到 Kindle |
| `config.py` | 保存的配置文件 |

---

## 📧 发送方式

### 方法 1：亚马逊官方推送
1. 获取 Kindle 邮箱：登录亚马逊 → 我的账户 → 管理内容与设备 → 个人文档设置
2. 复制生成的 HTML 文件
3. 作为附件发送到 Kindle 邮箱
4. 自动同步到 Kindle

### 方法 2：USB 传输
1. 连接 Kindle 到电脑
2. 复制文件到 `/documents/` 文件夹
3. 在 Kindle 上打开

### 方法 3：邮件附件
1. 使用 `send_to_kindle.py` 自动发送
2. 需要配置发件邮箱

---

## ⚙️ 配置

编辑 `send_to_kindle.py` 中的配置：
```python
KINDLE_EMAIL = "yourkindle@kindle.com"  # Kindle 邮箱
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SMTP_USER = "your_email@qq.com"
SMTP_PASSWORD = "your_app_password"
```

---

## 📱 Kindle 邮箱获取方法

1. 登录 https://www.amazon.cn
2. 点击「我的账户」
3. 选择「管理我的内容和设备」
4. 在「个人文档设置」中查看收件邮箱

常见域名：
- 国行版：`@kindle.cn`
- 美亚版：`@kindle.com`
- 其他：`@free.kindle.com`

---

## 🎯 更新数据

### 方式一：网页版（推荐）
打开 `https://devkaij.github.io/kindle-dashboard/`
- 点击屏幕手动刷新
- 每30分钟自动更新

### 方式二：生成静态文件
```bash
python3 generate.py
python3 send_to_kindle.py
```
生成后发送到 Kindle，每次运行都会生成新的 HTML 文件。

---

## ⚠️ 注意事项

1. **网页版**：需要 Kindle 保持网络连接
2. **文件版**：发送后自动同步，离线可查看
3. **时区**：显示的是本地时间（中国时区）
4. **位置**：天气固定显示宁德，如需修改修改 `generate.py` 中的 `WEATHER_CITY`

---

**最后更新**: 2026-08-18
