#!/bin/bash
# 简单的GitHub Token推送脚本

set -e

echo "========================================"
echo "GitHub Token推送 - 简单版"
echo "========================================"

# 检查git仓库
if [ ! -d ".git" ]; then
    echo "❌ 错误: 当前目录不是git仓库"
    exit 1
fi

# 显示当前状态
echo "仓库: $(basename -s .git $(git config --get remote.origin.url))"
echo "分支: $(git branch --show-current)"
echo "提交: $(git rev-parse --short HEAD)"
echo ""

# 显示最近提交
echo "最近提交:"
git log --oneline -3
echo ""

# 方法1: 使用临时URL推送
echo "方法1: 使用临时URL推送"
echo "----------------------------------------"

# 获取原始URL
ORIGINAL_URL=$(git config --get remote.origin.url)
echo "原始URL: $ORIGINAL_URL"

# 转换为HTTPS格式
if [[ $ORIGINAL_URL == git@github.com:* ]]; then
    # git@github.com:user/repo.git -> https://github.com/user/repo.git
    REPO_PATH=$(echo $ORIGINAL_URL | sed 's/git@github.com://' | sed 's/\.git$//')
    HTTPS_URL="https://github.com/$REPO_PATH.git"
    echo "HTTPS URL: $HTTPS_URL"
else
    HTTPS_URL=$ORIGINAL_URL
fi

# 输入Token
echo ""
echo "请输入GitHub Personal Access Token:"
echo "(Token需要 repo 权限)"
read -s GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 错误: Token不能为空"
    exit 1
fi

# 创建带Token的URL
TOKEN_URL="https://${GITHUB_TOKEN}@github.com/$REPO_PATH.git"
echo ""
echo "带Token的URL: https://[TOKEN_HIDDEN]@github.com/$REPO_PATH.git"

# 临时修改远程URL
echo ""
echo "临时修改远程URL..."
git remote set-url origin $TOKEN_URL

# 推送
echo "推送代码..."
if git push origin main; then
    echo "✅ 推送成功!"
else
    echo "❌ 推送失败"
    
    # 尝试强制推送
    read -p "是否尝试强制推送? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "强制推送..."
        if git push -f origin main; then
            echo "✅ 强制推送成功!"
        else
            echo "❌ 强制推送失败"
        fi
    fi
fi

# 恢复原始URL
echo ""
echo "恢复原始URL..."
git remote set-url origin $ORIGINAL_URL
echo "✅ URL已恢复"

echo ""
echo "========================================"
echo "推送完成!"
echo "========================================"

# 显示结果
echo ""
echo "仓库信息:"
echo "  • 名称: $REPO_PATH"
echo "  • 分支: main"
echo "  • 最新提交: $(git log --oneline -1 --format="%h %s")"
echo ""
echo "访问链接:"
echo "  • GitHub: https://github.com/$REPO_PATH"
echo "  • 分支: https://github.com/$REPO_PATH/tree/main"
echo "  • 提交: https://github.com/$REPO_PATH/commit/$(git rev-parse HEAD)"