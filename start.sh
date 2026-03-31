#!/bin/bash
# Python3-learning项目启动脚本
# 自动处理python/python3命令问题

set -e

echo "========================================"
echo "Python3-learning 项目启动"
echo "========================================"

# 检查Python命令
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✅ 使用命令: python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✅ 使用命令: python3"
else
    echo "❌ 错误: 未找到Python命令!"
    echo "请先安装Python3: https://www.python.org/downloads/"
    exit 1
fi

# 显示Python版本
$PYTHON_CMD --version

echo ""
echo "可用命令:"
echo "  1. 运行基础示例"
echo "  2. 运行Web应用示例"
echo "  3. 运行报销系统"
echo "  4. 列出所有文件"
echo "  5. 检查环境"
echo "  6. 退出"
echo ""

read -p "请选择 (1-6): " choice

case $choice in
    1)
        echo "运行基础示例..."
        $PYTHON_CMD examples/basics/python_fundamentals.py
        ;;
    2)
        echo "运行Web应用示例..."
        $PYTHON_CMD examples/intermediate/fastapi_web_app.py
        echo ""
        echo "✅ Web应用已启动!"
        echo "访问 http://127.0.0.1:8000/docs"
        echo "按 Ctrl+C 停止服务"
        ;;
    3)
        echo "运行报销系统..."
        cd projects/reimbursement-system
        $PYTHON_CMD main.py
        ;;
    4)
        echo "项目文件列表:"
        echo "========================================"
        find . -name "*.py" -type f | grep -v __pycache__ | grep -v venv | sort
        echo "========================================"
        echo "总计: $(find . -name "*.py" -type f | grep -v __pycache__ | grep -v venv | wc -l) 个Python文件"
        ;;
    5)
        echo "环境检查:"
        echo "========================================"
        echo "Python版本:"
        $PYTHON_CMD --version
        echo ""
        echo "Python路径:"
        $PYTHON_CMD -c "import sys; print(sys.executable)"
        echo ""
        echo "项目目录:"
        pwd
        echo ""
        echo "虚拟环境:"
        if [ -d "venv" ]; then
            echo "✅ 找到venv目录"
            source venv/bin/activate 2>/dev/null && echo "虚拟环境已激活" || echo "虚拟环境未激活"
        else
            echo "ℹ️  未找到venv目录"
        fi
        ;;
    6)
        echo "再见!"
        exit 0
        ;;
    *)
        echo "无效选择!"
        exit 1
        ;;
esac