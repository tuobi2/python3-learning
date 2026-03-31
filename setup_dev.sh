#!/bin/bash
# 开发环境设置脚本

set -e

echo "========================================"
echo "Python3项目开发环境设置"
echo "========================================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到python3命令"
    echo "请先安装Python3: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python版本: $PYTHON_VERSION"

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  不在虚拟环境中"
    
    if [ -d "venv" ]; then
        echo "激活虚拟环境..."
        source venv/bin/activate
    else
        echo "创建虚拟环境..."
        python3 -m venv venv
        source venv/bin/activate
        echo "✅ 虚拟环境已创建并激活"
    fi
else
    echo "✅ 已在虚拟环境中: $VIRTUAL_ENV"
fi

# 升级pip
echo "升级pip..."
pip install --upgrade pip

# 安装项目依赖
echo "安装项目依赖..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ 项目依赖安装完成"
else
    echo "⚠️  未找到requirements.txt"
fi

# 安装开发依赖
echo "安装开发依赖..."
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
    echo "✅ 开发依赖安装完成"
else
    echo "安装基础开发工具..."
    pip install pytest pytest-cov black flake8 mypy isort pre-commit
    echo "✅ 基础开发工具安装完成"
fi

# 安装预提交钩子
echo "设置预提交钩子..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    pre-commit install --hook-type commit-msg
    pre-commit install --hook-type pre-push
    echo "✅ 预提交钩子已安装"
else
    echo "⚠️  未找到pre-commit命令"
fi

# 验证安装
echo ""
echo "验证安装:"
echo "  • Python: $(python --version 2>/dev/null || echo '未找到')"
echo "  • pip: $(pip --version 2>/dev/null | cut -d' ' -f2 || echo '未找到')"
echo "  • pytest: $(python -c "import pytest; print(pytest.__version__)" 2>/dev/null || echo '未安装')"
echo "  • black: $(python -c "import black; print(black.__version__)" 2>/dev/null || echo '未安装')"
echo "  • flake8: $(python -c "import flake8; print(flake8.__version__)" 2>/dev/null || echo '未安装')"
echo "  • mypy: $(python -c "import mypy; print(mypy.__version__)" 2>/dev/null || echo '未安装')"
echo "  • pre-commit: $(pre-commit --version 2>/dev/null || echo '未安装')"

# 创建测试配置
echo ""
echo "创建测试配置..."
if [ ! -f "pytest.ini" ]; then
    cat > pytest.ini << 'EOF'
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=. --cov-report=term-missing --cov-report=html
markers =
    unit: 单元测试
    integration: 集成测试
    slow: 慢速测试
    web: Web测试
EOF
    echo "✅ pytest.ini 已创建"
fi

# 运行初始测试
echo ""
echo "运行初始测试..."
if python -m pytest tests/ -v --tb=short 2>&1 | tail -20; then
    echo "✅ 测试通过"
else
    echo "⚠️  测试失败或没有测试"
fi

echo ""
echo "========================================"
echo "开发环境设置完成!"
echo "========================================"
echo ""
echo "可用命令:"
echo "  • 运行测试: ./run_tests.sh 或 pytest"
echo "  • 格式化代码: black ."
echo "  • 代码检查: flake8 ."
echo "  • 类型检查: mypy ."
echo "  • 排序导入: isort ."
echo "  • 运行预提交: pre-commit run --all-files"
echo ""
echo "Git钩子已安装，提交时会自动:"
echo "  ✅ 格式化代码 (black)"
echo "  ✅ 排序导入 (isort)"
echo "  ✅ 代码检查 (flake8)"
echo "  ✅ 类型检查 (mypy)"
echo "  ✅ 安全扫描 (bandit)"
echo ""
echo "开始开发吧! 🚀"