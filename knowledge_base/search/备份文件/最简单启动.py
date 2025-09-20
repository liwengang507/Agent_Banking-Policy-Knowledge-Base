#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的Streamlit应用
"""

import streamlit as st
import subprocess
import sys
import os

def main():
    """主函数"""
    st.title("🏦 银行政策知识库RAG问答系统")
    st.write("系统正在启动中...")
    
    # 显示系统信息
    st.success("✅ 应用启动成功！")
    
    # 显示当前目录
    st.write(f"当前目录: {os.getcwd()}")
    
    # 显示文件列表
    st.write("可用文件:")
    files = os.listdir(".")
    for file in files:
        if file.endswith(".py"):
            st.write(f"- {file}")
    
    # 简单的问答界面
    st.subheader("💬 问答测试")
    question = st.text_input("输入问题:", placeholder="例如：普惠金融的发展现状如何？")
    
    if st.button("提交问题"):
        if question:
            st.write(f"您的问题: {question}")
            st.write("答案: 这是一个测试回答。实际系统会基于知识库提供专业答案。")
        else:
            st.warning("请输入问题")

if __name__ == "__main__":
    main()
