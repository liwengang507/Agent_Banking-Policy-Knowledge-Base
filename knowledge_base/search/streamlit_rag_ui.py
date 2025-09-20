#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库RAG问答系统 - Streamlit界面
基于现代化设计的智能问答界面
"""

import streamlit as st
import sys
from pathlib import Path
import time
import logging
from typing import Dict, Any, List

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from fixed_rag_integration import RAGQuestionAnsweringSystem

# 设置页面配置
st.set_page_config(
    page_title="银行政策知识库RAG问答系统",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 主标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #6366f1;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 侧边栏样式 */
    .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* 卡片样式 */
    .result-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .result-header {
        font-weight: bold;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .similarity-score {
        background: #f1f5f9;
        color: #475569;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* 进度条样式 */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 指标样式 */
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_rag_system():
    """初始化RAG系统（缓存）"""
    try:
        rag_system = RAGQuestionAnsweringSystem(".")
        return rag_system
    except Exception as e:
        st.error(f"RAG系统初始化失败: {e}")
        return None

def display_header():
    """显示页面头部"""
    st.markdown('<h1 class="main-title">🏦 银行政策知识库RAG问答系统</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">基于RAG技术的智能问答系统，支持银行政策文档的专业问答</p>', unsafe_allow_html=True)
    
    # 显示系统特性
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 文档总数", "4个", "政策报告")
    with col2:
        st.metric("🔍 词项总数", "17,371个", "智能索引")
    with col3:
        st.metric("🤖 答案类型", "5种", "专业问答")

def display_sidebar():
    """显示侧边栏配置"""
    st.sidebar.markdown("## 🔧 查询设置")
    
    # 问题输入
    question = st.sidebar.text_area(
        "💬 输入您的问题",
        placeholder="请输入您想要查询的问题...",
        height=100,
        help="支持关于普惠金融、经济展望、金融稳定等政策问题的查询"
    )
    
    # 答案类型选择
    st.sidebar.markdown("### 📝 答案类型")
    answer_type = st.sidebar.selectbox(
        "选择问题的答案类型",
        options=["string", "number", "boolean", "names", "comparative"],
        index=0,
        format_func=lambda x: {
            "string": "📄 开放性文本回答",
            "number": "🔢 数字答案",
            "boolean": "✅ 是/否答案", 
            "names": "📋 名称列表",
            "comparative": "📊 比较分析"
        }[x]
    )
    
    # 检索设置
    st.sidebar.markdown("### ⚙️ 检索设置")
    limit = st.sidebar.slider(
        "检索文档数量",
        min_value=1,
        max_value=10,
        value=5,
        help="设置检索相关文档的数量"
    )
    
    # 高级选项
    with st.sidebar.expander("🔧 高级选项"):
        show_prompt = st.checkbox("显示生成的提示模板", value=False)
        show_metadata = st.checkbox("显示详细元数据", value=False)
    
    return question, answer_type, limit, show_prompt, show_metadata

def display_search_results(rag_system, question: str, answer_type: str, limit: int, 
                          show_prompt: bool, show_metadata: bool):
    """显示搜索结果"""
    if not question.strip():
        st.warning("⚠️ 请输入您的问题")
        return
    
    # 显示进度条
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 步骤1: 初始化
        status_text.text("🚀 初始化RAG系统...")
        progress_bar.progress(20)
        time.sleep(0.5)
        
        # 步骤2: 搜索文档
        status_text.text("🔍 搜索相关文档...")
        progress_bar.progress(40)
        
        # 执行问答
        result = rag_system.ask_question(question, answer_type, limit)
        progress_bar.progress(80)
        
        # 步骤3: 生成结果
        status_text.text("🤖 生成答案...")
        progress_bar.progress(100)
        time.sleep(0.5)
        
        # 清除进度条
        progress_bar.empty()
        status_text.empty()
        
        if result['success']:
            # 显示查询摘要
            st.markdown("### 📋 查询摘要")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("问题类型", answer_type.upper())
            with col2:
                st.metric("检索文档", f"{len(result['context'])}个")
            with col3:
                st.metric("处理时间", f"{time.time():.2f}s")
            
            # 显示检索到的文档
            st.markdown("### 📚 检索结果")
            
            for i, ctx in enumerate(result['context'], 1):
                with st.expander(f"📄 结果 {i} - {ctx['title']}", expanded=(i==1)):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**文档标题:** {ctx['title']}")
                        if ctx.get('author'):
                            st.markdown(f"**作者:** {ctx['author']}")
                        if ctx.get('publish_date'):
                            st.markdown(f"**发布日期:** {ctx['publish_date']}")
                    
                    with col2:
                        st.markdown(f'<span class="similarity-score">相似度: {ctx["score"]:.3f}</span>', 
                                   unsafe_allow_html=True)
                    
                    # 显示文档内容
                    if isinstance(ctx['content'], list):
                        content_text = '\n'.join([str(item) for item in ctx['content']])
                    else:
                        content_text = str(ctx['content'])
                    
                    st.markdown("**文档内容:**")
                    st.text_area("", content_text, height=200, key=f"content_{i}")
            
            # 显示生成的提示模板
            if show_prompt:
                st.markdown("### 🤖 生成的提示模板")
                st.text_area("提示模板", result['prompt'], height=300)
            
            # 显示详细元数据
            if show_metadata:
                st.markdown("### 📊 详细元数据")
                metadata = result.get('metadata', {})
                
                col1, col2 = st.columns(2)
                with col1:
                    st.json({
                        "上下文数量": metadata.get('context_count', 0),
                        "搜索分数": [f"{s:.3f}" for s in metadata.get('search_scores', [])],
                        "文档列表": metadata.get('documents', [])
                    })
                
                with col2:
                    st.json({
                        "问题": result.get('question', ''),
                        "答案类型": result.get('answer_type', ''),
                        "成功状态": result.get('success', False)
                    })
            
            # 显示成功消息
            st.success(f"✅ 成功检索到 {len(result['context'])} 个相关文档，生成了 {len(result['prompt'])} 字符的提示模板")
            
        else:
            st.error(f"❌ 问答失败: {result.get('error', '未知错误')}")
            if 'traceback' in result:
                with st.expander("查看详细错误信息"):
                    st.code(result['traceback'])
    
    except Exception as e:
        st.error(f"❌ 处理问题时发生错误: {e}")
        import traceback
        with st.expander("查看详细错误信息"):
            st.code(traceback.format_exc())

def display_footer():
    """显示页面底部"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 1rem;">
        <p>🏦 银行行业政策知识库RAG问答系统 | 基于RAG技术的智能问答</p>
        <p>支持普惠金融、经济展望、金融稳定等政策文档的专业问答</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """主函数"""
    # 初始化RAG系统
    rag_system = initialize_rag_system()
    
    if rag_system is None:
        st.error("❌ RAG系统初始化失败，请检查系统配置")
        return
    
    # 显示页面头部
    display_header()
    
    # 显示侧边栏
    question, answer_type, limit, show_prompt, show_metadata = display_sidebar()
    
    # 显示主要内容区域
    st.markdown("## 🔍 检索结果")
    
    # 搜索按钮
    if st.button("🚀 开始搜索", type="primary", use_container_width=True):
        display_search_results(rag_system, question, answer_type, limit, show_prompt, show_metadata)
    
    # 显示系统信息
    with st.expander("ℹ️ 系统信息"):
        info = rag_system.get_system_info()
        st.json({
            "搜索引擎状态": "可用" if info['search_engine_available'] else "不可用",
            "文档总数": info['total_documents'],
            "可用答案类型": info['available_answer_types'],
            "知识库路径": info['base_path']
        })
    
    # 显示页面底部
    display_footer()

if __name__ == "__main__":
    main()
