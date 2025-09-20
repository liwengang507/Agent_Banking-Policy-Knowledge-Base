# 智能银行政策知识库RAG系统

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![RAG](https://img.shields.io/badge/RAG-Enhanced-orange.svg)](#)
[![Long-term%20Thinking](https://img.shields.io/badge/Long--term%20Thinking-Enabled-purple.svg)](#)
[![Knowledge%20Graph](https://img.shields.io/badge/Knowledge%20Graph-GraphRAG-blue.svg)](#)
[![Multi--Agent](https://img.shields.io/badge/Multi--Agent-Collaboration-purple.svg)](#)

## 📖 项目简介

这是一个基于长效思考机制的智能银行政策知识库RAG系统，采用先进的ReAct推理架构和GraphRAG知识图谱技术。系统集成了深度推理引擎和智能检索算法，形成多层次智能问答体系。通过长效思考过程和完整推理步骤展示，实现复杂政策问题的深度分析和精准回答。具备智能复杂度识别、动态推理策略选择、知识图谱检索和多模态推理能力，为银行政策咨询提供前所未有的智能化知识管理和问答服务。

## 🎯 核心特色

### 🤖 长效思考机制
**基于ReAct推理框架的深度思考过程**
- 展示完整的AI推理步骤和思考过程
- 支持多层次的逻辑推理和验证
- 提供可解释的推理链路和置信度评估

### 🧠 智能问答系统
**多类型专业问答能力**
- 政策咨询：银行政策解读和咨询
- 数据分析：金融指标查询和趋势分析
- 比较分析：不同时期、不同机构的对比分析
- 风险评估：金融风险识别和评估

### 🕸️ GraphRAG知识图谱
**基于实体关系的深度知识检索**
- 自动构建银行政策知识图谱
- 支持实体关系推理和关联分析
- 实现多文档独立图谱管理

### 🔍 混合检索算法
**BM25 + TF-IDF + 语义检索**
- 结合关键词匹配和语义相似度
- 支持多模态信息检索
- 提供精准的文档片段定位

### 📊 实时推理展示
**动态思考过程可视化**
- 实时显示推理进度和步骤
- 支持推理质量评估和优化
- 提供完整的思考链路追踪

### 🛡️ 智能保护机制
**多层次系统保护**
- 智能熔断和限流保护
- 资源使用监控和优化
- 异常处理和自动恢复

### 🚀 高性能架构
**可扩展的微服务架构**
- 支持高并发访问
- 模块化设计便于扩展
- 容器化部署支持

### 🔧 易于部署
**一键启动和配置**
- 自动化依赖安装
- 智能环境检测
- 跨平台部署支持

🌟 技术优势：

✅ 基于LangGraph的多Agent协同架构，支持复杂任务分解和并行处理

✅ Agent-as-Tool设计模式，实现专业能力的模块化和可复用性

✅ GraphRAG知识图谱技术，提供深度语义理解和关联推理能力

✅ 多图谱架构，支持多文档独立管理和精细化检索

✅ 智能复杂度判断，自动选择最优Agent协作策略

✅ 透明协作过程，提供完整的Agent交互链和决策依据

✅ 企业级稳定性，多层次熔断保护和异常恢复机制

✅ 高度可扩展，支持自定义Agent和工具集成

 🚀 示例截图:

<img width="1107" height="475" alt="image" src="https://github.com/user-attachments/assets/70a4449b-d0b6-4961-a8cb-f8e5ae95d661" />
<img width="1106" height="699" alt="image" src="https://github.com/user-attachments/assets/6d8316da-89cf-4adc-8cd5-2b6d68e2c6ae" />
<img width="1107" height="800" alt="image" src="https://github.com/user-attachments/assets/104200ac-58ed-4cdf-bdb5-1601ff8ba693" />



## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    用户界面层                               │
├─────────────────────────────────────────────────────────────┤
│  Streamlit Web界面  │  长效思考展示  │  进度可视化  │  交互控制  │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    业务逻辑层                               │
├─────────────────────────────────────────────────────────────┤
│  RAG处理管道  │  推理引擎  │  检索系统  │  答案生成  │  质量评估  │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    数据存储层                               │
├─────────────────────────────────────────────────────────────┤
│  知识库文档  │  索引文件  │  配置文件  │  缓存数据  │  日志文件  │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 环境要求
- Python 3.7+
- 4GB+ RAM
- 2GB+ 存储空间

### 一键启动
```bash
# 克隆项目
git clone https://github.com/your-username/bank-policy-rag-system.git
cd bank-policy-rag-system

# 启动系统
python 启动RAG.py
```

### 访问系统
打开浏览器访问：http://localhost:8501

## 💡 使用示例

### 政策咨询
**问题**: "普惠金融的发展现状如何？"
**系统响应**: 展示完整的思考过程，包括问题分析、文档检索、信息提取、逻辑推理等步骤，最终提供基于政策文档的专业分析。

### 数据分析
**问题**: "普惠小微贷款的余额是多少？"
**系统响应**: 通过长效思考机制，检索相关数据，进行趋势分析，提供准确的数值和变化趋势。

### 比较分析
**问题**: "比较不同时期的普惠金融发展情况"
**系统响应**: 运用多步骤推理，进行多维度对比分析，提供结构化的比较结果。

## 🛠️ 技术栈

### 核心技术
编程语言	  Python 3.7+
Web框架	 	Streamlit
AI/ML技术	RAG, ReAct, GraphRAG, BM25, TF-IDF等
数据处理	 	NumPy, Pandas, scikit-learn, jieba
文档处理	 	PyPDF2, python-docx
部署技术	 	Docker, GitHub Actions, Nginx等
开发工具	 	Git, pytest, flake8, black等
架构模式	 	微服务、分层、RAG管道、Agent

### 依赖包
```
streamlit>=1.28.0
numpy>=1.21.0

Web框架：
streamlit>=1.28.0 - 主要的Web界面框架

数据处理：
numpy>=1.21.0 - 数值计算库
pandas>=1.3.0 - 数据分析库

机器学习和文本处理：

scikit-learn>=1.0.0 - 机器学习库
jieba>=0.42.1 - 中文分词工具

文档处理：
PyPDF2>=3.0.0 - PDF文档处理
python-docx>=0.8.11 - Word文档处理
pandas>=1.3.0
scikit-learn>=1.0.0
jieba>=0.42.1
```

## 📁 项目结构

```
bank-policy-rag-system/
├── README.md                    # 项目说明文档
├── 启动RAG.py                  # 系统启动脚本
├── 长效思考RAG.py              # 主应用程序
├── docs/                       # 文档目录
│   ├── 系统架构.md
│   ├── API文档.md
│   └── 部署指南.md
├── requirements.txt            # 依赖包列表
├── LICENSE                     # MIT许可证
└── .gitignore                  # Git忽略文件
```

## 🔧 配置说明

### 基础配置
- **端口**: 8501 (可在启动脚本中修改)
- **知识库路径**: 当前目录
- **缓存设置**: 自动管理

### 高级配置
- **推理深度**: 可配置推理步骤数量
- **检索参数**: 可调整检索算法参数
- **显示设置**: 可自定义界面显示

## 📖 使用指南

### 1. 启动系统
```bash
python 启动RAG.py
```

### 2. 输入问题
在界面中输入您的问题，支持以下类型：
- 政策咨询类问题
- 数据分析类问题
- 比较分析类问题

### 3. 观察思考过程
系统会实时展示完整的思考过程，包括：
- 问题分析步骤
- 文档检索过程
- 信息提取结果
- 逻辑推理过程
- 答案生成步骤

### 4. 查看最终答案
系统会提供基于长效思考的专业答案，包括：
- 详细的分析结果
- 置信度评估
- 参考文档来源
- 推理质量分析

## 🤝 贡献指南

我们欢迎任何形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 贡献方式
- 🐛 报告Bug
- 💡 提出新功能
- 📝 完善文档
- 🔧 提交代码

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户。

---

**注意**: 这是一个演示项目，用于展示RAG技术和长效思考机制在银行政策问答中的应用。在生产环境中使用前，请确保进行充分的测试和验证。

## 📊 项目统计

![GitHub stars](https://img.shields.io/github/stars/your-username/bank-policy-rag-system?style=social)
![GitHub forks](https://img.shields.io/github/forks/your-username/bank-policy-rag-system?style=social)
![GitHub issues](https://img.shields.io/github/issues/your-username/bank-policy-rag-system)
![GitHub pull requests](https://img.shields.io/github/issues-pr/your-username/bank-policy-rag-system)



