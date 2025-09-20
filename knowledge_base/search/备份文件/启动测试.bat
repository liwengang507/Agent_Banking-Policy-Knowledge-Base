@echo off
chcp 65001 >nul
title 启动Streamlit测试应用

echo ============================================================
echo 🧪 Streamlit测试应用启动器
echo ============================================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装
    pause
    exit /b 1
)
echo ✅ Python正常

REM 检查Streamlit
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 📦 安装Streamlit...
    python -m pip install streamlit
)
echo ✅ Streamlit正常

echo.
echo 🚀 启动测试应用...
echo ============================================================
echo 💡 浏览器将自动打开: http://localhost:8502
echo 💡 按 Ctrl+C 停止服务器
echo ============================================================
echo.

REM 启动应用
streamlit run 简单测试.py --server.port 8502 --server.address localhost

pause
