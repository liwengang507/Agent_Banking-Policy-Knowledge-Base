#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库RAG提示模板
支持多种类型的问答提示模板
"""

from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BaseRAGPrompt:
    """RAG提示模板基类"""
    
    def __init__(self, search_engine=None):
        """
        初始化RAG提示模板
        
        Args:
            search_engine: 搜索引擎实例
        """
        self.search_engine = search_engine
    
    def format_prompt(self, question: str, context: List[Dict[str, Any]]) -> str:
        """
        格式化提示模板
        
        Args:
            question: 用户问题
            context: 检索到的上下文信息
            
        Returns:
            格式化后的提示文本
        """
        raise NotImplementedError("子类必须实现format_prompt方法")
    
    def extract_answer(self, response: str) -> Any:
        """
        从响应中提取答案
        
        Args:
            response: 模型响应
            
        Returns:
            提取的答案
        """
        raise NotImplementedError("子类必须实现extract_answer方法")

class AnswerWithRAGContextNumberPrompt(BaseRAGPrompt):
    """数字答案RAG提示模板"""
    
    def format_prompt(self, question: str, context: List[Dict[str, Any]]) -> str:
        """格式化数字答案提示"""
        context_text = self._format_context(context)
        
        prompt = f"""基于以下银行政策文档内容，请回答用户的问题。如果问题涉及具体数字，请提供准确的数值。

文档内容：
{context_text}

用户问题：{question}

请基于上述文档内容，提供一个准确的数字答案。如果文档中没有相关信息，请回答"无法从文档中找到相关信息"。

答案格式：请直接提供数字，不要包含其他解释。"""
        
        return prompt
    
    def extract_answer(self, response: str) -> Optional[float]:
        """提取数字答案"""
        import re
        
        # 尝试提取数字
        numbers = re.findall(r'-?\d+\.?\d*', response)
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return None
        return None
    
    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """格式化上下文信息"""
        formatted_context = []
        for i, ctx in enumerate(context, 1):
            if isinstance(ctx, dict):
                title = ctx.get('title', f'文档{i}')
                content = ctx.get('content', ctx.get('context', ''))
                formatted_context.append(f"{i}. {title}\n{content}\n")
            else:
                formatted_context.append(f"{i}. {str(ctx)}\n")
        
        return '\n'.join(formatted_context)

class AnswerWithRAGContextBooleanPrompt(BaseRAGPrompt):
    """布尔答案RAG提示模板"""
    
    def format_prompt(self, question: str, context: List[Dict[str, Any]]) -> str:
        """格式化布尔答案提示"""
        context_text = self._format_context(context)
        
        prompt = f"""基于以下银行政策文档内容，请回答用户的问题。请用"是"或"否"来回答。

文档内容：
{context_text}

用户问题：{question}

请基于上述文档内容，用"是"或"否"来回答问题。如果文档中没有相关信息，请回答"无法确定"。

答案格式：请只回答"是"、"否"或"无法确定"。"""
        
        return prompt
    
    def extract_answer(self, response: str) -> Optional[bool]:
        """提取布尔答案"""
        response_lower = response.lower().strip()
        
        if "是" in response_lower or "yes" in response_lower or "true" in response_lower:
            return True
        elif "否" in response_lower or "no" in response_lower or "false" in response_lower:
            return False
        else:
            return None
    
    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """格式化上下文信息"""
        formatted_context = []
        for i, ctx in enumerate(context, 1):
            if isinstance(ctx, dict):
                title = ctx.get('title', f'文档{i}')
                content = ctx.get('content', ctx.get('context', ''))
                formatted_context.append(f"{i}. {title}\n{content}\n")
            else:
                formatted_context.append(f"{i}. {str(ctx)}\n")
        
        return '\n'.join(formatted_context)

class AnswerWithRAGContextNamesPrompt(BaseRAGPrompt):
    """名称列表答案RAG提示模板"""
    
    def format_prompt(self, question: str, context: List[Dict[str, Any]]) -> str:
        """格式化名称列表答案提示"""
        context_text = self._format_context(context)
        
        prompt = f"""基于以下银行政策文档内容，请回答用户的问题。如果问题涉及名称、机构、人员等，请列出所有相关的名称。

文档内容：
{context_text}

用户问题：{question}

请基于上述文档内容，列出所有相关的名称。如果文档中没有相关信息，请回答"未找到相关信息"。

