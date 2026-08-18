#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kindle Dashboard 本地代理服务
解决 Kindle file:// 协议的 CORS 限制
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.request
import ssl
import re
import sys

class DashboardHandler(SimpleHTTPRequestHandler):
    """提供 Dashboard 页面和 API 代理"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=".", **kwargs)
    
    def do_GET(self):
        # 代理百度热搜 API
        if self.path.startswith('/api/hot'):
            return self.proxy_baidu_hot()
        
        # 代理天气 API
        if self.path.startswith('/api/weather'):
            return self.proxy_weather()
        
        # 返回 HTML 页面
        return super().do_GET()
    
    def proxy_baidu_hot(self):
        """代理百度热搜 API"""
        try:
            url = 'https://top.baidu.com/api/board?platform=wiseapp'
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json',
            })
            
            # 本地开发代理，跳过证书验证（开发环境，生产环境应恢复）
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                data = json.loads(resp.read().decode('utf-8'))

                if data.get('success') and data.get('data', {}).get('cards'):
                    items = data['data']['cards'][0]['content'][:10]
                    result = {
                        'success': True,
                        'items': [
                            {
                                'word': item.get('word', ''),
                                'hotScore': item.get('hotScore', '0'),
                                'desc': item.get('desc', '')[:50]
                            }
                            for item in items
                        ]
                    }
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                else:
                    raise Exception('No data')
                    
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))

    def proxy_weather(self):
        """代理天气 API (使用 Open-Meteo)"""
        try:
            # 从查询参数获取经纬度，默认宁德
            params = self.path.split('?')[1] if '?' in self.path else ''
            if 'lat' in params and 'lon' in params:
                lat = params.split('&')[0].split('=')[1]
                lon = params.split('&')[1].split('=')[1]
            else:
                lat, lon = '26.66', '119.52'  # 宁德默认
            
            url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m&timezone=Asia/Shanghai'
            
            req = urllib.request.Request(url)
            # 本地开发代理，跳过证书验证（开发环境，生产环境应恢复）
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                weather_map = {
                    0: '晴朗', 1: '晴间多云', 2: '多云', 3: '阴天',
                    45: '雾', 48: '雾',
                    51: '毛毛雨', 53: '毛毛雨', 55: '毛毛雨',
                    61: '小雨', 63: '中雨', 65: '大雨',
                    71: '小雪', 73: '中雪', 75: '大雪',
                    80: '阵雨', 81: '阵雨', 82: '暴雨',
                    95: '雷暴', 96: '雷暴夹冰雹', 99: '雷暴夹大冰雹'
                }
                desc = weather_map.get(cw.get('weathercode', 0), '未知')
                
                result = {
                    'temperature': cw.get('temperature', '--'),
                    'windspeed': cw.get('windspeed', '--'),
                    'description': desc,
                    'unit': '°C'
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
    
    def log_message(self, format, *args):
        """简化日志"""
        pass


def get_ip_info():
    """获取本地 IP 信息"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"


def main():
    port = 8765
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    local_ip = get_ip_info()
    
    print(f"📊 Kindle Dashboard 服务已启动")
    print(f"🌐 本机访问: http://127.0.0.1:{port}")
    print(f"📱 Kindle 访问: http://{local_ip}:{port}")
    print(f"🔗 备用访问: http://{local_ip}:{port}/kindle_dashboard_v2.html")
    print(f"\n请确保 Kindle 和电脑在同一 WiFi 网络")
    print(f"按 Ctrl+C 停止服务\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.shutdown()


if __name__ == '__main__':
    main()
