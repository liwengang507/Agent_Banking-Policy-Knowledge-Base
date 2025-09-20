#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库RAG集成模块（修复版）
将RAG提示模板与搜索引擎集成，提供完整的问答功能
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import logging

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from search_engine import KnowledgeBaseSearchEngine
from rag_prompts import (
    BaseRAGPrompt, 
    AnswerWithRAGContextStringPrompt,
    AnswerWithRAGContextNumberPrompt,
    AnswerWithRAGContextBooleanPrompt,
    AnswerWithRAGContextNamesPrompt,
    ComparativeAnswerPrompt,
    create_rag_prompt
)

logger = logging.getLogger(__name__)

class RAGQuestionAnsweringSystem:
    """RAG问答系统"""
    
    def __init__(self, base_path: str = "."):
        """
        初始化RAG问答系统
        
        Args:
            base_path: 知识库根目录路径
        """
        self.base_path = Path(base_path)
        self.search_engine = None
        self.prompt_templates = {}
        
        # 初始化搜索引擎
        self._initialize_search_engine()
        
        # 初始化提示模板
        self._initialize_prompt_templates()
        
        logger.info("RAG问答系统初始化完成")
    
    def _initialize_search_engine(self):
        """初始化搜索引擎"""
        try:
            # 修复路径问题：如果从search目录运行，需要指向父目录
            if str(self.base_path) == ".":
                # 检查当前是否在search目录中
                if current_dir.name == "search":
                    knowledge_base_path = current_dir.parent
                else:
                    knowledge_base_path = self.base_path
            else:
                knowledge_base_path = self.base_path
                
            logger.info(f"使用知识库路径: {knowledge_base_path}")
            self.search_engine = KnowledgeBaseSearchEngine(str(knowledge_base_path))
            logger.info("搜索引擎初始化成功")
        except Exception as e:
            logger.error(f"搜索引擎初始化失败: {e}")
            self.search_engine = None
    
    def _initialize_prompt_templates(self):
        """初始化提示模板"""
        if self.search_engine:
            self.prompt_templates = {
                "string": AnswerWithRAGContextStringPrompt(self.search_engine),
                "number": AnswerWithRAGContextNumberPrompt(self.search_engine),
                "boolean": AnswerWithRAGContextBooleanPrompt(self.search_engine),
                "names": AnswerWithRAGContextNamesPrompt(self.search_engine),
                "comparative": ComparativeAnswerPrompt(self.search_engine)
            }
            logger.info("提示模板初始化成功")
        else:
            logger.warning("搜索引擎未初始化，提示模板无法创建")
    
    def ask_question(self, question: str, answer_type: str = "string", 
                    limit: int = 5, **kwargs) -> Dict[str, Any]:
        """
        回答问题
        
        Args:
            question: 用户问题
            answer_type: 答案类型 ("string", "number", "boolean", "names", "comparative")
            limit: 检索文档数量限制
            **kwargs: 其他参数
            
        Returns:
            包含答案和元数据的字典
        """
        if not self.search_engine:
            return {
                "answer": "搜索引擎未初始化",
                "error": "搜索引擎未初始化",
                "success": False
            }
        
        if answer_type not in self.prompt_templates:
            return {
                "answer": f"不支持的答案类型: {answer_type}",
                "error": f"不支持的答案类型: {answer_type}",
                "success": False
            }
        
        try:
            # 获取提示模板
            prompt_template = self.prompt_templates[answer_type]
            
            # 搜索相关文档
            search_results = self.search_engine.hybrid_search(question, limit)
            
            if not search_results:
                return {
                    "answer": "未找到相关文档信息",
                    "context": [],
                    "search_results": [],
                    "success": False
                }
            
            # 提取上下文信息
            context = []
            for result in search_results:
                context_item = {
                    "title": result.get("title", ""),
                    "content": result.get("context", []),
                    "score": result.get("hybrid_score", 0),
                    "document_id": result.get("document_id", ""),
                    "author": result.get("author", ""),
                    "publish_date": result.get("publish_date", "")
                }
                context.append(context_item)
            
            # 格式化提示
            prompt = prompt_template.format_prompt(question, context)
            
            return {
                "question": question,
                "answer_type": answer_type,
                "prompt": prompt,
                "context": context,
                "search_results": search_results,
                "success": True,
                "metadata": {
                    "context_count": len(context),
                    "search_scores": [r.get("hybrid_score", 0) for r in search_results],
                    "documents": [r.get("title", "") for r in search_results]
                }
            }
            
        except Exception as e:
            logger.error(f"问答处理失败: {e}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            return {
                "answer": f"处理问题时发生错误: {str(e)}",
                "error": str(e),
                "success": False,
                "traceback": traceback.format_exc()
            }
    
    def get_available_answer_types(self) -> List[str]:
        """获取可用的答案类型"""
        return list(self.prompt_templates.keys())
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        return {
            "search_engine_available": self.search_engine is not None,
            "available_answer_types": self.get_available_answer_types(),
            "base_path": str(self.base_path),
            "total_documents": len(self.search_engine.documents) if self.search_engine else 0
        }

def main():
    """主函数"""
    print("=== 银行行业政策知识库RAG集成测试（修复版） ===")
    
    try:
        # 初始化RAG系统
        rag_system = RAGQuestionAnsweringSystem(".")
        
        # 显示系统信息
        info = rag_system.get_system_info()
        print(f"\n📊 系统信息:")
        print(f"   搜索引擎状态: {'可用' if info['search_engine_available'] else '不可用'}")
        print(f"   文档总数: {info['total_documents']}")
        print(f"   可用答案类型: {', '.join(info['available_answer_types'])}")
        
        if not rag_system.search_engine:
            print("\n❌ 搜索引擎不可用，无法进行测试")
            return
        
        # 测试不同类型的问题
        test_questions = [
            ("普惠小微贷款的余额是多少？", "number"),
            ("普惠金融是否在增长？", "boolean"),
            ("涉及普惠金融的机构有哪些？", "names"),
            ("比较不同时期的普惠金融发展情况", "comparative"),
            ("请详细介绍普惠金融的发展现状", "string")
        ]
        
        print(f"\n🔍 测试问答功能:")
        for i, (question, answer_type) in enumerate(test_questions, 1):
            print(f"\n{i}. 问题: {question}")
            print(f"   答案类型: {answer_type}")
            
            result = rag_system.ask_question(question, answer_type, limit=3)
            
            if result["success"]:
                print(f"   ✅ 成功 - 检索到{len(result['context'])}个相关文档")
                print(f"   📝 提示长度: {len(result['prompt'])}字符")
                print(f"   📊 搜索分数: {[f'{s:.3f}' for s in result['metadata']['search_scores']]}")
            else:
                print(f"   ❌ 失败 - {result.get('error', '未知错误')}")
                if 'traceback' in result:
                    print(f"   详细错误: {result['traceback']}")
        
        print(f"\n✅ RAG集成测试完成!")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        logger.error(f"RAG集成测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
