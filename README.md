# Python3 Learning Projects 🐍

Python3学习项目和示例代码集合，包含从基础到高级的完整学习路径。

## 📋 项目概述

这是一个全面的Python3学习资源库，包含：

- **基础示例**：Python核心语法和概念
- **中级示例**：Web开发、API设计、文件操作
- **高级示例**：LLM集成、多智能体系统、设计模式
- **完整项目**：基于Clean Architecture的报销管理系统
- **实用工具**：项目生成脚本、开发工具

## 🚀 快速开始

### 环境要求
- Python 3.9+
- pip (Python包管理器)

### 安装依赖
```bash
# 创建虚拟环境（推荐）
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 运行示例
```bash
# 运行基础示例
python examples/basics/python_fundamentals.py

# 运行Web应用示例
python examples/intermediate/fastapi_web_app.py
# 访问 http://127.0.0.1:8000/docs

# 运行报销系统
cd projects/reimbursement-system
python main.py
```

## 📁 项目结构

```
python3-learning/
├── examples/                    # Python示例
│   ├── basics/                 # 基础示例
│   │   ├── python_fundamentals.py  # Python基础语法
│   │   ├── data_types.py           # 数据类型详解
│   │   └── control_flow.py         # 控制流示例
│   ├── intermediate/           # 中级示例
│   │   ├── fastapi_web_app.py     # FastAPI Web应用
│   │   ├── file_operations.py     # 文件操作
│   │   └── api_integration.py     # API集成
│   ├── advanced/              # 高级示例
│   │   ├── spark_llm_integration.py  # LLM集成
│   │   ├── multi_agent_system.py     # 多智能体系统
│   │   └── design_patterns.py        # 设计模式
│   └── web/                   # Web开发示例
│       ├── fastapi_basics.py      # FastAPI基础
│       └── rest_api_design.py     # REST API设计
├── projects/                  # 完整项目
│   └── reimbursement-system/  # 报销管理系统
│       ├── src/              # 源代码
│       ├── tests/            # 测试用例
│       ├── docs/             # 项目文档
│       └── requirements.txt  # 项目依赖
├── scripts/                  # 实用脚本
│   ├── create_project.sh     # 项目生成脚本
│   ├── github_push.sh        # GitHub推送脚本
│   ├── run_examples.py       # 示例运行脚本
│   └── setup_environment.sh  # 环境设置脚本
├── docs/                     # 文档
│   ├── getting_started.md    # 入门指南
│   ├── api_reference.md      # API参考
│   └── architecture.md       # 架构设计
├── tests/                    # 测试文件
│   ├── test_basics.py        # 基础测试
│   ├── test_intermediate.py  # 中级测试
│   └── test_advanced.py      # 高级测试
├── utils/                    # 工具函数
│   ├── file_utils.py         # 文件工具
│   ├── validation.py         # 验证工具
│   └── logging_config.py     # 日志配置
├── config/                   # 配置文件
│   ├── settings.py           # 应用设置
│   └── constants.py          # 常量定义
├── .gitignore               # Git忽略规则
├── requirements.txt         # 项目依赖
├── pyproject.toml          # 项目配置
└── README.md               # 项目说明
```

## 📚 学习路径

### 初学者路径
1. **基础语法** → `examples/basics/python_fundamentals.py`
2. **数据类型** → `examples/basics/data_types.py`
3. **控制流** → `examples/basics/control_flow.py`
4. **函数和类** → `examples/basics/functions_classes.py`

### 中级开发者路径
1. **Web开发** → `examples/intermediate/fastapi_web_app.py`
2. **文件操作** → `examples/intermediate/file_operations.py`
3. **错误处理** → `examples/intermediate/error_handling.py`
4. **API集成** → `examples/intermediate/api_integration.py`

### 高级开发者路径
1. **LLM集成** → `examples/advanced/spark_llm_integration.py`
2. **多智能体** → `examples/advanced/multi_agent_system.py`
3. **设计模式** → `examples/advanced/design_patterns.py`
4. **异步编程** → `examples/advanced/async_programming.py`

### 项目实践
1. **报销系统** → `projects/reimbursement-system/`
2. **代码审查** → 阅读和理解完整项目代码
3. **功能扩展** → 基于现有项目添加新功能

## 🔧 实用工具

### 项目生成脚本
```bash
# 生成新的Python项目
./scripts/create_project.sh my-new-project
```

### 示例运行脚本
```bash
# 运行所有示例
python scripts/run_examples.py

# 运行特定类别示例
python scripts/run_examples.py --category basics
```

### GitHub推送脚本
```bash
# 推送代码到GitHub
./scripts/github_push.sh
```

## 🎯 项目特点

### 代码质量
- ✅ 完整的类型提示
- ✅ 详细的文档字符串
- ✅ 符合PEP 8规范
- ✅ 统一的代码风格

### 学习价值
- ✅ 从基础到高级的完整路径
- ✅ 实际可运行的项目示例
- ✅ 详细的注释和解释
- ✅ 渐进式难度设计

### 实用性
- ✅ 可直接复用的代码片段
- ✅ 完整的项目架构示例
- ✅ 生产级别的代码质量
- ✅ 现代化的技术栈

## 📖 详细文档

### 基础语法
- [Python基础语法指南](docs/basics/python_fundamentals.md)
- [数据类型详解](docs/basics/data_types.md)
- [控制流和函数](docs/basics/control_flow.md)

### Web开发
- [FastAPI入门指南](docs/web/fastapi_basics.md)
- [REST API设计](docs/web/rest_api_design.md)
- [错误处理最佳实践](docs/web/error_handling.md)

### 高级主题
- [LLM集成指南](docs/advanced/llm_integration.md)
- [多智能体系统](docs/advanced/multi_agent_systems.md)
- [设计模式应用](docs/advanced/design_patterns.md)

### 项目文档
- [报销系统架构](projects/reimbursement-system/docs/architecture.md)
- [API接口文档](projects/reimbursement-system/docs/api.md)
- [部署指南](projects/reimbursement-system/docs/deployment.md)

## 🧪 测试

运行测试确保代码质量：
```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_basics.py

# 生成测试覆盖率报告
pytest --cov=examples --cov-report=html
```

## 🤝 贡献指南

欢迎贡献代码、文档或提出建议！

### 贡献步骤
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

### 代码规范
- 遵循PEP 8代码风格
- 添加类型提示
- 编写文档字符串
- 添加测试用例

### 提交信息规范
使用约定式提交：
- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🚀 GitHub推送指南

项目已配置多种推送方式，支持GitHub Token认证：

### 推送方法
```bash
# 方法1: 使用一键推送脚本（推荐）
./push_to_github.sh

# 方法2: 使用简单Token脚本
./push_with_token_simple.sh

# 方法3: 使用环境变量
cp .env.example .env  # 编辑.env文件填入Token
./push_with_env.sh
```

### Token要求
GitHub Personal Access Token需要 `repo` 权限。详细指南见 [GITHUB_PUSH_GUIDE.md](GITHUB_PUSH_GUIDE.md)

## 📞 联系

如有问题或建议：
- 提交 [GitHub Issue](https://github.com/tuobi2/python3-learning/issues)
- 查看项目 [讨论区](https://github.com/tuobi2/python3-learning/discussions)

## 🙏 致谢

感谢所有为这个项目做出贡献的人！

---

**Happy Coding!** 🐍

> 学习Python最好的方式就是动手实践。从这个项目开始，逐步构建你的Python技能树！