# 贡献指南

感谢您对银行政策知识库RAG系统的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 1. Fork 项目
1. 点击项目页面右上角的 "Fork" 按钮
2. 将项目克隆到本地：
   ```bash
   git clone https://github.com/your-username/bank-policy-rag-system.git
   cd bank-policy-rag-system
   ```

### 2. 创建分支
```bash
git checkout -b feature/your-feature-name
```

### 3. 进行开发
- 编写代码
- 添加测试
- 更新文档

### 4. 提交更改
```bash
git add .
git commit -m "Add: 描述您的更改"
```

### 5. 推送分支
```bash
git push origin feature/your-feature-name
```

### 6. 创建 Pull Request
1. 在 GitHub 上创建 Pull Request
2. 详细描述您的更改
3. 等待代码审查

## 开发规范

### 代码风格
- 使用 Python PEP 8 代码风格
- 函数和类名使用下划线命名法
- 常量使用大写字母
- 添加适当的注释和文档字符串

### 提交信息规范
- 使用中文描述
- 格式：`类型: 描述`
- 类型包括：`新增`、`修复`、`更新`、`删除`、`重构`

示例：
```
新增: 添加长效思考功能
修复: 解决内存泄漏问题
更新: 优化检索算法性能
```

### 测试要求
- 新功能必须包含测试用例
- 测试覆盖率不低于 80%
- 所有测试必须通过

## 贡献类型

### 1. 代码贡献
- 新功能开发
- Bug 修复
- 性能优化
- 代码重构

### 2. 文档贡献
- 完善 README
- 添加使用示例
- 更新 API 文档
- 翻译文档

### 3. 测试贡献
- 编写单元测试
- 集成测试
- 性能测试
- 用户测试

### 4. 问题报告
- 发现 Bug
- 提出改进建议
- 功能需求
- 性能问题

## 开发环境设置

### 1. 环境准备
```bash
# 克隆项目
git clone https://github.com/your-username/bank-policy-rag-system.git
cd bank-policy-rag-system

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. 开发工具
```bash
# 安装开发依赖
pip install black flake8 pytest coverage

# 代码格式化
black .

# 代码检查
flake8 .

# 运行测试
pytest

# 生成覆盖率报告
coverage run -m pytest
coverage report
```

## 项目结构

```
bank-policy-rag-system/
├── README.md                 # 项目说明
├── CONTRIBUTING.md           # 贡献指南
├── LICENSE                   # 许可证
├── requirements.txt          # 生产依赖
├── requirements-dev.txt      # 开发依赖
├── .gitignore               # Git 忽略文件
├── 启动RAG.py               # 启动脚本
├── 长效思考RAG.py           # 主应用
├── docs/                    # 文档目录
│   ├── 系统架构.md
│   ├── API文档.md
│   └── 部署指南.md
├── tests/                   # 测试目录
│   ├── test_rag.py
│   ├── test_reasoning.py
│   └── test_api.py
├── knowledge_base/          # 知识库
│   ├── documents/
│   ├── index/
│   └── config/
└── static/                  # 静态文件
    ├── css/
    ├── js/
    └── images/
```

## 代码审查流程

### 1. 自动检查
- 代码风格检查
- 单元测试
- 集成测试
- 安全扫描

### 2. 人工审查
- 代码质量
- 功能完整性
- 性能影响
- 安全性

### 3. 合并标准
- 所有检查通过
- 至少一个审查者同意
- 无冲突
- 测试通过

## 发布流程

### 1. 版本号规范
- 主版本号：不兼容的 API 修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 2. 发布步骤
1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建 Release
4. 打标签
5. 发布到 PyPI

## 社区规范

### 1. 行为准则
- 尊重他人
- 建设性讨论
- 包容性环境
- 专业态度

### 2. 沟通渠道
- GitHub Issues：问题报告和功能请求
- GitHub Discussions：技术讨论
- Pull Requests：代码贡献
- 邮件：重要通知

## 许可证

本项目采用 MIT 许可证。贡献者需要同意将代码以相同许可证发布。

## 联系方式

- 项目维护者：your-email@example.com
- 项目主页：https://github.com/your-username/bank-policy-rag-system
- 问题反馈：https://github.com/your-username/bank-policy-rag-system/issues

感谢您的贡献！
