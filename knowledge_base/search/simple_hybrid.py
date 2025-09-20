#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的混合搜索实现
结合BM25和TF-IDF算法
"""

import json
import re
import math
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict, Counter

class SimpleHybridSearch:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.index_path = self.base_path / "index"
        
        # 加载索引
        self.document_index = self._load_json("document_index.json")
        self.topic_index = self._load_json("topic_index.json")
        self.keyword_index = self._load_json("keyword_index.json")
        
        # 构建搜索索引
        self.documents = []
        self.document_contents = {}
        self.term_freq = defaultdict(lambda: defaultdict(int))
        self.doc_freq = defaultdict(int)
        self.avg_doc_length = 0
        self.total_docs = 0
        
        self._build_index()
    
    def _load_json(self, filename: str) -> Dict:
        try:
            with open(self.index_path / filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载 {filename} 失败: {e}")
            return {}
    
    def _build_index(self):
        print("构建搜索索引...")
        
        for doc in self.document_index.get("documents", []):
            content = self._get_document_content(doc["id"])
            if content:
                self.documents.append(doc)
                self.document_contents[doc["id"]] = content
                
                # 分词
                words = self._tokenize(content)
                doc_length = len(words)
                
                # 统计词频
                word_freq = Counter(words)
                for word, freq in word_freq.items():
                    self.term_freq[doc["id"]][word] = freq
                    self.doc_freq[word] += 1
                
                self.avg_doc_length += doc_length
        
        self.total_docs = len(self.documents)
        if self.total_docs > 0:
            self.avg_doc_length /= self.total_docs
        
        print(f"索引构建完成: {self.total_docs}个文档")
    
    def _get_document_content(self, doc_id: str) -> str:
        for doc in self.document_index.get("documents", []):
            if doc["id"] == doc_id:
                try:
                    file_path = self.base_path / doc["file_path"]
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    print(f"读取文档失败: {e}")
                    return ""
        return ""
    
    def _tokenize(self, text: str) -> List[str]:
        # 简单中文分词
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+|\d+', text)
        return [w for w in words if len(w) > 1]
    
    def _bm25_score(self, query: str, doc_id: str) -> float:
        query_words = self._tokenize(query)
        doc_words = self._tokenize(self.document_contents.get(doc_id, ""))
        doc_length = len(doc_words)
        
        score = 0.0
        k1, b = 1.2, 0.75
        
        for word in query_words:
            if word in self.term_freq[doc_id]:
                # IDF
                if self.doc_freq[word] > 0:
                    idf = math.log((self.total_docs - self.doc_freq[word] + 0.5) / 
                                 (self.doc_freq[word] + 0.5))
                else:
                    idf = 0
                
                # TF
                tf = self.term_freq[doc_id][word]
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * (doc_length / self.avg_doc_length))
                
                score += idf * (numerator / denominator)
        
        return score
    
    def _tfidf_score(self, query: str, doc_id: str) -> float:
        query_words = self._tokenize(query)
        doc_words = self._tokenize(self.document_contents.get(doc_id, ""))
        
        score = 0.0
        
        for word in query_words:
            if word in self.term_freq[doc_id]:
                # TF
                tf = self.term_freq[doc_id][word] / len(doc_words)
                
                # IDF
                if self.doc_freq[word] > 0:
                    idf = math.log(self.total_docs / self.doc_freq[word])
                else:
                    idf = 0
                
                score += tf * idf
        
        return score
    
    def hybrid_search(self, query: str, limit: int = 10) -> List[Dict]:
        results = []
        
        for doc in self.documents:
            doc_id = doc["id"]
            
            # 计算BM25和TF-IDF分数
            bm25_score = self._bm25_score(query, doc_id)
            tfidf_score = self._tfidf_score(query, doc_id)
            
            # 归一化
            bm25_norm = bm25_score / max(bm25_score, 1e-6)
            tfidf_norm = tfidf_score / max(tfidf_score, 1e-6)
            
            # 混合分数 (BM25权重0.6, TF-IDF权重0.4)
            hybrid_score = 0.6 * bm25_norm + 0.4 * tfidf_norm
            
            if hybrid_score > 0:
                result = {
                    "title": doc["title"],
                    "doc_id": doc_id,
                    "hybrid_score": hybrid_score,
                    "bm25_score": bm25_score,
                    "tfidf_score": tfidf_score,
                    "summary": doc.get("summary", "")
                }
                results.append(result)
        
        # 按混合分数排序
        results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return results[:limit]
    
    def search_by_topic(self, topic: str, limit: int = 10) -> List[Dict]:
        # 获取主题相关关键词
        topic_keywords = []
        topics = self.topic_index.get("topics", {})
        if topic in topics:
            topic_data = topics[topic]
            for subtopic, data in topic_data.get("subtopics", {}).items():
                topic_keywords.extend(data.get("key_terms", []))
        
        if not topic_keywords:
            topic_keywords = [topic]
        
        query = " ".join(topic_keywords)
        return self.hybrid_search(query, limit)

def main():
    print("=== 银行行业政策知识库混合搜索 ===")
    
    try:
        search = SimpleHybridSearch(".")
        
        print(f"\n📊 索引统计:")
        print(f"   文档数量: {search.total_docs}")
        print(f"   词项数量: {len(search.doc_freq)}")
        print(f"   平均文档长度: {search.avg_doc_length:.1f}词")
        
        print(f"\n🔍 混合搜索测试 - '普惠金融':")
        results = search.hybrid_search("普惠金融", 3)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   混合分数: {result['hybrid_score']:.4f}")
            print(f"   BM25分数: {result['bm25_score']:.4f}")
            print(f"   TF-IDF分数: {result['tfidf_score']:.4f}")
        
        print(f"\n📚 主题搜索测试 - '普惠金融':")
        results = search.search_by_topic("普惠金融", 2)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   混合分数: {result['hybrid_score']:.4f}")
        
        print(f"\n✅ 混合搜索测试完成!")
        
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main() 