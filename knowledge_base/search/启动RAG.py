#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动RAG系统
"""

import subprocess
import sys
import webbrowser
import time
import threading

def main():
    """主函数"""
    print("=" * 50)
    print("银行政策知识库RAG系统")
    print("=" * 50)
    print()
    
    # 检查文件
    app_file = "长效思考RAG.py"
    print(f"应用文件: {app_file}")
    
    # 检查Streamlit
    try:
        import streamlit
        print("Streamlit已安装")
    except ImportError:
        print("安装Streamlit...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
        print("Streamlit安装完成")
    
    # 启动应用
    print()
    print("启动RAG系统...")
    print("=" * 50)
    print("浏览器将自动打开: http://localhost:8501")
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    print()
    
    # 等待3秒后自动打开浏览器
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:8501")
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # 启动Streamlit应用
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            app_file, 
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n应用已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == "__main__":
    main()
