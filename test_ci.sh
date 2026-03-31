#!/bin/bash
# CI测试验证脚本

set -e

echo "========================================"
echo "CI测试验证"
echo "========================================"

# 模拟GitHub Actions环境
echo "1. 检查Python版本..."
python3 --version

echo ""
echo "2. 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov flake8

echo ""
echo "3. 运行基础测试..."
python3 -m pytest tests/test_basic.py -v

echo ""
echo "4. 运行代码检查..."
echo "flake8检查..."
flake8 . --count --max-complexity=15 --max-line-length=127 --statistics --exit-zero

echo ""
echo "5. 检查项目结构..."
echo "检查包初始化..."
if [ -f "utils/__init__.py" ] && [ -f "examples/__init__.py" ]; then
    echo "✅ 包初始化文件存在"
else
    echo "❌ 包初始化文件缺失"
fi

echo ""
echo "6. 验证导入..."
echo "测试utils导入..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    import utils.file_utils
    print('✅ utils.file_utils导入成功')
except ImportError as e:
    print(f'❌ 导入失败: {e}')
"

echo ""
echo "========================================"
echo "CI验证完成!"
echo "如果所有检查都通过，GitHub Actions应该能成功运行。"
echo "访问 https://github.com/tuobi2/python3-learning/actions 查看状态"
echo "========================================"