答案格式：请以列表形式提供名称，每个名称占一行。"""
        
        return prompt
    
    def extract_answer(self, response: str) -> List[str]:
        """提取名称列表答案"""
        import re
        
        # 按行分割并清理
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        
        # 过滤掉空行和常见的非名称内容
        names = []
        for line in lines:
            # 跳过常见的非名称内容
            if any(skip in line.lower() for skip in ['答案', '回答', '根据', '基于', '文档', '内容']):
                continue
            if len(line) > 1:  # 过滤掉单字符
                names.append(line)
        
        return names
    
    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """格式化上下文信息"""
        formatted_context = []
        for i, ctx in enumerate(context, 1):
            if isinstance(ctx, dict):
                title = ctx.get('title', f'文档{i}')
                content = ctx.get('content', ctx.get('context', ''))
                formatted_context.append(f"{i}. {title}\n{content}\n")
            else:
                formatted_context.append(f"{i}. {str(ctx)}\n")
        
        return '\n'.join(formatted_context)

class ComparativeAnswerPrompt(BaseRAGPrompt):
    """比较分析答案RAG提示模板"""
    
    def format_prompt(self, question: str, context: List[Dict[str, Any]]) -> str:
        """格式化比较分析提示"""
        context_text = self._format_context(context)
        
        prompt = f"""基于以下银行政策文档内容，请对用户的问题进行详细的比较分析。

文档内容：
{context_text}

用户问题：{question}

请基于上述文档内容，进行详细的比较分析，包括：
1. 各个方面的具体数据或情况
2. 不同时期或不同对象之间的对比
3. 趋势分析和变化情况
4. 结论和建议

请提供结构化的比较分析结果。"""
        
        return prompt
    
    def extract_answer(self, response: str) -> Dict[str, Any]:
        """提取比较分析答案"""
        # 尝试解析结构化的比较分析
        analysis = {
            "comparison_points": [],
            "trends": [],
            "conclusions": [],
            "raw_response": response
        }
        
        # 简单的文本分析，提取关键信息
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if any(keyword in line for keyword in ['对比', '比较', '差异']):
                current_section = "comparison_points"
            elif any(keyword in line for keyword in ['趋势', '变化', '发展']):
                current_section = "trends"
            elif any(keyword in line for keyword in ['结论', '建议', '总结']):
                current_section = "conclusions"
            
            if current_section and line:
                analysis[current_section].append(line)
        
        return analysis
    
    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """格式化上下文信息"""
        formatted_context = []
        for i, ctx in enumerate(context, 1):
            if isinstance(ctx, dict):
                title = ctx.get('title', f'文档{i}')
                content = ctx.get('content', ctx.get('context', ''))
                formatted_context.append(f"{i}. {title}\n{content}\n")
            else:
                formatted_context.append(f"{i}. {str(ctx)}\n")
        
        return '\n'.join(formatted_context)

class AnswerWithRAGContextStringPrompt(BaseRAGPrompt):
    """开放性文本答案RAG提示模板"""
    
    def __init__(self, search_engine=None, max_context_length: int = 4000):
        """
        初始化开放性文本答案提示模板
        
        Args:
            search_engine: 搜索引擎实例
            max_context_length: 最大上下文长度
        """
        super().__init__(search_engine)
        self.max_context_length = max_context_length
    
    def format_prompt(self, question: str, context: List[Dict[str, Any]]) -> str:
        """
        格式化开放性文本答案提示
        
        Args:
            question: 用户问题
            context: 检索到的上下文信息
            
        Returns:
            格式化后的提示文本
        """
        context_text = self._format_context(context)
        
        prompt = f"""你是一个专业的银行政策分析师，请基于以下银行政策文档内容，详细回答用户的问题。

文档内容：
{context_text}

用户问题：{question}

请基于上述文档内容，提供一个详细、准确、结构化的回答。回答应该包括：
1. 直接回答用户的问题
2. 提供相关的背景信息和数据支撑
3. 分析问题的关键要点
4. 如果适用，提供相关的政策建议或趋势分析

请确保回答：
- 基于文档内容，避免编造信息
- 语言专业但易懂
- 结构清晰，逻辑性强
- 如果文档中没有相关信息，请明确说明

