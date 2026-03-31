#!/bin/bash
# 使用GitHub Token推送代码

set -e

echo "========================================"
echo "GitHub Token推送脚本"
echo "========================================"

# 检查是否在git仓库中
if [ ! -d ".git" ]; then
    echo "❌ 错误: 当前目录不是git仓库"
    exit 1
fi

# 获取当前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "当前分支: $CURRENT_BRANCH"

# 显示远程仓库
echo -e "\n远程仓库配置:"
git remote -v

# 询问GitHub Token
echo -e "\n请输入GitHub Personal Access Token:"
read -s GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 错误: Token不能为空"
    exit 1
fi

# 获取远程仓库URL
REMOTE_URL=$(git remote get-url origin)
echo -e "\n远程仓库URL: $REMOTE_URL"

# 转换SSH URL为HTTPS URL（如果需要）
if [[ $REMOTE_URL == git@github.com:* ]]; then
    # 从 git@github.com:user/repo.git 转换为 https://github.com/user/repo.git
    REPO_PATH=$(echo $REMOTE_URL | sed 's/git@github.com://' | sed 's/\.git$//')
    HTTPS_URL="https://github.com/$REPO_PATH.git"
    echo "转换为HTTPS URL: $HTTPS_URL"
    
    # 添加带Token的远程仓库
    TOKEN_URL="https://${GITHUB_TOKEN}@github.com/$REPO_PATH.git"
    echo "带Token的URL: https://[TOKEN]@github.com/$REPO_PATH.git"
    
    # 添加临时远程仓库
    git remote add token-origin $TOKEN_URL
    echo "✅ 已添加带Token的远程仓库: token-origin"
    
    PUSH_TARGET="token-origin"
else
    # 已经是HTTPS URL
    if [[ $REMOTE_URL == https://* ]]; then
        # 提取URL部分
        URL_WITHOUT_PROTOCOL=$(echo $REMOTE_URL | sed 's|https://||')
        TOKEN_URL="https://${GITHUB_TOKEN}@$URL_WITHOUT_PROTOCOL"
        echo "带Token的URL: https://[TOKEN]@$(echo $URL_WITHOUT_PROTOCOL | cut -d'@' -f2-)"
        
        # 添加临时远程仓库
        git remote add token-origin $TOKEN_URL
        echo "✅ 已添加带Token的远程仓库: token-origin"
        
        PUSH_TARGET="token-origin"
    else
        echo "❌ 错误: 不支持的远程仓库格式"
        exit 1
    fi
fi

# 显示提交历史
echo -e "\n最近提交:"
git log --oneline -5

# 确认推送
echo -e "\n准备推送到: $PUSH_TARGET/$CURRENT_BRANCH"
read -p "确认推送? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消推送"
    git remote remove token-origin 2>/dev/null || true
    exit 0
fi

# 推送代码
echo -e "\n推送代码..."
if git push $PUSH_TARGET $CURRENT_BRANCH; then
    echo "✅ 推送成功!"
else
    echo "❌ 推送失败"
    
    # 尝试强制推送
    read -p "是否尝试强制推送? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "强制推送..."
        if git push -f $PUSH_TARGET $CURRENT_BRANCH; then
            echo "✅ 强制推送成功!"
        else
            echo "❌ 强制推送失败"
        fi
    fi
fi

# 清理临时远程仓库
echo -e "\n清理临时远程仓库..."
git remote remove token-origin 2>/dev/null || true
echo "✅ 清理完成"

echo -e "\n========================================"
echo "推送完成!"
echo "========================================"

# 显示仓库信息
REPO_NAME=$(basename -s .git $(git config --get remote.origin.url))
echo -e "\n仓库信息:"
echo "  • 仓库: $REPO_NAME"
echo "  • 分支: $CURRENT_BRANCH"
echo "  • 提交: $(git rev-parse --short HEAD)"
echo "  • 文件数: $(git ls-files | wc -l)"
echo "  • 代码行数: $(git ls-files | xargs cat | wc -l)"

# 提供访问链接
if [[ $REMOTE_URL == git@github.com:* ]] || [[ $REMOTE_URL == https://github.com/* ]]; then
    REPO_PATH=$(echo $REMOTE_URL | sed 's/git@github.com://' | sed 's/\.git$//' | sed 's|https://github.com/||')
    echo -e "\n访问链接:"
    echo "  • GitHub: https://github.com/$REPO_PATH"
    echo "  • 分支: https://github.com/$REPO_PATH/tree/$CURRENT_BRANCH"
    echo "  • 提交: https://github.com/$REPO_PATH/commit/$(git rev-parse HEAD)"
fi