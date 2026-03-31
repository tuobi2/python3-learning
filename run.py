#!/usr/bin/env python3
"""
Python3-learning 项目运行脚本

统一运行入口，解决python/python3命令问题。
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_python_command():
    """检查Python命令可用性"""
    python_commands = ['python', 'python3']
    
    for cmd in python_commands:
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return cmd
        except FileNotFoundError:
            continue
    
    return None


def run_example(example_path: str):
    """运行示例文件"""
    python_cmd = check_python_command()
    
    if not python_cmd:
        print("错误: 未找到Python命令!")
        print("请确保已安装Python3，并尝试使用 'python3' 命令")
        return False
    
    example_file = Path(example_path)
    
    if not example_file.exists():
        print(f"错误: 文件不存在 - {example_path}")
        return False
    
    print(f"使用命令: {python_cmd}")
    print(f"运行文件: {example_file}")
    print("=" * 60)
    
    try:
        # 切换到文件所在目录
        original_cwd = os.getcwd()
        os.chdir(example_file.parent)
        
        # 运行Python文件
        result = subprocess.run(
            [python_cmd, example_file.name],
            capture_output=True,
            text=True
        )
        
        # 输出结果
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        
        # 返回原目录
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            print("=" * 60)
            print("✅ 运行成功!")
            return True
        else:
            print("=" * 60)
            print(f"❌ 运行失败 (退出码: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"运行出错: {e}")
        return False


def list_examples():
    """列出所有示例"""
    project_root = Path(__file__).parent
    examples_dir = project_root / "examples"
    
    if not examples_dir.exists():
        print("未找到examples目录!")
        return
    
    print("可用示例:")
    print("=" * 60)
    
    for category_dir in sorted(examples_dir.iterdir()):
        if category_dir.is_dir():
            print(f"\n{category_dir.name.upper()}:")
            print("-" * 40)
            
            for py_file in sorted(category_dir.glob("*.py")):
                # 读取文件描述
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if first_line.startswith('"""') or first_line.startswith("'''"):
                            # 尝试读取文档字符串
                            lines = []
                            for i, line in enumerate(f):
                                if i >= 3:  # 只读几行
                                    break
                                lines.append(line.strip())
                            
                            description = ' '.join(lines).replace('"""', '').replace("'''", '')[:50]
                            if description:
                                print(f"  • {py_file.stem}: {description}...")
                                continue
                except:
                    pass
                
                print(f"  • {py_file.stem}")


def create_wrapper_scripts():
    """创建包装脚本"""
    project_root = Path(__file__).parent
    
    # 创建运行基础示例的脚本
    wrapper_content = '''#!/bin/bash
# 运行Python示例的包装脚本

# 尝试不同的Python命令
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "错误: 未找到Python命令!"
    exit 1
fi

echo "使用命令: $PYTHON_CMD"
echo "运行: $1"
echo ""

$PYTHON_CMD "$@"
'''
    
    wrapper_path = project_root / "run_example.sh"
    with open(wrapper_path, 'w') as f:
        f.write(wrapper_content)
    
    # 设置执行权限
    wrapper_path.chmod(0o755)
    
    print(f"已创建包装脚本: {wrapper_path}")
    print("使用方法: ./run_example.sh <python文件>")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Python3-learning项目运行工具")
    parser.add_argument(
        "file",
        nargs="?",
        help="要运行的Python文件路径"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有示例"
    )
    parser.add_argument(
        "--create-wrappers",
        action="store_true",
        help="创建包装脚本"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="检查Python环境"
    )
    
    args = parser.parse_args()
    
    if args.check:
        python_cmd = check_python_command()
        if python_cmd:
            print(f"✅ 找到Python命令: {python_cmd}")
            subprocess.run([python_cmd, '--version'])
        else:
            print("❌ 未找到Python命令!")
            print("请安装Python3或创建别名:")
            print("  echo 'alias python=\"python3\"' >> ~/.zshrc")
            print("  source ~/.zshrc")
        return
    
    if args.create_wrappers:
        create_wrapper_scripts()
        return
    
    if args.list:
        list_examples()
        return
    
    if args.file:
        success = run_example(args.file)
        sys.exit(0 if success else 1)
    else:
        # 交互模式
        print("Python3-learning项目运行工具")
        print("=" * 60)
        
        while True:
            print("\n选项:")
            print("  1. 运行基础示例")
            print("  2. 运行Web应用示例")
            print("  3. 列出所有示例")
            print("  4. 检查Python环境")
            print("  5. 退出")
            
            try:
                choice = input("\n请选择 (1-5): ").strip()
                
                if choice == "1":
                    run_example("examples/basics/python_fundamentals.py")
                elif choice == "2":
                    run_example("examples/intermediate/fastapi_web_app.py")
                elif choice == "3":
                    list_examples()
                elif choice == "4":
                    python_cmd = check_python_command()
                    if python_cmd:
                        print(f"Python命令: {python_cmd}")
                        subprocess.run([python_cmd, '--version'])
                    else:
                        print("未找到Python命令!")
                elif choice == "5":
                    print("再见!")
                    break
                else:
                    print("无效选择!")
                    
            except KeyboardInterrupt:
                print("\n\n程序被用户中断")
                break
            except Exception as e:
                print(f"错误: {e}")


if __name__ == "__main__":
    main()