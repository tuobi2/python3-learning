#!/bin/bash
# SSH推送脚本 - 简洁版

set -e

echo "🔐 GitHub SSH推送"
echo "========================"

# 检查SSH
if ! ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "❌ SSH未配置"
    echo "请运行: ssh-keygen -t ed25519 -C \"your_email@example.com\""
    echo "然后添加公钥到: https://github.com/settings/keys"
    exit 1
fi

echo "✅ SSH已就绪"

# 推送
BRANCH=$(git branch --show-current)
echo "推送分支: $BRANCH"

if git push origin $BRANCH; then
    echo "✅ 推送完成"
    REPO_URL=$(git config --get remote.origin.url)
    if [[ $REPO_URL == git@github.com:* ]]; then
        REPO_PATH=$(echo $REPO_URL | sed 's/git@github.com://' | sed 's/\.git$//')
        echo "🔗 https://github.com/$REPO_PATH"
    fi
else
    echo "❌ 推送失败"
    exit 1
fi