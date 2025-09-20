#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试应用
"""

import streamlit as st

# 设置页面配置
st.set_page_config(
    page_title="简单测试",
    page_icon="🧪",
    layout="wide"
)

def main():
    """主函数"""
    st.title("🧪 简单测试应用")
    st.write("这是一个简单的测试应用，用于验证Streamlit是否正常工作。")
    
    # 显示成功信息
    st.success("✅ 应用运行正常！")
    
    # 简单的交互
    name = st.text_input("请输入您的姓名：")
    if name:
        st.write(f"您好，{name}！")
    
    # 按钮测试
    if st.button("点击测试"):
        st.balloons()
        st.write("🎉 按钮工作正常！")

if __name__ == "__main__":
    main()
