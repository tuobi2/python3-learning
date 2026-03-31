#!/bin/bash
# 一键推送Python3项目到GitHub (使用SSH)

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查SSH认证
check_ssh_auth() {
    print_info "检查SSH认证..."
    if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        print_success "SSH认证成功"
        return 0
    else
        print_error "SSH认证失败"
        echo ""
        print_info "请先设置SSH密钥:"
        echo "  1. 生成SSH密钥: ssh-keygen -t ed25519 -C \"your_email@example.com\""
        echo "  2. 添加到GitHub: https://github.com/settings/keys"
        echo "  3. 测试连接: ssh -T git@github.com"
        return 1
    fi
}

# 主函数
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}    Python3项目GitHub推送工具 (SSH版)${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    # 检查git仓库
    if [ ! -d ".git" ]; then
        print_error "当前目录不是git仓库"
        exit 1
    fi
    
    # 检查SSH认证
    if ! check_ssh_auth; then
        exit 1
    fi
    
    # 显示当前状态
    REPO_URL=$(git config --get remote.origin.url)
    BRANCH=$(git branch --show-current)
    COMMIT_HASH=$(git rev-parse --short HEAD)
    
    print_info "仓库: $(basename -s .git $REPO_URL)"
    print_info "分支: $BRANCH"
    print_info "最新提交: $COMMIT_HASH"
    
    # 显示待推送的更改
    echo ""
    print_info "待推送的更改:"
    git status --short
    
    # 显示最近提交
    echo ""
    print_info "最近提交:"
    git log --oneline -3
    
    # 提取仓库路径
    if [[ $REPO_URL == git@github.com:* ]]; then
        REPO_PATH=$(echo $REPO_URL | sed 's/git@github.com://' | sed 's/\.git$//')
    elif [[ $REPO_URL == https://github.com/* ]]; then
        REPO_PATH=$(echo $REPO_URL | sed 's|https://github.com/||' | sed 's/\.git$//')
    else
        print_error "不支持的仓库URL格式: $REPO_URL"
        exit 1
    fi
    
    # 确认推送
    echo ""
    print_warning "即将使用SSH推送到: https://github.com/$REPO_PATH"
    read -p "确认推送? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "取消推送"
        exit 0
    fi
    
    # 推送
    print_info "推送中..."
    if git push origin "$BRANCH"; then
        print_success "推送成功!"
        SUCCESS=true
    else
        print_error "推送失败"
        
        # 询问是否强制推送
        read -p "是否尝试强制推送? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_warning "强制推送..."
            if git push -f origin "$BRANCH"; then
                print_success "强制推送成功!"
                SUCCESS=true
            else
                print_error "强制推送失败"
                SUCCESS=false
            fi
        else
            SUCCESS=false
        fi
    fi
    
    # 显示结果
    echo ""
    echo -e "${BLUE}========================================${NC}"
    if [ "$SUCCESS" = true ]; then
        print_success "🎉 项目已成功推送到GitHub!"
        
        # 显示项目信息
        echo ""
        print_info "项目信息:"
        echo "  • 名称: Python3 Learning"
        echo "  • 描述: Python3学习项目，包含基础语法、Web应用、工具函数等"
        echo "  • 结构: examples/, projects/, scripts/, utils/"
        echo "  • 文件数: $(git ls-files | wc -l)"
        echo "  • Python文件: $(find . -name "*.py" -type f | grep -v __pycache__ | wc -l)"
        
        echo ""
        print_info "访问链接:"
        echo "  • 仓库主页: https://github.com/$REPO_PATH"
        echo "  • 当前分支: https://github.com/$REPO_PATH/tree/$BRANCH"
        echo "  • 最新提交: https://github.com/$REPO_PATH/commit/$(git rev-parse HEAD)"
        echo "  • 文件列表: https://github.com/$REPO_PATH/tree/$BRANCH"
        
        echo ""
        print_info "项目包含内容:"
        echo "  ✅ 基础Python示例 (examples/basics/)"
        echo "  ✅ FastAPI Web应用 (examples/intermediate/)"
        echo "  ✅ 报销系统项目 (projects/reimbursement-system/)"
        echo "  ✅ 实用工具函数 (utils/file_utils.py)"
        echo "  ✅ 运行脚本 (scripts/, run.py, start.sh)"
        echo "  ✅ Docker支持 (Dockerfile, docker-compose.yml)"
        echo "  ✅ 虚拟环境管理 (setup_venv.sh)"
        
    else
        print_error "推送失败"
        echo ""
        print_info "可能的原因:"
        echo "  1. SSH密钥未正确配置"
        echo "  2. 网络连接问题"
        echo "  3. 仓库不存在或无权访问"
        echo "  4. 分支冲突"
        echo ""
        print_info "解决方法:"
        echo "  1. 检查SSH配置: ssh -T git@github.com"
        echo "  2. 确认仓库存在: https://github.com/$REPO_PATH"
        echo "  3. 拉取最新代码: git pull origin $BRANCH"
        echo "  4. 解决冲突后重试"
    fi
    echo -e "${BLUE}========================================${NC}"
}

# 运行主函数
main "$@"