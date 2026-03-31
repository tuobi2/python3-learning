#!/bin/bash
# 检查GitHub Actions状态

set -e

echo "========================================"
echo "GitHub Actions状态检查"
echo "========================================"

REPO="tuobi2/python3-learning"
echo "仓库: $REPO"

# 使用GitHub API检查最新的工作流运行
echo ""
echo "检查最新工作流运行..."

# 尝试获取工作流运行状态
API_URL="https://api.github.com/repos/$REPO/actions/runs"

# 显示最近的工作流
echo "最近的工作流运行:"
echo "访问: https://github.com/$REPO/actions"

# 提供直接链接
echo ""
echo "直接链接:"
echo "  • Actions主页: https://github.com/$REPO/actions"
echo "  • 测试工作流: https://github.com/$REPO/actions/workflows/test.yml"
echo "  • 代码质量工作流: https://github.com/$REPO/actions/workflows/code-quality.yml"

# 检查本地测试状态
echo ""
echo "本地测试状态:"
if [ -f "tests/test_basic.py" ]; then
    echo "运行基础测试..."
    if python3 -m pytest tests/test_basic.py -v 2>&1 | grep -q "PASSED\|passed"; then
        echo "✅ 基础测试通过"
    else
        echo "❌ 基础测试失败"
    fi
else
    echo "⚠️  未找到基础测试文件"
fi

# 检查项目结构
echo ""
echo "项目结构检查:"
if [ -f "utils/__init__.py" ]; then
    echo "✅ utils包已初始化"
else
    echo "❌ utils包未初始化"
fi

if [ -f "examples/__init__.py" ]; then
    echo "✅ examples包已初始化"
else
    echo "❌ examples包未初始化"
fi

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt存在"
else
    echo "❌ requirements.txt不存在"
fi

# 建议
echo ""
echo "========================================"
echo "建议:"
echo "1. 访问 https://github.com/$REPO/actions 查看工作流状态"
echo "2. 如果工作流失败，点击失败的工作流查看详细日志"
echo "3. 常见问题:"
echo "   • 依赖安装失败 - 检查requirements.txt"
echo "   • 测试失败 - 检查测试文件语法"
echo "   • 导入错误 - 检查__init__.py文件"
echo "4. 本地测试命令: python3 -m pytest tests/test_basic.py -v"
echo "========================================"

echo ""
echo "如果需要进一步调试，请提供GitHub Actions的失败日志。"