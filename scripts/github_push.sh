#!/bin/bash
# python3-learning项目推送脚本

echo "=== python3-learning项目推送 ==="
echo "目标仓库: tuobi2/python3-learning"
echo ""

cd /Users/lijiepeng/python3 || { echo "错误: 无法进入python3目录"; exit 1; }

# 显示当前状态
echo "1. 本地仓库状态:"
echo "   分支: $(git branch --show-current)"
echo "   提交: $(git log --oneline -2)"
echo "   文件: $(git ls-files | wc -l) 个"
echo ""

# 检查远程配置
echo "2. 远程配置:"
git remote -v
echo ""

# 检查SSH连接
echo "3. 检查GitHub连接..."
ssh -T git@github.com 2>&1 | grep "successfully authenticated"
if [ $? -eq 0 ]; then
    echo "   ✅ SSH认证成功"
else
    echo "   ❌ SSH认证失败"
    echo "   请确保:"
    echo "   1. SSH密钥已添加到GitHub"
    echo "   2. SSH配置正确"
    exit 1
fi

# 推送选项
echo ""
echo "4. 推送选项:"
echo "   a) 创建新仓库并推送 (如果GitHub上不存在)"
echo "   b) 推送到现有仓库"
echo "   c) 强制推送 (覆盖远程)"
read -p "   请选择 (a/b/c): " choice

case $choice in
    a)
        echo "创建新仓库..."
        echo "请先在GitHub创建仓库: https://github.com/new"
        echo "仓库名: python3-learning"
        echo "描述: Python3学习项目和报销系统"
        echo "不要初始化README、.gitignore、license"
        echo ""
        read -p "仓库已创建？(y/n): " created
        if [ "$created" = "y" ]; then
            git remote add origin git@github.com:tuobi2/python3-learning.git
            git push -u origin main
        else
            echo "请先创建GitHub仓库"
            exit 1
        fi
        ;;
    b)
        echo "推送到现有仓库..."
        git push -u origin main
        ;;
    c)
        echo "强制推送..."
        git push -f origin main
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

# 验证结果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo "   仓库地址: https://github.com/tuobi2/python3-learning"
    echo ""
    echo "   最终状态:"
    git remote -v
    git log --oneline -3
else
    echo ""
    echo "❌ 推送失败"
    echo "   可能原因:"
    echo "   1. 仓库不存在 - 需要先创建"
    echo "   2. 权限不足 - 确认仓库访问权限"
    echo "   3. 网络问题 - 检查网络连接"
fi

echo ""
echo "=== 完成 ==="