@echo off
chcp 65001 >nul
title 银行政策知识库RAG问答系统

echo ============================================================
echo 🏦 银行政策知识库RAG问答系统
echo ============================================================
echo.

REM 切换到正确目录
cd /d "D:\ai\AI大模型开发项目\银行行业政策知识库\pdf_reports\knowledge_base\search"

REM 检查文件是否存在
if not exist "终极解决方案.py" (
    echo ❌ 找不到终极解决方案.py文件
    echo 当前目录: %CD%
    dir
    pause
    exit /b 1
)

echo ✅ 找到应用文件
echo 当前目录: %CD%

REM 启动应用
echo 🚀 启动RAG问答系统...
echo ============================================================
echo 💡 浏览器将自动打开: http://localhost:8501
echo 💡 按 Ctrl+C 停止服务器
echo ============================================================
echo.

streamlit run 终极解决方案.py --server.port 8501 --server.address localhost

pause
