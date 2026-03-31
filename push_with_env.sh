#!/bin/bash
# 使用环境变量推送GitHub

set -e

echo "========================================"
echo "GitHub推送 - 环境变量版"
echo "========================================"

# 加载环境变量
if [ -f ".env" ]; then
    echo "加载 .env 文件..."
    source .env
else
    echo "⚠️  未找到 .env 文件"
    echo "请创建 .env 文件或手动输入Token"
fi

# 检查必要变量
if [ -z "$GITHUB_TOKEN" ]; then
    echo "请输入GitHub Personal Access Token:"
    read -s GITHUB_TOKEN
    echo
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 错误: GITHUB_TOKEN不能为空"
    exit 1
fi

# 获取仓库信息
REPO_URL=$(git config --get remote.origin.url)
if [ -z "$REPO_URL" ]; then
    echo "❌ 错误: 未配置远程仓库"
    exit 1
fi

# 提取仓库路径
if [[ $REPO_URL == git@github.com:* ]]; then
    REPO_PATH=$(echo $REPO_URL | sed 's/git@github.com://' | sed 's/\.git$//')
elif [[ $REPO_URL == https://github.com/* ]]; then
    REPO_PATH=$(echo $REPO_URL | sed 's|https://github.com/||' | sed 's/\.git$//')
else
    echo "❌ 错误: 不支持的仓库URL格式"
    exit 1
fi

echo "仓库: $REPO_PATH"
echo "分支: $(git branch --show-current)"

# 显示待推送的提交
echo ""
echo "待推送的提交:"
git log --oneline origin/main..HEAD 2>/dev/null || git log --oneline -5
echo ""

# 确认推送
read -p "确认推送到GitHub? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消推送"
    exit 0
fi

# 使用Token推送
echo "使用Token推送..."
TOKEN_URL="https://${GITHUB_TOKEN}@github.com/${REPO_PATH}.git"

# 保存原始URL
ORIGINAL_URL=$REPO_URL

# 临时修改URL
git remote set-url origin $TOKEN_URL

# 推送
echo "推送中..."
if git push origin main; then
    echo "✅ 推送成功!"
    SUCCESS=true
else
    echo "❌ 推送失败"
    SUCCESS=false
fi

# 恢复原始URL
git remote set-url origin $ORIGINAL_URL
echo "✅ 恢复原始URL"

# 显示结果
echo ""
echo "========================================"
if [ "$SUCCESS" = true ]; then
    echo "🎉 推送完成!"
else
    echo "推送失败，请检查:"
    echo "1. Token是否有 repo 权限"
    echo "2. 网络连接"
    echo "3. 仓库是否存在"
fi
echo "========================================"

if [ "$SUCCESS" = true ]; then
    echo ""
    echo "访问链接:"
    echo "  • 仓库: https://github.com/$REPO_PATH"
    echo "  • 提交: https://github.com/$REPO_PATH/commit/$(git rev-parse HEAD)"
    
    # 统计信息
    echo ""
    echo "项目统计:"
    echo "  • Python文件: $(find . -name "*.py" -type f | grep -v __pycache__ | wc -l)"
    echo "  • 总文件数: $(git ls-files | wc -l)"
    echo "  • 代码行数: $(git ls-files | xargs cat | wc -l)"
fi