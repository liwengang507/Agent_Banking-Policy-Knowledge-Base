#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库混合搜索接口
提供vDB + BM25混合搜索功能
"""

from search_engine import KnowledgeBaseSearchEngine
import json

def main():
    """混合搜索接口主函数"""
    print("=== 银行行业政策知识库混合搜索引擎 ===")
    print("结合BM25和TF-IDF算法的混合搜索系统")
    print("=" * 50)
    
    try:
        # 初始化搜索引擎
        search_engine = KnowledgeBaseSearchEngine(".")
        
        # 显示统计信息
        stats = search_engine.get_statistics()
        print(f"\n📊 知识库统计:")
        print(f"   文档总数: {stats['total_documents']}")
        print(f"   字符总数: {stats['total_characters']:,}")
        print(f"   关键词总数: {stats['total_keywords']}")
        print(f"   主题总数: {stats['total_topics']}")
        
        print(f"\n🔥 热门关键词:")
        for kw in stats['popular_keywords']:
            print(f"   {kw['keyword']}: {kw['frequency']}次")
        
        # 混合搜索演示
        print(f"\n🔍 混合搜索演示:")
        
        # 测试查询列表
        test_queries = [
            "普惠金融",
            "小微企业",
            "金融稳定",
            "货币政策",
            "风险监管"
        ]
        
        for query in test_queries:
            print(f"\n--- 搜索: '{query}' ---")
            results = search_engine.hybrid_search(query, 2)
            
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   混合分数: {result['hybrid_score']:.4f}")
                print(f"   BM25分数: {result['bm25_score']:.4f}")
                print(f"   TF-IDF分数: {result['tfidf_score']:.4f}")
                print(f"   作者: {result['author']}")
                print(f"   发布时间: {result['publish_date']}")
                
                # 显示上下文
                if result['context']:
                    print(f"   相关段落: {len(result['context'])}个")
                    for j, ctx in enumerate(result['context'][:1], 1):
                        print(f"     段落{j}: {ctx['content'][:100]}...")
        
        # 主题混合搜索演示
        print(f"\n📚 主题混合搜索演示:")
        topics = ["普惠金融", "经济展望", "金融稳定", "政策法规"]
        
        for topic in topics:
            print(f"\n--- 主题: '{topic}' ---")
            results = search_engine.search_by_topic_hybrid(topic, 1)
            
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   混合分数: {result['hybrid_score']:.4f}")
                print(f"   主题关键词: {', '.join(result['topic_keywords'])}")
        
        print(f"\n✅ 混合搜索功能演示完成!")
        print(f"\n💡 使用说明:")
        print(f"   - 混合搜索结合了BM25和TF-IDF两种算法")
        print(f"   - BM25权重: 0.6 (适合精确匹配)")
        print(f"   - TF-IDF权重: 0.4 (适合语义相似)")
        print(f"   - 结果按混合分数排序，提供更准确的搜索体验")
        
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main() 