#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kindle Dashboard - 静态页面生成器
生成包含最新数据的 HTML 文件，直接发送到 Kindle
"""

import json
import urllib.request
import ssl
from datetime import datetime
import sys
import os

# 配置
WEATHER_CITY = "ningde"
TIMEZONE = "Asia/Shanghai"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"

def fetch_weather():
    """获取天气数据"""
    try:
        url = f"https://wttr.in/{WEATHER_CITY}?format=j1"
        req = urllib.request.Request(url, headers={
            'User-Agent': USER_AGENT,
            'Accept': 'application/json'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            cc = data['current_condition'][0]
            
            weather_map = {
                '113': '晴朗', '116': '多云', '119': '阴天',
                '122': '阴天', '143': '雾', '176': '阵雨',
                '179': '小阵雨', '182': '小冰雹', '185': '小冰雹',
                '200': '雷雨', '227': '雪', '230': '大雪',
                '260': '冻雨', '263': '毛毛雨', '266': '毛毛雨',
                '281': '冻雨', '284': '冻雨', '293': '小雨',
                '296': '小雨', '299': '中雨', '302': '中雨',
                '305': '大雨', '308': '大雨', '311': '小冰雹',
                '314': '中冰雹', '317': '大冰雹', '320': '小雪',
                '323': '中雪', '326': '大雪', '329': '小阵雪',
                '332': '中阵雪', '335': '大阵雪', '338': '大雪',
                '350': '冰粒', '353': '小雨', '356': '中雨',
                '359': '大雨', '362': '小冰雹', '365': '小冰雹',
                '368': '小阵雪', '371': '大阵雪', '374': '冰雹',
                '377': '冰粒', '386': '雷雨有雨', '389': '雷雨有雪',
                '392': '雷雨', '395': '雷雨有雪'
            }
            
            code = cc.get('weatherCode', '116')
            desc = weather_map.get(code, '多云')
            
            return {
                'temp': cc.get('temp_C', '--'),
                'desc': desc,
                'humidity': cc.get('humidity', '--'),
                'wind': cc.get('windspeedKmph', '--'),
                'feels_like': cc.get('FeelsLikeC', '--')
            }
    except Exception as e:
        print(f"天气获取失败: {e}")
        return {'temp': '--', 'desc': '获取失败', 'humidity': '--', 'wind': '--', 'feels_like': '--'}

def fetch_news(count=10):
    """获取 Hacker News 热榜"""
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            ids = json.loads(resp.read().decode('utf-8'))
            
            stories = []
            for sid in ids[:count]:
                try:
                    item_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
                    req = urllib.request.Request(item_url, headers={'User-Agent': USER_AGENT})
                    
                    with urllib.request.urlopen(req, timeout=10, context=ctx) as item_resp:
                        story = json.loads(item_resp.read().decode('utf-8'))
                        if story and 'title' in story:
                            stories.append({
                                'title': story.get('title', 'Untitled')[:50],
                                'score': story.get('score', 0),
                                'comments': story.get('descendants', 0),
                                'url': story.get('url', '#')
                            })
                except:
                    continue
            
            # 按分数排序
            stories.sort(key=lambda x: x['score'], reverse=True)
            return stories[:8]
    except Exception as e:
        print(f"新闻获取失败: {e}")
        return []

def generate_html(weather, news):
    """生成静态 HTML"""
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日 星期%w")
    time_str = now.strftime("%H:%M")
    update_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # 生成新闻列表 HTML
    news_items = ""
    for i, item in enumerate(news, 1):
        rank_class = "top3" if i <= 3 else ""
        news_items += f'''
        <li class="hot-item">
            <span class="hot-rank {rank_class}">{i}</span>
            <span class="hot-word">{item['title']}</span>
            <span class="hot-score">{item['score']}分</span>
        </li>'''
    
    if not news_items:
        news_items = '<li class="error">新闻获取失败</li>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kindle Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: "SimSun", "宋体", "Microsoft YaHei", sans-serif;
            background: #ffffff; color: #000000; padding: 15px; font-size: 18px;
        }}
        .header {{
            text-align: center; font-size: 22px; font-weight: bold;
            margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #000;
        }}
        .card {{
            border: 2px solid #000; margin-bottom: 15px; padding: 15px; background: #fff;
        }}
        .card-title {{
            font-size: 16px; font-weight: bold; margin-bottom: 8px;
            color: #333; border-bottom: 1px dashed #ccc; padding-bottom: 5px;
        }}
        .time-main {{ font-size: 42px; font-weight: bold; text-align: center; letter-spacing: 2px; }}
        .time-date {{ text-align: center; font-size: 16px; margin-top: 5px; color: #333; }}
        .weather-row {{ display: flex; justify-content: space-between; align-items: center; }}
        .weather-temp {{ font-size: 36px; font-weight: bold; }}
        .weather-desc {{ font-size: 18px; }}
        .weather-detail {{ font-size: 14px; color: #666; margin-top: 5px; }}
        .hot-list {{ list-style: none; }}
        .hot-item {{
            display: flex; align-items: baseline; padding: 8px 0;
            border-bottom: 1px dashed #ccc; font-size: 16px; line-height: 1.4;
        }}
        .hot-item:last-child {{ border-bottom: none; }}
        .hot-rank {{ display: inline-block; width: 24px; font-weight: bold; color: #333; flex-shrink: 0; }}
        .hot-rank.top3 {{ color: #c00; }}
        .hot-word {{ flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .hot-score {{ font-size: 12px; color: #999; margin-left: 8px; flex-shrink: 0; }}
        .error {{ text-align: center; padding: 20px; color: #999; font-size: 14px; }}
        .update-time {{ text-align: center; font-size: 14px; color: #999; margin-top: 15px; }}
    </style>
</head>
<body>
    <div class="header">📊 Kindle 状态面板</div>
    
    <div class="card">
        <div class="card-title">⏰ 时间</div>
        <div class="time-main">{time_str}</div>
        <div class="time-date">{date_str}</div>
    </div>
    
    <div class="card">
        <div class="card-title">🌤️ 天气 (宁德)</div>
        <div class="weather-row">
            <div class="weather-temp">{weather['temp']}°C</div>
            <div class="weather-desc">{weather['desc']}</div>
        </div>
        <div class="weather-detail">体感 {weather['feels_like']}°C | 湿度 {weather['humidity']}% | 风速 {weather['wind']} km/h</div>
    </div>
    
    <div class="card">
        <div class="card-title">📰 科技新闻 (Hacker News)</div>
        <ul class="hot-list">
            {news_items}
        </ul>
    </div>
    
    <div class="update-time">更新时间: {update_time}</div>
</body>
</html>'''
    
    return html

def save_html(html, filename=None):
    """保存 HTML 文件"""
    if filename is None:
        now = datetime.now()
        filename = f"kindle_dashboard_{now.strftime('%Y%m%d_%H%M')}.html"
    
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 已生成: {filepath}")
    print(f"📧 将此文件发送到你的 Kindle 邮箱即可")
    return filepath

def main():
    print("🔄 正在获取数据...")
    
    print("🌤️ 获取天气...")
    weather = fetch_weather()
    print(f"   温度: {weather['temp']}°C, {weather['desc']}")
    
    print("📰 获取新闻...")
    news = fetch_news(10)
    print(f"   获取到 {len(news)} 条新闻")
    
    print("📝 生成 HTML...")
    html = generate_html(weather, news)
    
    print("💾 保存文件...")
    filepath = save_html(html)
    
    print("\n✅ 完成！")
    print(f"文件路径: {filepath}")
    print("\n发送方法:")
    print("1. 将此文件作为附件发送到你的 Kindle 邮箱")
    print("2. 或手动复制到 Kindle 的 /documents/ 文件夹")

if __name__ == '__main__':
    main()
