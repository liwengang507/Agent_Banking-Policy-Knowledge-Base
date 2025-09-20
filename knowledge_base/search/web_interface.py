#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库Web界面
基于Flask的Web搜索界面
"""

from flask import Flask, render_template, request, jsonify
import json
import sys
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from search_engine import KnowledgeBaseSearchEngine
from simple_hybrid import SimpleHybridSearch

app = Flask(__name__)

# 全局搜索引擎实例
search_engine = None
hybrid_engine = None

def initialize_engines():
    """初始化搜索引擎"""
    global search_engine, hybrid_engine
    try:
        search_engine = KnowledgeBaseSearchEngine(".")
        hybrid_engine = SimpleHybridSearch(".")
        return True
    except Exception as e:
        print(f"初始化失败: {e}")
        return False

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """获取知识库统计信息"""
    if not search_engine:
        return jsonify({"error": "搜索引擎未初始化"}), 500
    
    stats = search_engine.get_statistics()
    return jsonify(stats)

@app.route('/api/search/keyword')
def search_keyword():
    """关键词搜索API"""
    if not search_engine:
        return jsonify({"error": "搜索引擎未初始化"}), 500
    
    keyword = request.args.get('q', '').strip()
    limit = int(request.args.get('limit', 10))
    
    if not keyword:
        return jsonify({"error": "请输入搜索关键词"}), 400
    
    try:
        results = search_engine.search_by_keyword(keyword, limit)
        return jsonify({
            "query": keyword,
            "results": results,
            "total": len(results)
        })
    except Exception as e:
        return jsonify({"error": f"搜索失败: {str(e)}"}), 500

@app.route('/api/search/topic')
def search_topic():
    """主题搜索API"""
    if not search_engine:
        return jsonify({"error": "搜索引擎未初始化"}), 500
    
    topic = request.args.get('q', '').strip()
    limit = int(request.args.get('limit', 10))
    
    if not topic:
        return jsonify({"error": "请输入主题名称"}), 400
    
    try:
        results = search_engine.search_by_topic(topic, limit)
        return jsonify({
            "query": topic,
            "results": results,
            "total": len(results)
        })
    except Exception as e:
        return jsonify({"error": f"搜索失败: {str(e)}"}), 500

@app.route('/api/search/hybrid')
def search_hybrid():
    """混合搜索API"""
    if not hybrid_engine:
        return jsonify({"error": "混合搜索引擎未初始化"}), 500
    
    query = request.args.get('q', '').strip()
    limit = int(request.args.get('limit', 10))
    
    if not query:
        return jsonify({"error": "请输入搜索查询"}), 400
    
    try:
        results = hybrid_engine.hybrid_search(query, limit)
        return jsonify({
            "query": query,
            "results": results,
            "total": len(results)
        })
    except Exception as e:
        return jsonify({"error": f"搜索失败: {str(e)}"}), 500

@app.route('/api/documents')
def get_documents():
    """获取文档列表"""
    if not search_engine:
        return jsonify({"error": "搜索引擎未初始化"}), 500
    
    documents = search_engine.document_index.get("documents", [])
    return jsonify({"documents": documents})

if __name__ == '__main__':
    print("🏦 银行行业政策知识库Web界面")
    print("="*50)
    
    if initialize_engines():
        print("✅ 搜索引擎初始化完成")
        print("🌐 启动Web服务器...")
        print("📱 访问地址: http://localhost:5000")
        print("="*50)
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ 搜索引擎初始化失败")
