#!/bin/bash
# 使用GitHub API推送（备用方案）

set -e

echo "========================================"
echo "GitHub API推送 - 备用方案"
echo "========================================"

# 检查git仓库
if [ ! -d ".git" ]; then
    echo "❌ 错误: 当前目录不是git仓库"
    exit 1
fi

# 获取仓库信息
REPO_URL=$(git config --get remote.origin.url)
if [[ $REPO_URL == git@github.com:* ]]; then
    REPO_PATH=$(echo $REPO_URL | sed 's/git@github.com://' | sed 's/\.git$//')
    OWNER=$(echo $REPO_PATH | cut -d'/' -f1)
    REPO=$(echo $REPO_PATH | cut -d'/' -f2)
elif [[ $REPO_URL == https://github.com/* ]]; then
    REPO_PATH=$(echo $REPO_URL | sed 's|https://github.com/||' | sed 's/\.git$//')
    OWNER=$(echo $REPO_PATH | cut -d'/' -f1)
    REPO=$(echo $REPO_PATH | cut -d'/' -f2)
else
    echo "❌ 错误: 不支持的仓库URL格式"
    exit 1
fi

echo "仓库: $OWNER/$REPO"
echo "分支: $(git branch --show-current)"

# 输入Token
echo ""
echo "请输入GitHub Personal Access Token (需要repo权限):"
read -s GITHUB_TOKEN
echo

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 错误: Token不能为空"
    exit 1
fi

# 方法1: 使用git直接推送（推荐）
echo ""
echo "方法1: 使用git直接推送"
echo "----------------------------------------"

TOKEN_URL="https://${GITHUB_TOKEN}@github.com/${OWNER}/${REPO}.git"
ORIGINAL_URL=$REPO_URL

# 临时修改URL
git remote set-url origin "$TOKEN_URL"

echo "推送中..."
if git push origin main; then
    echo "✅ 推送成功!"
else
    echo "❌ 推送失败，尝试方法2..."
    
    # 方法2: 创建新的提交通过API
    echo ""
    echo "方法2: 通过GitHub API创建提交"
    echo "----------------------------------------"
    
    # 获取当前提交的SHA
    CURRENT_SHA=$(git rev-parse HEAD)
    echo "当前提交SHA: $CURRENT_SHA"
    
    # 创建新的tree
    echo "创建文件树..."
    # 这里可以扩展为通过API创建提交
    echo "⚠️  API方法需要更多实现，建议使用方法1"
fi

# 恢复原始URL
git remote set-url origin "$ORIGINAL_URL"
echo "✅ 恢复原始URL"

echo ""
echo "========================================"
echo "完成!"
echo "========================================"