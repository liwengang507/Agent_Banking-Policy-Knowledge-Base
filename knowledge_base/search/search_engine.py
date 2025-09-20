#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库搜索引擎
支持关键词搜索、主题搜索和文档搜索
"""

import json
import os
import re
import math
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from collections import defaultdict, Counter

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeBaseSearchEngine:
    """知识库搜索引擎"""
    
    def __init__(self, base_path: str = "."):
        """
        初始化搜索引擎
        
        Args:
            base_path: 知识库根目录路径
        """
        self.base_path = Path(base_path)
        self.index_path = self.base_path / "index"
        self.data_path = self.base_path / "data"
        
        # 加载索引文件
        self.document_index = self._load_index("document_index.json")
        self.topic_index = self._load_index("topic_index.json")
        self.keyword_index = self._load_index("keyword_index.json")
        
        # 初始化混合搜索相关变量
        self.documents = []
        self.document_contents = {}
        self.avg_doc_length = 0
        self.total_docs = 0
        self.doc_freq = defaultdict(int)
        self.term_freq = defaultdict(lambda: defaultdict(int))
        
        # 构建混合搜索索引
        self._build_hybrid_index()
        
        logger.info("知识库搜索引擎初始化完成")
    
    def _load_index(self, filename: str) -> Dict[str, Any]:
        """加载索引文件"""
        try:
            index_file = self.index_path / filename
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载索引文件 {filename} 失败: {e}")
            return {}
    
    def _build_hybrid_index(self):
        """构建混合搜索索引"""
        logger.info("开始构建混合搜索索引...")
        
        for doc in self.document_index.get("documents", []):
            content = self._get_document_content_for_hybrid(doc["id"])
            if content:
                self.documents.append(doc)
                self.document_contents[doc["id"]] = content
                
                # 分词处理
                words = self._tokenize_text(content)
                doc_length = len(words)
                
                # 更新词项频率和文档频率
                word_freq = Counter(words)
                for word, freq in word_freq.items():
                    self.term_freq[doc["id"]][word] = freq
                    self.doc_freq[word] += 1
                
                # 计算平均文档长度
                self.avg_doc_length += doc_length
        
        self.total_docs = len(self.documents)
        if self.total_docs > 0:
            self.avg_doc_length /= self.total_docs
        
        logger.info(f"混合搜索索引构建完成: {self.total_docs}个文档, {len(self.doc_freq)}个词项")
    
    def _get_document_content_for_hybrid(self, document_id: str) -> Optional[str]:
        """获取文档内容（用于混合搜索）"""
        doc = None
        for d in self.document_index.get("documents", []):
            if d["id"] == document_id:
                doc = d
                break
        
        if not doc:
            return None
        
        try:
            # 修正路径，使用相对于知识库根目录的路径
            file_path = self.base_path / doc["file_path"].replace("../", "")
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"读取文档内容失败: {e}")
            return None
    
    def _tokenize_text(self, text: str) -> List[str]:
        """文本分词"""
        # 简单的中文分词
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+|\d+', text)
        filtered_words = []
        for word in words:
            if len(word) > 1:
                filtered_words.append(word)
        return filtered_words
    
    def _calculate_bm25_score(self, query: str, doc_id: str, k1: float = 1.2, b: float = 0.75) -> float:
        """计算BM25分数"""
        query_words = self._tokenize_text(query)
        doc_words = self._tokenize_text(self.document_contents.get(doc_id, ""))
        doc_length = len(doc_words)
        
        score = 0.0
        
        for word in query_words:
            if word in self.term_freq[doc_id]:
                if self.doc_freq[word] > 0:
                    idf = math.log((self.total_docs - self.doc_freq[word] + 0.5) / 
                                 (self.doc_freq[word] + 0.5))
                else:
                    idf = 0
                
                tf = self.term_freq[doc_id][word]
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * (doc_length / self.avg_doc_length))
                
                score += idf * (numerator / denominator)
        
        return score
    
    def _calculate_tfidf_score(self, query: str, doc_id: str) -> float:
        """计算TF-IDF分数"""
        query_words = self._tokenize_text(query)
        doc_words = self._tokenize_text(self.document_contents.get(doc_id, ""))
        
        score = 0.0
        
        for word in query_words:
            if word in self.term_freq[doc_id]:
                # 计算TF
                tf = self.term_freq[doc_id][word] / len(doc_words)
                
                # 计算IDF
                if self.doc_freq[word] > 0:
                    idf = math.log(self.total_docs / self.doc_freq[word])
                else:
                    idf = 0
                
                score += tf * idf
        
        return score
    
    def search_by_keyword(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        按关键词搜索
        
        Args:
            keyword: 搜索关键词
            limit: 返回结果数量限制
            
        Returns:
            搜索结果列表
        """
        results = []
        
        # 在关键词索引中搜索
        if keyword in self.keyword_index.get("keywords", {}):
            keyword_data = self.keyword_index["keywords"][keyword]
            for doc in keyword_data.get("documents", []):
                result = {
                    "type": "keyword_match",
                    "keyword": keyword,
                    "document_id": doc["id"],
                    "title": doc["title"],
                    "occurrences": doc["occurrences"],
                    "contexts": doc.get("contexts", []),
                    "relevance_score": doc.get("occurrences", 0) / keyword_data.get("frequency", 1)
                }
                results.append(result)
        
        # 在文档内容中搜索
        for doc in self.document_index.get("documents", []):
            if keyword.lower() in doc.get("title", "").lower():
                result = {
                    "type": "title_match",
                    "keyword": keyword,
                    "document_id": doc["id"],
                    "title": doc["title"],
                    "summary": doc.get("summary", ""),
                    "relevance_score": 0.8
                }
                results.append(result)
        
        # 按相关性排序并限制结果数量
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return results[:limit]
    
    def search_by_topic(self, topic: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        按主题搜索
        
        Args:
            topic: 搜索主题
            limit: 返回结果数量限制
            
        Returns:
            搜索结果列表
        """
        results = []
        
        topics = self.topic_index.get("topics", {})
        if topic in topics:
            topic_data = topics[topic]
            for doc in topic_data.get("documents", []):
                result = {
                    "type": "topic_match",
                    "topic": topic,
                    "document_id": doc["id"],
                    "title": doc["title"],
                    "relevance": doc.get("relevance", 0),
                    "key_sections": doc.get("key_sections", []),
                    "description": topic_data.get("description", "")
                }
                results.append(result)
        
        # 按相关性排序并限制结果数量
        results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        return results[:limit]
    
    def search_by_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        按文档ID搜索
        
        Args:
            document_id: 文档ID
            
        Returns:
            文档信息
        """
        for doc in self.document_index.get("documents", []):
            if doc["id"] == document_id:
                return doc
        return None
    
    def get_document_content(self, document_id: str) -> Optional[str]:
        """
        获取文档内容
        
        Args:
            document_id: 文档ID
            
        Returns:
            文档内容
        """
        doc = self.search_by_document(document_id)
        if not doc:
            return None
        
        try:
            file_path = self.base_path / doc["file_path"]
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"读取文档内容失败: {e}")
            return None
    
    def hybrid_search(self, query: str, limit: int = 10, 
                     bm25_weight: float = 0.6, tfidf_weight: float = 0.4) -> List[Dict[str, Any]]:
        """
        混合搜索 - 结合BM25和TF-IDF算法
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制
            bm25_weight: BM25权重
            tfidf_weight: TF-IDF权重
            
        Returns:
            搜索结果列表
        """
        results = []
        
        for doc in self.documents:
            doc_id = doc["id"]
            
            # 计算BM25和TF-IDF分数
            bm25_score = self._calculate_bm25_score(query, doc_id)
            tfidf_score = self._calculate_tfidf_score(query, doc_id)
            
            # 归一化分数
            bm25_score_norm = bm25_score / max(bm25_score, 1e-6)
            tfidf_score_norm = tfidf_score / max(tfidf_score, 1e-6)
            
            # 计算混合分数
            hybrid_score = bm25_weight * bm25_score_norm + tfidf_weight * tfidf_score_norm
            
            if hybrid_score > 0:
                # 提取上下文
                context = self._extract_context(query, doc_id)
                
                result = {
                    "type": "hybrid_search",
                    "query": query,
                    "document_id": doc_id,
                    "title": doc["title"],
                    "author": doc.get("author", ""),
                    "publish_date": doc.get("publish_date", ""),
                    "hybrid_score": hybrid_score,
                    "bm25_score": bm25_score,
                    "tfidf_score": tfidf_score,
                    "context": context,
                    "summary": doc.get("summary", ""),
                    "keywords": doc.get("keywords", [])
                }
                results.append(result)
        
        # 按混合分数排序
        results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return results[:limit]
    
    def _extract_context(self, query: str, doc_id: str) -> List[Dict[str, Any]]:
        """提取查询相关的上下文"""
        content = self.document_contents.get(doc_id, "")
        if not content:
            return []
        
        contexts = []
        query_words = self._tokenize_text(query)
        paragraphs = content.split('\n')
        
        for i, para in enumerate(paragraphs):
            para_words = self._tokenize_text(para)
            
            if any(word in para_words for word in query_words):
                start = max(0, i - 1)
                end = min(len(paragraphs), i + 2)
                context_paras = paragraphs[start:end]
                
                context = {
                    "paragraph_index": i,
                    "content": para.strip(),
                    "context": '\n'.join(context_paras).strip(),
                    "relevance": sum(1 for word in query_words if word in para_words) / len(query_words)
                }
                contexts.append(context)
        
        contexts.sort(key=lambda x: x["relevance"], reverse=True)
        return contexts[:3]
    
    def search_by_keyword_hybrid(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """基于关键词的混合搜索"""
        return self.hybrid_search(keyword, limit)
    
    def search_by_topic_hybrid(self, topic: str, limit: int = 10) -> List[Dict[str, Any]]:
        """基于主题的混合搜索"""
        topic_keywords = []
        topics = self.topic_index.get("topics", {})
        if topic in topics:
            topic_data = topics[topic]
            for subtopic, data in topic_data.get("subtopics", {}).items():
                topic_keywords.extend(data.get("key_terms", []))
        
        if not topic_keywords:
            topic_keywords = [topic]
        
        query = " ".join(topic_keywords)
        results = self.hybrid_search(query, limit)
        
        for result in results:
            result["topic"] = topic
            result["topic_keywords"] = topic_keywords
        
        return results
    
    def search_content(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        在文档内容中搜索
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制
            
        Returns:
            搜索结果列表
        """
        results = []
        
        for doc in self.document_index.get("documents", []):
            content = self.get_document_content(doc["id"])
            if content and query.lower() in content.lower():
                # 找到匹配的段落
                paragraphs = content.split('\n')
                matches = []
                
                for i, para in enumerate(paragraphs):
                    if query.lower() in para.lower():
                        matches.append({
                            "paragraph": i + 1,
                            "content": para.strip(),
                            "context": paragraphs[max(0, i-1):min(len(paragraphs), i+2)]
                        })
                
                if matches:
                    result = {
                        "type": "content_match",
                        "query": query,
                        "document_id": doc["id"],
                        "title": doc["title"],
                        "matches": matches,
                        "relevance_score": len(matches) / doc.get("line_count", 1)
                    }
                    results.append(result)
        
        # 按相关性排序并限制结果数量
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return results[:limit]
    
    def get_related_keywords(self, keyword: str) -> List[str]:
        """
        获取相关关键词
        
        Args:
            keyword: 关键词
            
        Returns:
            相关关键词列表
        """
        if keyword in self.keyword_index.get("keywords", {}):
            return self.keyword_index["keywords"][keyword].get("related_keywords", [])
        return []
    
    def get_popular_keywords(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取热门关键词
        
        Args:
            limit: 返回结果数量限制
            
        Returns:
            热门关键词列表
        """
        keywords = []
        for keyword, data in self.keyword_index.get("keywords", {}).items():
            keywords.append({
                "keyword": keyword,
                "frequency": data.get("frequency", 0),
                "documents": len(data.get("documents", []))
            })
        
        # 按频率排序
        keywords.sort(key=lambda x: x["frequency"], reverse=True)
        return keywords[:limit]
    
    def get_topic_summary(self, topic: str) -> Optional[Dict[str, Any]]:
        """
        获取主题摘要
        
        Args:
            topic: 主题名称
            
        Returns:
            主题摘要信息
        """
        topics = self.topic_index.get("topics", {})
        if topic in topics:
            topic_data = topics[topic]
            return {
                "topic": topic,
                "description": topic_data.get("description", ""),
                "document_count": len(topic_data.get("documents", [])),
                "subtopics": list(topic_data.get("subtopics", {}).keys()),
                "documents": topic_data.get("documents", [])
            }
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取知识库统计信息
        
        Returns:
            统计信息
        """
        return {
            "total_documents": self.document_index.get("metadata", {}).get("total_documents", 0),
            "total_characters": self.document_index.get("metadata", {}).get("total_characters", 0),
            "total_keywords": self.keyword_index.get("metadata", {}).get("total_keywords", 0),
            "total_topics": self.topic_index.get("metadata", {}).get("total_topics", 0),
            "popular_keywords": self.get_popular_keywords(5)
        }

def main():
    """测试搜索引擎"""
    # 初始化搜索引擎
    search_engine = KnowledgeBaseSearchEngine(".")
    
    # 获取统计信息
    stats = search_engine.get_statistics()
    print("=== 知识库统计信息 ===")
    print(f"文档总数: {stats['total_documents']}")
    print(f"字符总数: {stats['total_characters']:,}")
    print(f"关键词总数: {stats['total_keywords']}")
    print(f"主题总数: {stats['total_topics']}")
    
    print("\n=== 热门关键词 ===")
    for kw in stats['popular_keywords']:
        print(f"{kw['keyword']}: {kw['frequency']}次")
    
    # 测试关键词搜索
    print("\n=== 关键词搜索测试 ===")
    results = search_engine.search_by_keyword("普惠金融", 3)
    for result in results:
        print(f"- {result['title']} (相关性: {result['relevance_score']:.2f})")
    
    # 测试主题搜索
    print("\n=== 主题搜索测试 ===")
    results = search_engine.search_by_topic("普惠金融", 3)
    for result in results:
        print(f"- {result['title']} (相关性: {result['relevance']:.2f})")
    
    # 测试混合搜索
    print("\n=== 混合搜索测试 ===")
    results = search_engine.hybrid_search("普惠金融", 3)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   混合分数: {result['hybrid_score']:.4f}")
        print(f"   BM25分数: {result['bm25_score']:.4f}")
        print(f"   TF-IDF分数: {result['tfidf_score']:.4f}")
        print(f"   上下文数量: {len(result['context'])}")
    
    # 测试主题混合搜索
    print("\n=== 主题混合搜索测试 ===")
    results = search_engine.search_by_topic_hybrid("普惠金融", 2)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']} (主题: {result['topic']})")
        print(f"   混合分数: {result['hybrid_score']:.4f}")
    
    print("\n✅ 混合搜索功能测试完成!")

if __name__ == "__main__":
    main() 