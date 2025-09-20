#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库搜索界面
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from search.search_engine import KnowledgeBaseSearchEngine

def main():
    """主函数"""
    print("🏦 银行行业政策知识库搜索系统")
    print("=" * 50)
    
    # 初始化搜索引擎
    search_engine = KnowledgeBaseSearchEngine(".")
    
    # 显示统计信息
    stats = search_engine.get_statistics()
    print(f"📚 文档总数: {stats['total_documents']}")
    print(f"📝 字符总数: {stats['total_characters']:,}")
    print(f"🔑 关键词总数: {stats['total_keywords']}")
    
    # 显示热门关键词
    print(f"\n🔥 热门关键词:")
    for kw in stats['popular_keywords']:
        print(f"   {kw['keyword']}: {kw['frequency']}次")
    
    # 测试搜索功能
    print(f"\n🔍 搜索测试:")
    results = search_engine.search_by_keyword("普惠金融", 3)
    for result in results:
        print(f"   📄 {result['title']} (相关性: {result.get('relevance_score', 0):.2f})")
    
    print("\n✅ 知识库构建完成！")

if __name__ == "__main__":
    main() 