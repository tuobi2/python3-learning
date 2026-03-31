#!/bin/bash
# Docker运行脚本

set -e

echo "========================================"
echo "Python3-learning Docker运行"
echo "========================================"

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未找到Docker命令"
    echo "请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: 未找到docker-compose命令"
    echo "请先安装Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker版本: $(docker --version)"
echo "✅ Docker Compose版本: $(docker-compose --version)"
echo ""

# 选择运行模式
echo "选择运行模式:"
echo "  1. 运行FastAPI示例 (端口: 8000)"
echo "  2. 运行报销系统 (端口: 8001)"
echo "  3. 运行开发环境 (热重载, 端口: 8002)"
echo "  4. 运行所有服务"
echo "  5. 构建镜像"
echo "  6. 停止所有服务"
echo "  7. 清理容器和镜像"
echo "  8. 进入容器Shell"
echo "  9. 退出"
read -p "请选择 (1-9): " choice

case $choice in
    1)
        echo "启动FastAPI示例..."
        docker-compose up -d fastapi-example
        echo "✅ 服务已启动"
        echo "访问: http://localhost:8000/docs"
        echo "查看日志: docker-compose logs -f fastapi-example"
        ;;
    2)
        echo "启动报销系统..."
        docker-compose up -d reimbursement-system
        echo "✅ 服务已启动"
        echo "访问: http://localhost:8001/docs"
        echo "查看日志: docker-compose logs -f reimbursement-system"
        ;;
    3)
        echo "启动开发环境..."
        docker-compose up -d dev
        echo "✅ 开发环境已启动"
        echo "访问: http://localhost:8002/docs"
        echo "查看日志: docker-compose logs -f dev"
        echo "修改代码会自动重载"
        ;;
    4)
        echo "启动所有服务..."
        docker-compose up -d
        echo "✅ 所有服务已启动"
        echo ""
        echo "服务状态:"
        docker-compose ps
        echo ""
        echo "访问地址:"
        echo "  FastAPI示例: http://localhost:8000/docs"
        echo "  报销系统:    http://localhost:8001/docs"
        echo "  开发环境:    http://localhost:8002/docs"
        echo ""
        echo "查看日志: docker-compose logs -f"
        ;;
    5)
        echo "构建Docker镜像..."
        docker-compose build
        echo "✅ 镜像构建完成"
        ;;
    6)
        echo "停止所有服务..."
        docker-compose down
        echo "✅ 服务已停止"
        ;;
    7)
        echo "清理Docker资源..."
        read -p "确认删除所有容器和镜像? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v --rmi all
            docker system prune -f
            echo "✅ 清理完成"
        else
            echo "取消清理"
        fi
        ;;
    8)
        echo "进入容器Shell..."
        echo "选择容器:"
        echo "  1. FastAPI示例容器"
        echo "  2. 报销系统容器"
        echo "  3. 开发容器"
        read -p "请选择 (1-3): " container_choice
        
        case $container_choice in
            1)
                CONTAINER="python3-fastapi-example"
                ;;
            2)
                CONTAINER="python3-reimbursement-system"
                ;;
            3)
                CONTAINER="python3-dev"
                ;;
            *)
                echo "无效选择"
                exit 1
                ;;
        esac
        
        docker exec -it $CONTAINER /bin/bash
        ;;
    9)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo ""
echo "常用命令:"
echo "  docker-compose ps           # 查看服务状态"
echo "  docker-compose logs -f      # 查看日志"
echo "  docker-compose down         # 停止服务"
echo "  docker-compose up -d        # 启动服务"