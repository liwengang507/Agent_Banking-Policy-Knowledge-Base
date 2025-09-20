#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键启动RAG系统
"""

import subprocess
import sys
import os
import webbrowser
import time

def main():
    """主函数"""
    print("=" * 60)
    print("🏦 银行政策知识库RAG问答系统 - 一键启动")
    print("=" * 60)
    print()
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 检查文件是否存在
    app_file = "终极解决方案.py"
    if not os.path.exists(app_file):
        print(f"❌ 找不到 {app_file} 文件")
        print("可用文件:")
        for file in os.listdir("."):
            if file.endswith(".py"):
                print(f"  - {file}")
        return
    
    print(f"✅ 找到应用文件: {app_file}")
    
    # 检查Streamlit是否安装
    try:
        import streamlit
        print("✅ Streamlit已安装")
    except ImportError:
        print("📦 安装Streamlit...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit安装完成")
    
    # 启动应用
    print()
    print("🚀 启动RAG问答系统...")
    print("=" * 60)
    print("💡 浏览器将自动打开: http://localhost:8501")
    print("💡 按 Ctrl+C 停止服务器")
    print("=" * 60)
    print()
    
    # 等待2秒后自动打开浏览器
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:8501")
    
    import threading
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
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