回答："""
        
        return prompt
    
    def extract_answer(self, response: str) -> str:
        """
        提取开放性文本答案
        
        Args:
            response: 模型响应
            
        Returns:
            清理后的文本答案
        """
        # 清理响应文本
        cleaned_response = response.strip()
        
        # 移除可能的提示词残留
        if cleaned_response.startswith("回答："):
            cleaned_response = cleaned_response[3:].strip()
        
        return cleaned_response
    
    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """
        格式化上下文信息，控制长度
        
        Args:
            context: 上下文信息列表
            
        Returns:
            格式化后的上下文文本
        """
        formatted_context = []
        current_length = 0
        
        for i, ctx in enumerate(context, 1):
            if isinstance(ctx, dict):
                title = ctx.get('title', f'文档{i}')
                content = ctx.get('content', ctx.get('context', ''))
                
                # 截断过长的内容
                if len(content) > 1000:
                    content = content[:1000] + "..."
                
                context_item = f"{i}. {title}\n{content}\n"
                
                # 检查长度限制
                if current_length + len(context_item) > self.max_context_length:
                    break
                
                formatted_context.append(context_item)
                current_length += len(context_item)
            else:
                context_str = str(ctx)
                if len(context_str) > 1000:
                    context_str = context_str[:1000] + "..."
                
                if current_length + len(context_str) > self.max_context_length:
                    break
                
                formatted_context.append(f"{i}. {context_str}\n")
                current_length += len(context_str)
        
        return '\n'.join(formatted_context)
    
    def search_and_answer(self, question: str, limit: int = 5) -> Dict[str, Any]:
        """
        搜索并生成答案
        
        Args:
            question: 用户问题
            limit: 检索文档数量限制
            
        Returns:
            包含答案和元数据的字典
        """
        if not self.search_engine:
            return {
                "answer": "搜索引擎未初始化",
                "context": [],
                "error": "搜索引擎未初始化"
            }
        
        try:
            # 使用混合搜索获取相关文档
            search_results = self.search_engine.hybrid_search(question, limit)
            
            if not search_results:
                return {
                    "answer": "未找到相关文档信息",
                    "context": [],
                    "search_results": []
                }
            
            # 提取上下文信息
            context = []
            for result in search_results:
                context_item = {
                    "title": result.get("title", ""),
                    "content": result.get("context", []),
                    "score": result.get("hybrid_score", 0),
                    "document_id": result.get("document_id", "")
                }
                context.append(context_item)
            
            # 格式化提示
            prompt = self.format_prompt(question, context)
            
            return {
                "prompt": prompt,
                "context": context,
                "search_results": search_results,
                "question": question
            }
            
        except Exception as e:
            logger.error(f"搜索和答案生成失败: {e}")
            return {
                "answer": f"处理问题时发生错误: {str(e)}",
                "context": [],
                "error": str(e)
            }

def create_rag_prompt(prompt_type: str, search_engine=None, **kwargs) -> BaseRAGPrompt:
    """
    创建RAG提示模板实例
    
    Args:
        prompt_type: 提示模板类型
        search_engine: 搜索引擎实例
        **kwargs: 其他参数
        
    Returns:
        RAG提示模板实例
    """
    prompt_classes = {
        "number": AnswerWithRAGContextNumberPrompt,
        "boolean": AnswerWithRAGContextBooleanPrompt,
        "names": AnswerWithRAGContextNamesPrompt,
        "comparative": ComparativeAnswerPrompt,
        "string": AnswerWithRAGContextStringPrompt
    }
    
    if prompt_type not in prompt_classes:
        raise ValueError(f"不支持的提示模板类型: {prompt_type}")
    
    return prompt_classes[prompt_type](search_engine, **kwargs)

def main():
    """测试RAG提示模板"""
    print("=== 银行行业政策知识库RAG提示模板测试 ===")
    
    # 模拟上下文数据
    mock_context = [
        {
            "title": "中国普惠金融指标分析报告（2023-2024年）",
            "content": "普惠小微贷款余额达到29.4万亿元，同比增长23.5%。普惠小微授信户数6166万户，同比增长9.1%。",
            "score": 0.95
        },
        {
            "title": "中国经济金融展望报告（2025年）",
            "content": "预计2025年一季度GDP同比增长5.2%左右，二季度GDP同比增长5.3%左右。",
            "score": 0.88
        }
    ]
    
    # 测试各种提示模板
    test_question = "普惠小微贷款的余额是多少？"
    
    print(f"\n测试问题: {test_question}")
    print(f"模拟上下文: {len(mock_context)}个文档")
    
    # 测试数字答案提示
    number_prompt = AnswerWithRAGContextNumberPrompt()
    number_formatted = number_prompt.format_prompt(test_question, mock_context)
    print(f"\n数字答案提示模板:")
    print(f"长度: {len(number_formatted)}字符")
    print(f"预览: {number_formatted[:200]}...")
    
    # 测试布尔答案提示
    boolean_prompt = AnswerWithRAGContextBooleanPrompt()
    boolean_question = "普惠小微贷款是否增长？"
    boolean_formatted = boolean_prompt.format_prompt(boolean_question, mock_context)
    print(f"\n布尔答案提示模板:")
    print(f"长度: {len(boolean_formatted)}字符")
    print(f"预览: {boolean_formatted[:200]}...")
    
    # 测试开放性文本答案提示
    string_prompt = AnswerWithRAGContextStringPrompt()
    string_formatted = string_prompt.format_prompt(test_question, mock_context)
    print(f"\n开放性文本答案提示模板:")
    print(f"长度: {len(string_formatted)}字符")
    print(f"预览: {string_formatted[:200]}...")
    
    print(f"\n✅ RAG提示模板测试完成!")

if __name__ == "__main__":
    main()
