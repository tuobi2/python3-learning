#!/bin/bash
# GitHub推送脚本 - SSH版

set -e

echo "========================================"
echo "GitHub推送工具 (SSH版)"
echo "========================================"

# 检查git仓库
if [ ! -d ".git" ]; then
    echo "❌ 错误: 当前目录不是git仓库"
    exit 1
fi

# 检查SSH配置
echo "检查SSH认证..."
if ! ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "❌ SSH认证失败"
    echo ""
    echo "请先设置SSH密钥:"
    echo "  1. 生成SSH密钥: ssh-keygen -t ed25519 -C \"your_email@example.com\""
    echo "  2. 添加到GitHub: https://github.com/settings/keys"
    echo "  3. 测试连接: ssh -T git@github.com"
    exit 1
fi

echo "✅ SSH认证成功"

# 显示项目信息
REPO_URL=$(git config --get remote.origin.url)
BRANCH=$(git branch --show-current)
COMMIT_HASH=$(git rev-parse --short HEAD)

echo ""
echo "项目信息:"
echo "  • 仓库: $(basename -s .git $REPO_URL)"
echo "  • 分支: $BRANCH"
echo "  • 最新提交: $COMMIT_HASH"

# 显示待推送内容
echo ""
echo "待推送的更改:"
git status --short

echo ""
echo "最近提交:"
git log --oneline -3

# 确认推送
echo ""
read -p "确认推送到GitHub? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消推送"
    exit 0
fi

# 推送
echo "推送中..."
if git push origin $BRANCH; then
    echo "✅ 推送成功!"
    
    # 显示结果
    echo ""
    echo "========================================"
    echo "🎉 项目已成功推送到GitHub!"
    echo "========================================"
    
    # 提取仓库路径
    if [[ $REPO_URL == git@github.com:* ]]; then
        REPO_PATH=$(echo $REPO_URL | sed 's/git@github.com://' | sed 's/\.git$//')
    elif [[ $REPO_URL == https://github.com/* ]]; then
        REPO_PATH=$(echo $REPO_URL | sed 's|https://github.com/||' | sed 's/\.git$//')
    fi
    
    echo ""
    echo "访问链接:"
    echo "  • 仓库: https://github.com/$REPO_PATH"
    echo "  • 分支: https://github.com/$REPO_PATH/tree/$BRANCH"
    echo "  • 提交: https://github.com/$REPO_PATH/commit/$COMMIT_HASH"
    
    echo ""
    echo "项目统计:"
    echo "  • 文件数: $(git ls-files | wc -l)"
    echo "  • Python文件: $(find . -name "*.py" -type f | grep -v __pycache__ | wc -l)"
    echo "  • 提交数: $(git log --oneline | wc -l)"
    
else
    echo "❌ 推送失败"
    
    # 尝试强制推送
    read -p "是否尝试强制推送? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "强制推送..."
        if git push -f origin $BRANCH; then
            echo "✅ 强制推送成功!"
        else
            echo "❌ 强制推送失败"
        fi
    fi
fi
