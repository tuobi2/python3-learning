#!/bin/bash
# 最简单的Web应用运行脚本

echo "========================================"
echo "运行Python Web应用"
echo "========================================"

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  不在虚拟环境中"
    
    # 检查是否有venv目录
    if [ -d "venv" ]; then
        echo "找到venv目录，正在激活..."
        source venv/bin/activate
        echo "✅ 虚拟环境已激活"
    else
        echo "❌ 错误: 未找到虚拟环境"
        echo ""
        echo "请先设置虚拟环境:"
        echo "  方法1: 运行 ./setup_venv.sh"
        echo "  方法2: 手动创建:"
        echo "    python3 -m venv venv"
        echo "    source venv/bin/activate"
        echo "    pip install -r requirements.txt"
        echo ""
        echo "或使用Docker运行: ./docker-run.sh"
        exit 1
    fi
else
    echo "✅ 已在虚拟环境中: $VIRTUAL_ENV"
fi

# 检查Python
if ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到python命令"
    echo "请确保虚拟环境已正确激活"
    exit 1
fi

echo "Python版本: $(python --version)"
echo ""

# 运行Web应用
APP_FILE="examples/intermediate/fastapi_web_app.py"

if [ ! -f "$APP_FILE" ]; then
    echo "❌ 错误: 文件不存在 - $APP_FILE"
    exit 1
fi

echo "运行: $APP_FILE"
echo "端口: 8000"
echo "访问: http://127.0.0.1:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================"

# 运行应用
python "$APP_FILE"