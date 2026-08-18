@echo off
chcp 65001 >nul
title Kindle Dashboard 自动更新
echo ========================================
echo   Kindle Dashboard 自动更新程序
echo ========================================
echo.
echo [%date% %time%] 开始运行...
echo.

cd /d "%~dp0"
python auto_update.py

echo.
echo [%date% %time%] 运行完成
pause
