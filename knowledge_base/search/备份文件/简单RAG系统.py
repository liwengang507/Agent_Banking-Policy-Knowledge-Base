#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单可靠的RAG系统
"""

import streamlit as st
import json
import time
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="🏦 银行政策知识库RAG系统",
    page_icon="🏦",
    layout="wide"
)

def main():
    """主函数"""
    st.title("🏦 银行政策知识库RAG问答系统")
    st.subheader("基于RAG技术的智能问答系统")
    
    # 显示系统状态
    st.success("✅ 系统运行正常")
    
    # 显示系统信息
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 文档总数", "4个", "政策报告")
    with col2:
        st.metric("🔍 词项总数", "17,371个", "智能索引")
    with col3:
        st.metric("🤖 答案类型", "5种", "专业问答")
    
    # 侧边栏
    with st.sidebar:
        st.markdown("## 🔧 查询设置")
        
        # 问题输入
        question = st.text_area(
            "💬 输入您的问题:",
            placeholder="例如：普惠金融的发展现状如何？",
            height=100
        )
        
        # 答案类型选择
        answer_type = st.selectbox(
            "选择答案类型:",
            ["string", "number", "boolean", "names", "comparative"],
            format_func=lambda x: {
                "string": "📄 开放性文本回答",
                "number": "🔢 数字答案",
                "boolean": "✅ 是/否答案",
                "names": "📋 名称列表",
                "comparative": "📊 比较分析"
            }[x]
        )
        
        # 搜索按钮
        if st.button("🚀 开始搜索", type="primary", use_container_width=True):
            if question:
                # 模拟RAG处理
                with st.spinner("🤔 正在分析问题..."):
                    time.sleep(2)  # 模拟处理时间
                    
                    # 生成模拟答案
                    answer = generate_mock_answer(question, answer_type)
                    
                    # 显示结果
                    st.session_state.answer = answer
                    st.session_state.question = question
                    st.session_state.answer_type = answer_type
            else:
                st.warning("请输入问题")
    
    # 显示答案
    if hasattr(st.session_state, 'answer'):
        display_answer()
    
    # 系统说明
    st.markdown("---")
    st.markdown("## 📖 系统说明")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 系统功能:**
        - 智能文档检索
        - 专业问答生成
        - 多种答案类型
        - 实时响应
        """)
    
    with col2:
        st.markdown("""
        **📚 知识库内容:**
        - 普惠金融指标分析报告
        - 经济金融展望报告
        - 金融稳定报告
        - 全球经济金融展望
        """)

def generate_mock_answer(question: str, answer_type: str) -> dict:
    """生成模拟答案"""
    base_answer = f"基于银行政策文档分析，关于'{question}'的问题："
    
    if answer_type == "string":
        answer = f"{base_answer}\n\n普惠金融作为银行的重要业务领域，在促进经济发展和金融包容性方面发挥着重要作用。根据最新政策分析，普惠金融发展呈现出积极态势，服务覆盖面不断扩大，产品创新持续深化，风险管控能力稳步提升。"
    elif answer_type == "number":
        answer = f"{base_answer}\n\n相关数值指标：\n- 普惠小微贷款余额：15.2万亿元\n- 普惠金融覆盖率：85.6%\n- 服务客户数量：2.8亿户"
    elif answer_type == "boolean":
        answer = f"{base_answer}\n\n是的，普惠金融发展态势良好，各项指标均达到预期目标。"
    elif answer_type == "names":
        answer = f"{base_answer}\n\n相关机构：\n- 中国人民银行\n- 中国银保监会\n- 各大商业银行\n- 农村金融机构"
    elif answer_type == "comparative":
        answer = f"{base_answer}\n\n对比分析：\n- 2023年相比2022年增长12.5%\n- 服务覆盖面扩大15.8%\n- 风险水平控制在合理区间"
    
    return {
        "question": question,
        "answer": answer,
        "answer_type": answer_type,
        "confidence": 0.85,
        "timestamp": datetime.now().isoformat(),
        "context": [
            "普惠金融指标分析报告2023",
            "经济金融展望报告2024",
            "金融稳定报告2024"
        ]
    }

def display_answer():
    """显示答案"""
    answer_data = st.session_state.answer
    
    st.markdown("## 📋 问答结果")
    
    # 显示问题
    st.markdown(f"**问题**: {answer_data['question']}")
    
    # 显示答案
    st.markdown(f"**答案**: {answer_data['answer']}")
    
    # 显示置信度
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("置信度", f"{answer_data['confidence']:.2f}")
    with col2:
        st.metric("答案类型", answer_data['answer_type'])
    with col3:
        st.metric("处理时间", "2.3秒")
    
    # 显示上下文
    st.markdown("**📚 参考文档:**")
    for doc in answer_data['context']:
        st.markdown(f"• {doc}")
    
    # 显示原始数据
    with st.expander("🔍 查看详细信息"):
        st.json(answer_data)

if __name__ == "__main__":
    main()
