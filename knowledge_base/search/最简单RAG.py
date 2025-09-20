#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的RAG系统
"""

import streamlit as st

# 设置页面配置
st.set_page_config(
    page_title="RAG系统",
    page_icon="🏦",
    layout="wide"
)

def main():
    """主函数"""
    st.title("🏦 银行政策知识库RAG系统")
    st.write("这是一个简单的RAG问答系统")
    
    # 显示成功信息
    st.success("✅ 系统启动成功！")
    
    # 问题输入
    question = st.text_input("请输入问题:", placeholder="例如：普惠金融的发展现状如何？")
    
    if st.button("搜索"):
        if question:
            # 简单的模拟答案
            st.write("**答案:** 基于银行政策文档分析，普惠金融发展态势良好，各项指标均达到预期目标。")
            st.write("**置信度:** 0.85")
            st.write("**参考文档:** 普惠金融指标分析报告2023")
        else:
            st.warning("请输入问题")

if __name__ == "__main__":
    main()
