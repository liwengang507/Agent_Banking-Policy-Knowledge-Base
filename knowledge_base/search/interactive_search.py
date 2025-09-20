#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库交互式搜索界面
提供友好的用户交互体验
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from search_engine import KnowledgeBaseSearchEngine
from simple_hybrid import SimpleHybridSearch

class InteractiveSearchInterface:
    """交互式搜索界面"""
    
    def __init__(self):
        """初始化搜索界面"""
        self.search_engine = None
        self.hybrid_engine = None
        self.running = True
        
    def initialize_engines(self):
        """初始化搜索引擎"""
        try:
            print("正在初始化搜索引擎...")
            self.search_engine = KnowledgeBaseSearchEngine(".")
            self.hybrid_engine = SimpleHybridSearch(".")
            print("搜索引擎初始化完成！")
            return True
        except Exception as e:
            print("初始化失败: " + str(e))
            return False
    
    def display_welcome(self):
        """显示欢迎信息"""
        print("\n" + "="*60)
        print("银行行业政策知识库交互式搜索系统")
        print("="*60)
        print("基于4个重要银行政策报告构建的专业知识库")
        print("支持关键词搜索、主题搜索和混合搜索")
        print("="*60)
    
    def display_statistics(self):
        """显示知识库统计信息"""
        if not self.search_engine:
            return
            
        stats = self.search_engine.get_statistics()
        print(f"\n知识库统计信息:")
        print(f"   文档总数: {stats['total_documents']}")
        print(f"   字符总数: {stats['total_characters']:,}")
        print(f"   关键词总数: {stats['total_keywords']}")
        print(f"   主题总数: {stats['total_topics']}")
        
        print(f"\n热门关键词:")
        for i, kw in enumerate(stats['popular_keywords'][:5], 1):
            print(f"   {i}. {kw['keyword']}: {kw['frequency']}次")
    
    def display_menu(self):
        """显示主菜单"""
        print(f"\n请选择搜索方式:")
        print(f"   1. 关键词搜索")
        print(f"   2. 主题搜索")
        print(f"   3. 混合搜索 (BM25 + TF-IDF)")
        print(f"   4. 查看知识库统计")
        print(f"   5. 查看文档列表")
        print(f"   6. 帮助信息")
        print(f"   0. 退出系统")
        print(f"   " + "-"*50)
    
    def keyword_search(self):
        """关键词搜索"""
        print(f"\n 关键词搜索")
        print(f" 提示: 输入关键词进行精确搜索，如: 普惠金融、小微企业、货币政策等")
        
        while True:
            keyword = input(f"\n请输入搜索关键词 (输入 'back' 返回主菜单): ").strip()
            
            if keyword.lower() == 'back':
                break
                
            if not keyword:
                print(" 请输入有效的关键词")
                continue
            
            try:
                print(f"\n 正在搜索: '{keyword}'...")
                results = self.search_engine.search_by_keyword(keyword, 5)
                
                if not results:
                    print(f" 未找到包含 '{keyword}' 的文档")
                    continue
                
                print(f"\n 搜索结果 (共{len(results)}个):")
                for i, result in enumerate(results, 1):
                    print(f"\n{i}.  {result['title']}")
                    print(f"    作者: {result['author']}")
                    print(f"    发布时间: {result['publish_date']}")
                    print(f"    相关性: {result['relevance']:.3f}")
                    print(f"    摘要: {result['summary'][:100]}...")
                    
                    if result.get('context'):
                        print(f"    相关段落: {len(result['context'])}个")
                        for j, ctx in enumerate(result['context'][:2], 1):
                            print(f"      段落{j}: {ctx['content'][:80]}...")
                
            except Exception as e:
                print(f" 搜索出错: {e}")
    
    def topic_search(self):
        """主题搜索"""
        print(f"\n 主题搜索")
        print(f" 可用主题: 普惠金融、经济展望、金融稳定、政策法规")
        
        while True:
            topic = input(f"\n请输入主题名称 (输入 'back' 返回主菜单): ").strip()
            
            if topic.lower() == 'back':
                break
                
            if not topic:
                print(" 请输入有效的主题名称")
                continue
            
            try:
                print(f"\n 正在搜索主题: '{topic}'...")
                results = self.search_engine.search_by_topic(topic, 5)
                
                if not results:
                    print(f" 未找到主题 '{topic}' 的相关文档")
                    continue
                
                print(f"\n 主题搜索结果 (共{len(results)}个):")
                for i, result in enumerate(results, 1):
                    print(f"\n{i}.  {result['title']}")
                    print(f"    作者: {result['author']}")
                    print(f"    发布时间: {result['publish_date']}")
                    print(f"    主题相关性: {result['topic_relevance']:.3f}")
                    print(f"    摘要: {result['summary'][:100]}...")
                    
                    if result.get('topic_keywords'):
                        print(f"   🔑 主题关键词: {', '.join(result['topic_keywords'][:5])}")
                
            except Exception as e:
                print(f" 搜索出错: {e}")
    
    def hybrid_search(self):
        """混合搜索"""
        print(f"\n 混合搜索 (BM25 + TF-IDF)")
        print(f" 提示: 混合搜索结合了精确匹配和语义相似性，提供更准确的搜索结果")
        
        while True:
            query = input(f"\n请输入搜索查询 (输入 'back' 返回主菜单): ").strip()
            
            if query.lower() == 'back':
                break
                
            if not query:
                print(" 请输入有效的搜索查询")
                continue
            
            try:
                print(f"\n 正在进行混合搜索: '{query}'...")
                results = self.hybrid_engine.hybrid_search(query, 5)
                
                if not results:
                    print(f" 未找到与 '{query}' 相关的文档")
                    continue
                
                print(f"\n 混合搜索结果 (共{len(results)}个):")
                for i, result in enumerate(results, 1):
                    print(f"\n{i}.  {result['title']}")
                    print(f"    混合分数: {result['hybrid_score']:.4f}")
                    print(f"    BM25分数: {result['bm25_score']:.4f}")
                    print(f"   📈 TF-IDF分数: {result['tfidf_score']:.4f}")
                    print(f"    摘要: {result['summary'][:100]}...")
                
            except Exception as e:
                print(f" 搜索出错: {e}")
    
    def show_document_list(self):
        """显示文档列表"""
        if not self.search_engine:
            return
            
        documents = self.search_engine.document_index.get("documents", [])
        
        print(f"\n 知识库文档列表:")
        print(f"   " + "-"*50)
        
        for i, doc in enumerate(documents, 1):
            print(f"\n{i}.  {doc['title']}")
            print(f"    作者: {doc['author']}")
            print(f"    发布时间: {doc['publish_date']}")
            print(f"    文件大小: {doc['file_size']}")
            print(f"    字符数: {doc['char_count']:,}")
            print(f"    分类: {', '.join(doc['categories'])}")
            print(f"   🔑 关键词: {', '.join(doc['keywords'][:5])}")
            print(f"    摘要: {doc['summary'][:150]}...")
    
    def show_help(self):
        """显示帮助信息"""
        print(f"\n❓ 帮助信息")
        print(f"   " + "-"*50)
        print(f" 关键词搜索:")
        print(f"   - 输入精确的关键词进行搜索")
        print(f"   - 支持中文关键词，如: 普惠金融、小微企业")
        print(f"   - 显示相关性和上下文信息")
        
        print(f"\n 主题搜索:")
        print(f"   - 按主题分类浏览内容")
        print(f"   - 可用主题: 普惠金融、经济展望、金融稳定、政策法规")
        print(f"   - 显示主题相关性和关键词")
        
        print(f"\n 混合搜索:")
        print(f"   - 结合BM25和TF-IDF算法")
        print(f"   - 提供更准确的搜索结果")
        print(f"   - 显示详细的分数信息")
        
        print(f"\n 搜索技巧:")
        print(f"   - 使用专业术语获得更好结果")
        print(f"   - 尝试不同的关键词组合")
        print(f"   - 查看相关上下文理解完整含义")
    
    def run(self):
        """运行交互式界面"""
        self.display_welcome()
        
        if not self.initialize_engines():
            return
        
        self.display_statistics()
        
        while self.running:
            self.display_menu()
            
            try:
                choice = input(f"\n请选择操作 (0-6): ").strip()
                
                if choice == '0':
                    print(f"\n👋 感谢使用银行行业政策知识库！")
                    self.running = False
                elif choice == '1':
                    self.keyword_search()
                elif choice == '2':
                    self.topic_search()
                elif choice == '3':
                    self.hybrid_search()
                elif choice == '4':
                    self.display_statistics()
                elif choice == '5':
                    self.show_document_list()
                elif choice == '6':
                    self.show_help()
                else:
                    print(f" 无效选择，请输入 0-6 之间的数字")
                    
            except KeyboardInterrupt:
                print(f"\n\n👋 用户中断，感谢使用！")
                self.running = False
            except Exception as e:
                print(f" 发生错误: {e}")

def main():
    """主函数"""
    interface = InteractiveSearchInterface()
    interface.run()

if __name__ == "__main__":
    main()
