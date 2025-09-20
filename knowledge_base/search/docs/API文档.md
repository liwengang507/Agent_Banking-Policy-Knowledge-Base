# API 文档

## 概述

银行政策知识库RAG系统提供RESTful API接口，支持智能问答、文档检索、推理过程查询等功能。

## 基础信息

- **Base URL**: `http://localhost:8501`
- **Content-Type**: `application/json`
- **字符编码**: UTF-8

## 认证

当前版本无需认证，后续版本将支持API Key认证。

## 核心接口

### 1. 智能问答接口

#### 发送问题
```http
POST /api/question
Content-Type: application/json

{
    "question": "普惠金融的发展现状如何？",
    "question_type": "policy",
    "max_steps": 5
}
```

#### 响应示例
```json
{
    "status": "success",
    "data": {
        "question": "普惠金融的发展现状如何？",
        "answer": "基于银行政策文档分析，普惠金融发展态势良好...",
        "confidence": 0.92,
        "reasoning_steps": [
            {
                "step": 1,
                "action": "问题分析",
                "result": "识别为政策咨询类问题",
                "confidence": 0.95
            },
            {
                "step": 2,
                "action": "文档检索",
                "result": "找到3个相关文档片段",
                "confidence": 0.88
            }
        ],
        "references": [
            "普惠金融指标分析报告2023",
            "经济金融展望报告2024"
        ],
        "processing_time": 2.3
    }
}
```

### 2. 推理过程查询接口

#### 获取推理步骤
```http
GET /api/reasoning/{question_id}
```

#### 响应示例
```json
{
    "status": "success",
    "data": {
        "question_id": "q_123456",
        "reasoning_chain": [
            {
                "step": 1,
                "timestamp": "2024-01-01T10:00:00Z",
                "action": "问题分析",
                "input": "普惠金融的发展现状如何？",
                "output": "识别为政策咨询类问题",
                "confidence": 0.95
            }
        ],
        "total_steps": 5,
        "quality_score": 0.92
    }
}
```

### 3. 文档检索接口

#### 搜索文档
```http
POST /api/search
Content-Type: application/json

{
    "query": "普惠金融",
    "limit": 10,
    "filters": {
        "document_type": "policy",
        "date_range": "2023-2024"
    }
}
```

#### 响应示例
```json
{
    "status": "success",
    "data": {
        "results": [
            {
                "document_id": "doc_001",
                "title": "普惠金融指标分析报告2023",
                "content": "普惠金融发展态势良好...",
                "relevance_score": 0.95,
                "metadata": {
                    "author": "中国人民银行",
                    "date": "2023-12-01",
                    "type": "policy"
                }
            }
        ],
        "total_count": 15,
        "search_time": 0.5
    }
}
```

## 错误处理

### 错误响应格式
```json
{
    "status": "error",
    "error": {
        "code": "INVALID_QUESTION",
        "message": "问题格式不正确",
        "details": "问题不能为空"
    }
}
```

### 常见错误码

| 错误码 | HTTP状态码 | 描述 |
|--------|------------|------|
| INVALID_QUESTION | 400 | 问题格式不正确 |
| QUESTION_TOO_LONG | 400 | 问题长度超过限制 |
| SYSTEM_BUSY | 503 | 系统繁忙 |
| INTERNAL_ERROR | 500 | 内部服务器错误 |

## 使用示例

### Python 客户端示例

```python
import requests
import json

class RAGClient:
    def __init__(self, base_url="http://localhost:8501"):
        self.base_url = base_url
    
    def ask_question(self, question, question_type="general"):
        """发送问题"""
        url = f"{self.base_url}/api/question"
        data = {
            "question": question,
            "question_type": question_type
        }
        
        response = requests.post(url, json=data)
        return response.json()
    
    def search_documents(self, query, limit=10):
        """搜索文档"""
        url = f"{self.base_url}/api/search"
        data = {
            "query": query,
            "limit": limit
        }
        
        response = requests.post(url, json=data)
        return response.json()

# 使用示例
client = RAGClient()

# 发送问题
result = client.ask_question("普惠金融的发展现状如何？")
print(result['data']['answer'])

# 搜索文档
docs = client.search_documents("风险管理")
print(f"找到 {len(docs['data']['results'])} 个相关文档")
```

### JavaScript 客户端示例

```javascript
class RAGClient {
    constructor(baseUrl = 'http://localhost:8501') {
        this.baseUrl = baseUrl;
    }
    
    async askQuestion(question, questionType = 'general') {
        const response = await fetch(`${this.baseUrl}/api/question`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                question_type: questionType
            })
        });
        
        return await response.json();
    }
    
    async searchDocuments(query, limit = 10) {
        const response = await fetch(`${this.baseUrl}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                limit: limit
            })
        });
        
        return await response.json();
    }
}

// 使用示例
const client = new RAGClient();

// 发送问题
client.askQuestion('普惠金融的发展现状如何？')
    .then(result => {
        console.log(result.data.answer);
    })
    .catch(error => {
        console.error('Error:', error);
    });
```

## 性能指标

### 响应时间
- **简单问题**: < 2秒
- **复杂问题**: < 5秒
- **文档检索**: < 1秒

### 并发处理
- **最大并发数**: 100
- **请求频率限制**: 100次/分钟
- **超时设置**: 30秒

## 版本信息

### 当前版本: v1.0.0
- 支持基础问答功能
- 支持推理过程查询
- 支持文档检索

### 计划功能
- v1.1.0: 支持批量问答
- v1.2.0: 支持实时流式响应
- v1.3.0: 支持多语言问答
