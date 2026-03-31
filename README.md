# Python3 Learning Projects

Python3学习项目和示例代码集合。

## 项目结构

### 1. Python学习示例
- `demo.py` - 基础Python语法和功能示例
- `demo2.py` - 进阶Python编程示例
- `demo3.py` - 高级Python特性和模式
- `generate_python_project.sh` - Python项目生成脚本
- `readme.txt` - 项目说明文档

### 2. 报销管理系统 (Clean Architecture)
位于 `reimbursement-clean-arch-python/` 目录

#### 架构设计
```
reimbursement-clean-arch-python/
├── src/
│   ├── domain/              # 领域层
│   │   └── entities/        # 领域实体
│   │       ├── bill.py      # 账单实体
│   │       └── notification.py # 通知实体
│   ├── use_cases/           # 用例层
│   │   ├── audit/           # 审计用例
│   │   ├── classify/        # 分类用例
│   │   └── dispatcher/      # 分发处理用例
│   └── interface_adapters/  # 接口适配器层
│       ├── llm/             # LLM适配器
│       ├── repositories/    # 仓储适配器
│       └── invoice/         # 发票适配器
├── frameworks/              # 框架层
│   ├── api/                 # API框架
│   └── config/              # 配置管理
├── main.py                  # 应用入口
└── requirements.txt         # 依赖列表
```

#### 功能特性
- **账单分类**：使用LLM智能分类报销项目
- **审计检查**：自动审计报销合规性
- **流程分发**：根据类型分发处理流程
- **FastAPI集成**：提供RESTful API接口
- **Spark LLM集成**：大语言模型能力集成

## 技术栈

### 核心语言
- Python 3.x

### 主要框架和库
- FastAPI - 现代Web框架
- Pydantic - 数据验证和设置管理
- 干净架构 - 软件架构设计模式

### 开发工具
- Git - 版本控制
- 虚拟环境 - 依赖隔离

## 快速开始

### 环境设置
```bash
# 克隆项目
git clone git@github.com:tuobi2/python3-learning.git
cd python3-learning

# 进入报销项目
cd reimbursement-clean-arch-python

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 运行示例
```bash
# 运行Python示例
python demo.py
python demo2.py
python demo3.py

# 运行报销系统
cd reimbursement-clean-arch-python
python main.py
```

### 生成新项目
```bash
# 使用项目生成脚本
./generate_python_project.sh my-new-project
```

## 学习资源

### Python基础
- `demo.py` - 变量、数据类型、控制流
- `demo2.py` - 函数、类、模块
- `demo3.py` - 装饰器、生成器、上下文管理器

### 软件架构
- 干净架构原理和实践
- 领域驱动设计(DDD)基础
- 依赖倒置原则

### Web开发
- FastAPI快速入门
- RESTful API设计
- 异步编程

## 项目目标

1. **学习Python3**：掌握现代Python编程
2. **实践干净架构**：理解分层架构设计
3. **构建实际项目**：开发可用的报销管理系统
4. **代码质量**：培养良好的编程习惯

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

### 开发流程
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

## 许可证

本项目仅供学习使用。

## 联系

如有问题或建议，请通过GitHub Issues联系。

---

**Happy Coding!** 🐍