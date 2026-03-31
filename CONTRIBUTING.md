# 贡献指南

感谢你考虑为Python3 Learning项目做出贡献！本指南将帮助你开始贡献流程。

## 📋 行为准则

本项目遵循[贡献者公约](https://www.contributor-covenant.org/version/2/1/code_of_conduct/)行为准则。请确保你的行为符合该准则。

## 🚀 如何贡献

### 报告Bug
如果你发现了一个bug，请：
1. 检查是否已有相关issue
2. 如果没有，创建一个新的issue
3. 详细描述bug，包括：
   - 重现步骤
   - 期望行为
   - 实际行为
   - 环境信息（Python版本、操作系统等）

### 请求新功能
如果你有功能建议，请：
1. 检查是否已有相关讨论
2. 创建一个新的issue
3. 详细描述：
   - 功能需求
   - 使用场景
   - 可能的实现方案

### 提交代码
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

## 💻 开发环境设置

### 1. 克隆仓库
```bash
git clone https://github.com/tuobi2/python3-learning.git
cd python3-learning
```

### 2. 设置虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

### 3. 安装预提交钩子
```bash
pre-commit install
```

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
./run_tests.sh

# 或直接使用pytest
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ -v --cov=. --cov-report=html
```

### 测试覆盖率要求
- 新代码应包含测试
- 目标覆盖率：80%以上
- 核心功能：90%以上

## 📝 代码规范

### 代码风格
- 遵循[PEP 8](https://pep8.org/)规范
- 使用[Black](https://black.readthedocs.io/)自动格式化
- 使用[isort](https://pycqa.github.io/isort/)排序导入

### 类型提示
- 所有函数和方法都应包含类型提示
- 使用Python 3.9+的类型提示语法

### 文档字符串
- 使用Google风格的文档字符串
- 所有公共函数、类、模块都应包含文档
- 文档应包含参数、返回值和示例

### 提交信息
使用[约定式提交](https://www.conventionalcommits.org/)：
```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `test`: 添加或修改测试
- `chore`: 构建过程或辅助工具

## 🔧 工具配置

### 预提交钩子
项目配置了预提交钩子，会自动：
- 格式化代码（black）
- 排序导入（isort）
- 检查代码风格（flake8）
- 检查类型（mypy）

### 编辑器配置
建议使用以下编辑器配置：

#### VS Code
```json
{
  "python.formatting.provider": "black",
  "python.sortImports.args": ["--profile", "black"],
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true
}
```

#### PyCharm
- 安装Black和isort插件
- 配置为外部工具
- 设置保存时自动格式化

## 📁 项目结构

```
python3-learning/
├── examples/          # Python学习示例
├── projects/         # 完整项目
├── scripts/          # 实用脚本
├── tests/            # 测试文件
├── utils/            # 工具函数
├── docs/             # 文档
└── .github/          # GitHub配置
```

### 添加新示例
1. 根据难度级别选择目录：
   - `examples/basics/` - 基础示例
   - `examples/intermediate/` - 中级示例
   - `examples/advanced/` - 高级示例
2. 创建Python文件
3. 添加详细的文档字符串
4. 添加测试用例

### 添加新工具
1. 添加到`utils/`目录
2. 确保有完整的类型提示
3. 添加单元测试
4. 更新文档

## 🔍 代码审查

### Pull Request流程
1. 确保所有测试通过
2. 确保代码覆盖率不下降
3. 更新相关文档
4. 遵循代码规范
5. 添加有意义的提交信息

### 审查重点
- 代码正确性
- 测试覆盖率
- 代码风格
- 文档完整性
- 性能考虑

## 📚 学习资源

### Python学习
- [Python官方文档](https://docs.python.org/zh-cn/3/)
- [Real Python](https://realpython.com/)
- [Python进阶](https://docs.python-guide.org/)

### 工具学习
- [pytest文档](https://docs.pytest.org/)
- [Black文档](https://black.readthedocs.io/)
- [mypy文档](https://mypy.readthedocs.io/)

## 🤝 社区

### 讨论
- 使用GitHub Discussions进行讨论
- 在Issues中报告问题
- 通过Pull Request提交代码

### 联系方式
- 项目维护者：李杰鹏
- GitHub: [@tuobi2](https://github.com/tuobi2)

## 🙏 致谢

感谢所有为这个项目做出贡献的人！你的每一份贡献都让这个项目变得更好。

---

**Happy Coding!** 🐍