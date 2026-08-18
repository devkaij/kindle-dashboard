@echo off
chcp 65001 >nul
title Kindle Dashboard Server
echo ========================================
echo   Kindle Dashboard 本地代理服务
echo ========================================
echo.
echo 📊 服务启动中...
echo.
cd /d "%~dp0"
python server.py
pause
