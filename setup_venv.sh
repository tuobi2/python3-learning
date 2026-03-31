#!/bin/bash
# Python3-learning 虚拟环境设置脚本

set -e

echo "========================================"
echo "Python3-learning 虚拟环境设置"
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
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "ℹ️  已在虚拟环境中: $VIRTUAL_ENV"
    read -p "是否继续设置? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# 创建虚拟环境
VENV_DIR="venv"
if [ -d "$VENV_DIR" ]; then
    echo "ℹ️  虚拟环境已存在: $VENV_DIR"
    read -p "是否重新创建? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "删除旧虚拟环境..."
        rm -rf "$VENV_DIR"
        python3 -m venv "$VENV_DIR"
        echo "✅ 虚拟环境已重新创建"
    else
        echo "使用现有虚拟环境"
    fi
else
    echo "创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
    echo "✅ 虚拟环境已创建: $VENV_DIR"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source "$VENV_DIR/bin/activate"

# 升级pip
echo "升级pip..."
pip install --upgrade pip

# 安装依赖
echo "安装项目依赖..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ 项目依赖安装完成"
else
    echo "⚠️  未找到requirements.txt，安装基础依赖..."
    pip install fastapi==0.110.0 uvicorn==0.29.0 pydantic==2.6.4 requests==2.31.0 python-dotenv==1.0.1
    echo "✅ 基础依赖安装完成"
fi

# 安装开发依赖（可选）
read -p "是否安装开发依赖? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "安装开发依赖..."
    pip install pytest pytest-cov black flake8 mypy
    echo "✅ 开发依赖安装完成"
fi

echo ""
echo "========================================"
echo "虚拟环境设置完成!"
echo "========================================"
echo ""
echo "✅ 虚拟环境: $VENV_DIR"
echo "✅ Python: $(python --version)"
echo "✅ Pip: $(pip --version | cut -d' ' -f2)"
echo ""
echo "使用命令:"
echo "  source $VENV_DIR/bin/activate    # 激活虚拟环境"
echo "  deactivate                       # 退出虚拟环境"
echo ""
echo "运行项目:"
echo "  ./run_web.sh                     # 运行Web应用"
echo "  ./run_examples.sh                # 运行示例"
echo ""

# 创建快捷运行脚本
create_run_scripts() {
    echo "创建运行脚本..."
    
    # run_web.sh
    cat > run_web.sh << 'EOF'
#!/bin/bash
# 运行Web应用脚本

set -e

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" == "" ]]; then
    if [ -d "venv" ]; then
        echo "激活虚拟环境..."
        source venv/bin/activate
    else
        echo "❌ 错误: 未找到虚拟环境"
        echo "请先运行: ./setup_venv.sh"
        exit 1
    fi
fi

echo "========================================"
echo "运行Web应用"
echo "========================================"

# 检查Python
if ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到python命令"
    exit 1
fi

echo "Python版本: $(python --version)"
echo "虚拟环境: $VIRTUAL_ENV"
echo ""

# 选择要运行的Web应用
echo "选择Web应用:"
echo "  1. FastAPI示例 (examples/intermediate/fastapi_web_app.py)"
echo "  2. 报销系统 (projects/reimbursement-system/main.py)"
echo "  3. 退出"
read -p "请选择 (1-3): " choice

case $choice in
    1)
        APP_FILE="examples/intermediate/fastapi_web_app.py"
        PORT=8000
        ;;
    2)
        APP_FILE="projects/reimbursement-system/main.py"
        PORT=8001
        ;;
    3)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

if [ ! -f "$APP_FILE" ]; then
    echo "❌ 错误: 文件不存在 - $APP_FILE"
    exit 1
fi

echo ""
echo "运行: $APP_FILE"
echo "端口: $PORT"
echo "访问: http://127.0.0.1:$PORT/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================"

# 运行应用
python "$APP_FILE"
EOF

    # run_examples.sh
    cat > run_examples.sh << 'EOF'
#!/bin/bash
# 运行示例脚本

set -e

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" == "" ]]; then
    if [ -d "venv" ]; then
        echo "激活虚拟环境..."
        source venv/bin/activate
    else
        echo "❌ 错误: 未找到虚拟环境"
        echo "请先运行: ./setup_venv.sh"
        exit 1
    fi
fi

echo "========================================"
echo "运行Python示例"
echo "========================================"

echo "Python版本: $(python --version)"
echo "虚拟环境: $VIRTUAL_ENV"
echo ""

# 选择示例
echo "选择示例类别:"
echo "  1. 基础示例 (自动运行版)"
echo "  2. 基础示例 (完整交互版)"
echo "  3. 所有示例"
echo "  4. 退出"
read -p "请选择 (1-4): " choice

case $choice in
    1)
        EXAMPLE_FILE="examples/basics/python_fundamentals_auto.py"
        echo "运行基础示例 (自动版)..."
        python "$EXAMPLE_FILE"
        ;;
    2)
        EXAMPLE_FILE="examples/basics/python_fundamentals.py"
        echo "运行基础示例 (交互版)..."
        echo "注意: 需要按Enter继续"
        python "$EXAMPLE_FILE"
        ;;
    3)
        echo "运行所有示例..."
        python scripts/run_all_examples.py --interactive
        ;;
    4)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac
EOF

    # 设置执行权限
    chmod +x run_web.sh run_examples.sh
    
    echo "✅ 运行脚本已创建"
    echo "  ./run_web.sh      # 运行Web应用"
    echo "  ./run_examples.sh # 运行示例"
}

# 询问是否创建运行脚本
read -p "是否创建运行脚本? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    create_run_scripts
fi

echo ""
echo "🎉 设置完成! 现在可以运行:"
echo "  source venv/bin/activate"
echo "  然后使用上面的运行脚本"