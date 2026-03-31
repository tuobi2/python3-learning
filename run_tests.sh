#!/bin/bash
# 运行测试脚本

set -e

echo "========================================"
echo "Python3项目测试运行"
echo "========================================"

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  不在虚拟环境中"
    
    if [ -d "venv" ]; then
        echo "激活虚拟环境..."
        source venv/bin/activate
    else
        echo "❌ 错误: 未找到虚拟环境"
        echo "请先运行: ./setup_venv.sh"
        exit 1
    fi
fi

echo "Python版本: $(python --version)"
echo "工作目录: $(pwd)"
echo ""

# 检查pytest
if ! python -c "import pytest" 2>/dev/null; then
    echo "安装pytest..."
    pip install pytest pytest-cov
fi

# 选择测试模式
echo "选择测试模式:"
echo "  1. 运行所有测试"
echo "  2. 运行单元测试"
echo "  3. 运行特定测试文件"
echo "  4. 运行测试并生成覆盖率报告"
echo "  5. 退出"
read -p "请选择 (1-5): " choice

case $choice in
    1)
        echo "运行所有测试..."
        python -m pytest tests/ -v
        ;;
    2)
        echo "运行单元测试..."
        python -m pytest tests/unit/ -v
        ;;
    3)
        echo "可用测试文件:"
        find tests/ -name "test_*.py" | sort
        echo ""
        read -p "请输入测试文件路径: " test_file
        if [ -f "$test_file" ]; then
            python -m pytest "$test_file" -v
        else
            echo "❌ 文件不存在: $test_file"
            exit 1
        fi
        ;;
    4)
        echo "运行测试并生成覆盖率报告..."
        if python -c "import pytest_cov" 2>/dev/null; then
            python -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html
            echo ""
            echo "✅ 覆盖率报告已生成"
            echo "打开: file://$(pwd)/htmlcov/index.html"
        else
            echo "安装pytest-cov..."
            pip install pytest-cov
            python -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html
        fi
        ;;
    5)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "测试完成!"
echo "========================================"