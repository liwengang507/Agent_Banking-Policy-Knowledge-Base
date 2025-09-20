#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库简化混合搜索引擎
结合BM25和TF-IDF算法的混合搜索
"""

import json
import re
import math
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from collections import defaultdict, Counter

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleHybridSearchEngine:
    """简化混合搜索引擎 - 结合BM25和TF-IDF"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.index_path = self.base_path / "index"
        self.data_path = self.base_path / "data"
        
        # 加载索引文件
        self.document_index = self._load_index("document_index.json")
        self.topic_index = self._load_index("topic_index.json")
        self.keyword_index = self._load_index("keyword_index.json")
        
        # 初始化搜索相关变量
        self.documents = []
        self.document_contents = {}
        self.avg_doc_length = 0
        self.total_docs = 0
        self.doc_freq = defaultdict(int)
        self.term_freq = defaultdict(lambda: defaultdict(int))
        
        # 构建索引
        self._build_indices()
        
        logger.info("简化混合搜索引擎初始化完成")
    
    def _load_index(self, filename: str) -> Dict[str, Any]:
        """加载索引文件"""
        try:
            index_file = self.index_path / filename
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载索引文件 {filename} 失败: {e}")
            return {}
    
    def _build_indices(self):
        """构建搜索索引"""
        logger.info("开始构建搜索索引...")
        
        for doc in self.document_index.get("documents", []):
            content = self._get_document_content(doc["id"])
            if content:
                self.documents.append(doc)
                self.document_contents[doc["id"]] = content
                
                words = self._tokenize_text(content)
                doc_length = len(words)
                
                word_freq = Counter(words)
                for word, freq in word_freq.items():
                    self.term_freq[doc["id"]][word] = freq
                    self.doc_freq[word] += 1
                
                self.avg_doc_length += doc_length
        
        self.total_docs = len(self.documents)
        if self.total_docs > 0:
            self.avg_doc_length /= self.total_docs
        
        logger.info(f"索引构建完成: {self.total_docs}个文档, {len(self.doc_freq)}个词项")
    
    def _tokenize_text(self, text: str) -> List[str]:
        """文本分词"""
        # 简单的中文分词
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+|\d+', text)
        filtered_words = []
        for word in words:
            if len(word) > 1:
                filtered_words.append(word)
        return filtered_words
    
    def _get_document_content(self, document_id: str) -> Optional[str]:
        """获取文档内容"""
        doc = None
        for d in self.document_index.get("documents", []):
            if d["id"] == document_id:
                doc = d
                break
        
        if not doc:
            return None
        
        try:
            file_path = self.base_path / doc["file_path"]
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"读取文档内容失败: {e}")
            return None
    
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
    
    def hybrid_search(self, query: str, limit: int = 10, 
                     bm25_weight: float = 0.6, tfidf_weight: float = 0.4) -> List[Dict[str, Any]]:
        """混合搜索"""
        results = []
        
        for doc in self.documents:
            doc_id = doc["id"]
            
            bm25_score = self._calculate_bm25_score(query, doc_id)
            tfidf_score = self._calculate_tfidf_score(query, doc_id)
            
            # 归一化分数
            bm25_score_norm = bm25_score / max(bm25_score, 1e-6)
            tfidf_score_norm = tfidf_score / max(tfidf_score, 1e-6)
            
            hybrid_score = bm25_weight * bm25_score_norm + tfidf_weight * tfidf_score_norm
            
            if hybrid_score > 0:
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
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """获取搜索统计信息"""
        return {
            "total_documents": self.total_docs,
            "total_terms": len(self.doc_freq),
            "avg_document_length": self.avg_doc_length,
            "index_size_mb": sum(len(content.encode('utf-8')) for content in self.document_contents.values()) / (1024 * 1024),
            "popular_terms": sorted(self.doc_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        }

def main():
    """测试简化混合搜索引擎"""
    print("=== 银行行业政策知识库混合搜索引擎 ===")
    
    try:
        search_engine = SimpleHybridSearchEngine(".")
        
        stats = search_engine.get_search_statistics()
        print(f"\n📊 统计信息:")
        print(f"   文档总数: {stats['total_documents']}")
        print(f"   词项总数: {stats['total_terms']}")
        print(f"   平均文档长度: {stats['avg_document_length']:.1f}词")
        print(f"   索引大小: {stats['index_size_mb']:.2f}MB")
        
        print(f"\n🔥 热门词项:")
        for term, freq in stats['popular_terms']:
            print(f"   {term}: {freq}次")
        
        print(f"\n🔍 混合搜索测试:")
        results = search_engine.hybrid_search("普惠金融", 3)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   混合分数: {result['hybrid_score']:.4f}")
            print(f"   BM25分数: {result['bm25_score']:.4f}")
            print(f"   TF-IDF分数: {result['tfidf_score']:.4f}")
            print(f"   上下文数量: {len(result['context'])}")
        
        print(f"\n📚 主题混合搜索测试:")
        results = search_engine.search_by_topic_hybrid("普惠金融", 2)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']} (主题: {result['topic']})")
            print(f"   混合分数: {result['hybrid_score']:.4f}")
        
        print(f"\n✅ 混合搜索引擎测试完成!")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        logger.error(f"混合搜索引擎测试失败: {e}")

if __name__ == "__main__":
    main() 