# Kindle Dashboard v2 - 使用说明

## 📦 文件列表

| 文件 | 说明 |
|------|------|
| `kindle_dashboard_v2.html` | 主页面（时间+天气+热搜） |
| `server.py` | 本地代理服务 |
| `启动服务.bat` | Windows 一键启动脚本 |

---

## 🚀 使用方法

### 第一步：启动服务

**方式一：双击运行**
```
双击 "启动服务.bat"
```

**方式二：命令行启动**
```bash
cd D:/AI Desktop/kindle-dashboard
python3 server.py
```

### 第二步：Kindle 连接

确保 Kindle 和电脑在同一 WiFi 网络，然后在 Kindle 浏览器访问：
```
http://192.168.2.252:8765/kindle_dashboard_v2.html
```

> 如果 IP 地址不对，查看启动服务时打印的地址

---

## ✅ 已验证功能

### 🔥 百度热搜
- API: `top.baidu.com/api/board`
- 返回: TOP 10 热搜
- 状态: ✅ 正常

```
示例输出:
1. 天安门下半旗悼念朱镕基同志 (780万)
2. 重要规划发布！新风口要来了 (771万)
3. 石油天然气发展"十五五"规划印发 (761万)
...
```

### 🌤️ 天气
- API: `open-meteo.com` (免费无需key)
- 定位: 宁德 (26.66°N, 119.52°E)
- 显示: 温度、天气描述、风速
- 状态: ✅ 正常

```
示例输出:
31.3°C 晴朗 风速14km/h
```

### ⏰ 时间
- 每60秒更新一次（时分）
- 自动跟随系统时区

---

## 🔧 技术说明

### 为什么需要本地代理？

Kindle 使用 `file://` 协议打开 HTML 时，浏览器安全策略会阻止：
1. 跨域 AJAX 请求（CORS）
2. 访问外部 API

本地代理服务解决这些问题：
- 代理百度热搜 API → `http://localhost:8765/api/hot`
- 代理天气 API → `http://localhost:8765/api/weather`
- 添加 CORS 头 → `Access-Control-Allow-Origin: *`

### API 代理表

| 前端请求 | 后端代理 | 外部服务 |
|---------|---------|---------|
| `/api/hot` | `top.baidu.com/api/board` | 百度热搜 |
| `/api/weather?lat=x&lon=y` | `api.open-meteo.com/v1/forecast` | Open-Meteo |

---

## 📱 Kindle 操作指南

1. 打开 Kindle 内置浏览器
2. 输入地址栏：`http://192.168.2.252:8765`
3. 点击屏幕刷新数据
4. 等待 30 分钟自动更新

---

## ⚠️ 注意事项

1. **保持服务运行**：关闭电脑或停止服务后，Kindle 将无法获取数据
2. **同一网络**：Kindle 和电脑必须在同一 WiFi
3. **防火墙**：如无法访问，检查 Windows 防火墙是否允许 8765 端口
4. **电池消耗**：后台运行会消耗 Kindle 电量，建议充电使用

---

## 🐛 常见问题

### Q: Kindle 显示"连接失败"
```
A: 检查：
   1. 服务是否正在运行
   2. Kindle 和电脑是否同一 WiFi
   3. Windows 防火墙是否允许
```

### Q: 热搜加载失败
```
A: 检查电脑网络是否能访问百度
```

### Q: 天气显示默认值
```
A: 检查 Open-Meteo API 是否可达
```

---

## 📄 版本历史

- **v2.0** (2026-08-18): 添加百度热搜，修复 CORS 问题
- **v1.0**: 初版时间+天气

---

**服务地址**: http://127.0.0.1:8765  
**Kindle 地址**: http://192.168.2.252:8765
