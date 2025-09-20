#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库启动脚本
提供多种搜索界面选择
"""

import sys
import os
from pathlib import Path

def display_menu():
    """显示启动菜单"""
    print("\n" + "="*60)
    print("银行行业政策知识库启动器")
    print("="*60)
    print("基于4个重要银行政策报告构建的专业知识库")
    print("支持关键词搜索、主题搜索和混合搜索")
    print("="*60)
    print("\n请选择启动方式:")
    print("   1. 交互式命令行界面")
    print("   2. Web浏览器界面")
    print("   3. 简单混合搜索演示")
    print("   4. 知识库统计信息")
    print("   5. 查看帮助信息")
    print("   0. 退出")
    print("   " + "-"*50)

def start_interactive():
    """启动交互式界面"""
    print("\n启动交互式搜索界面...")
    try:
        from search.interactive_search import main
        main()
    except Exception as e:
        print("启动失败: " + str(e))

def start_web():
    """启动Web界面"""
    print("\n启动Web界面...")
    print("提示: 启动后请在浏览器中访问 http://localhost:5000")
    print("正在启动Web服务器...")
    try:
        from search.web_interface import app, initialize_engines
        if initialize_engines():
            print("Web服务器启动成功!")
            print("访问地址: http://localhost:5000")
            app.run(debug=False, host='0.0.0.0', port=5000)
        else:
            print("搜索引擎初始化失败")
    except Exception as e:
        print("启动失败: " + str(e))

def start_simple_demo():
    """启动简单演示"""
    print("\n启动简单混合搜索演示...")
    try:
        from search.simple_hybrid import main
        main()
    except Exception as e:
        print("启动失败: " + str(e))

def show_stats():
    """显示知识库统计信息"""
    print("\n知识库统计信息")
    print("="*50)
    try:
        from search.search_engine import KnowledgeBaseSearchEngine
        search_engine = KnowledgeBaseSearchEngine(".")
        stats = search_engine.get_statistics()
        
        print(f"文档总数: {stats['total_documents']}")
        print(f"字符总数: {stats['total_characters']:,}")
        print(f"关键词总数: {stats['total_keywords']}")
        print(f"主题总数: {stats['total_topics']}")
        
        print(f"\n热门关键词:")
        for i, kw in enumerate(stats['popular_keywords'][:10], 1):
            print(f"   {i:2d}. {kw['keyword']}: {kw['frequency']}次")
        
        print(f"\n文档列表:")
        documents = search_engine.document_index.get("documents", [])
        for i, doc in enumerate(documents, 1):
            print(f"   {i}. {doc['title']}")
            print(f"      作者: {doc['author']}")
            print(f"      发布时间: {doc['publish_date']}")
            print(f"      文件大小: {doc['file_size']}")
            print(f"      字符数: {doc['char_count']:,}")
            print()
        
    except Exception as e:
        print("获取统计信息失败: " + str(e))

def show_help():
    """显示帮助信息"""
    print("\n帮助信息")
    print("="*50)
    print("搜索功能说明:")
    print("   - 关键词搜索: 输入精确的关键词进行搜索")
    print("   - 主题搜索: 按主题分类浏览内容")
    print("   - 混合搜索: 结合BM25和TF-IDF算法，提供更准确的搜索结果")
    
    print("\n可用主题:")
    print("   - 普惠金融: 普惠金融相关政策和发展情况")
    print("   - 经济展望: 经济形势分析和预测")
    print("   - 金融稳定: 金融体系稳定性和风险监管")
    print("   - 政策法规: 相关政策和法规文件")
    
    print("\n搜索技巧:")
    print("   - 使用专业术语获得更好结果")
    print("   - 尝试不同的关键词组合")
    print("   - 查看相关上下文理解完整含义")
    
    print("\n快速开始:")
    print("   1. 选择交互式界面进行命令行搜索")
    print("   2. 选择Web界面进行浏览器搜索")
    print("   3. 查看统计信息了解知识库概况")
    
    print("\n文件结构:")
    print("   knowledge_base/")
    print("   ├── search/           # 搜索功能")
    print("   ├── index/            # 索引文件")
    print("   ├── data/             # 原始数据")
    print("   └── categories/       # 分类目录")

def main():
    """主函数"""
    while True:
        display_menu()
        
        try:
            choice = input("\n请选择操作 (0-5): ").strip()
            
            if choice == '0':
                print("\n感谢使用银行行业政策知识库！")
                break
            elif choice == '1':
                start_interactive()
            elif choice == '2':
                start_web()
            elif choice == '3':
                start_simple_demo()
            elif choice == '4':
                show_stats()
            elif choice == '5':
                show_help()
            else:
                print("无效选择，请输入 0-5 之间的数字")
                
        except KeyboardInterrupt:
            print("\n\n用户中断，感谢使用！")
            break
        except Exception as e:
            print("发生错误: " + str(e))

if __name__ == "__main__":
    main()
