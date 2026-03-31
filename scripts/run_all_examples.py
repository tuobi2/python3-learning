#!/usr/bin/env python3
"""
运行所有Python示例的脚本

这个脚本可以运行项目中的所有Python示例，方便学习和测试。
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import importlib.util


def setup_environment():
    """设置Python路径"""
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # 添加示例目录到路径
    examples_dir = project_root / "examples"
    if examples_dir.exists():
        sys.path.insert(0, str(examples_dir))
    
    return project_root


def find_python_files(directory: Path, recursive: bool = True) -> List[Path]:
    """查找目录中的所有Python文件"""
    python_files = []
    
    if recursive:
        pattern = "**/*.py"
    else:
        pattern = "*.py"
    
    for py_file in directory.glob(pattern):
        # 排除__pycache__和测试文件
        if "__pycache__" not in str(py_file) and "test_" not in py_file.name:
            python_files.append(py_file)
    
    return sorted(python_files)


def get_example_categories(project_root: Path) -> Dict[str, List[Path]]:
    """获取示例分类"""
    examples_dir = project_root / "examples"
    
    if not examples_dir.exists():
        return {}
    
    categories = {}
    
    for category_dir in examples_dir.iterdir():
        if category_dir.is_dir():
            category_name = category_dir.name
            python_files = find_python_files(category_dir, recursive=False)
            
            if python_files:
                categories[category_name] = python_files
    
    return categories


def print_example_info(file_path: Path) -> None:
    """打印示例文件信息"""
    print(f"\n{'='*60}")
    print(f"文件: {file_path.name}")
    print(f"路径: {file_path.relative_to(file_path.parent.parent.parent)}")
    print('='*60)
    
    # 读取文件前几行获取描述
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = []
            for i, line in enumerate(f):
                if i >= 20:  # 只读取前20行
                    break
                lines.append(line.rstrip())
            
            # 查找文档字符串
            in_docstring = False
            docstring_lines = []
            
            for line in lines:
                if '"""' in line or "'''" in line:
                    if not in_docstring:
                        in_docstring = True
                        # 移除引号
                        clean_line = line.replace('"""', '').replace("'''", '').strip()
                        if clean_line:
                            docstring_lines.append(clean_line)
                    else:
                        in_docstring = False
                        break
                elif in_docstring:
                    docstring_lines.append(line.strip())
            
            if docstring_lines:
                print("\n描述:")
                for doc_line in docstring_lines:
                    if doc_line:
                        print(f"  {doc_line}")
            
            # 显示文件统计
            line_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8'))
            print(f"\n统计: {line_count} 行代码")
            
    except Exception as e:
        print(f"读取文件信息失败: {e}")


def run_python_file(file_path: Path, timeout: int = 30) -> bool:
    """运行Python文件"""
    print(f"\n{'='*60}")
    print(f"运行: {file_path.name}")
    print('='*60)
    
    try:
        # 使用subprocess运行，这样可以捕获输出和控制超时
        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=file_path.parent
        )
        
        if result.stdout:
            print("输出:")
            print(result.stdout)
        
        if result.stderr:
            print("错误:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"\n✅ 运行成功!")
            return True
        else:
            print(f"\n❌ 运行失败 (退出码: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n⏰ 运行超时 ({timeout}秒)")
        return False
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        return False


def run_examples_interactive(categories: Dict[str, List[Path]]) -> None:
    """交互式运行示例"""
    print("\n" + "="*60)
    print("Python3 Learning Examples - 交互式运行器")
    print("="*60)
    
    while True:
        print("\n可用分类:")
        for i, category in enumerate(sorted(categories.keys()), 1):
            file_count = len(categories[category])
            print(f"  {i}. {category} ({file_count}个示例)")
        
        print(f"  {len(categories) + 1}. 运行所有示例")
        print(f"  {len(categories) + 2}. 退出")
        
        try:
            choice = input("\n请选择分类编号: ").strip()
            
            if choice == str(len(categories) + 2):
                print("再见!")
                break
            elif choice == str(len(categories) + 1):
                # 运行所有示例
                run_all_examples(categories)
            elif choice.isdigit() and 1 <= int(choice) <= len(categories):
                category_idx = int(choice) - 1
                category_name = sorted(categories.keys())[category_idx]
                run_category_examples(category_name, categories[category_name])
            else:
                print("无效选择，请重试")
                
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"错误: {e}")


def run_category_examples(category_name: str, files: List[Path]) -> None:
    """运行特定分类的示例"""
    print(f"\n{'='*60}")
    print(f"分类: {category_name}")
    print('='*60)
    
    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] ", end="")
        print_example_info(file_path)
        
        choice = input(f"\n是否运行此示例? (y/n/s=跳过剩余/q=退出): ").lower().strip()
        
        if choice == 'q':
            print("退出当前分类")
            break
        elif choice == 's':
            print("跳过剩余示例")
            break
        elif choice == 'y':
            success = run_python_file(file_path)
            if not success:
                retry = input("运行失败，是否重试? (y/n): ").lower().strip()
                if retry == 'y':
                    run_python_file(file_path)
        
        # 如果不是最后一个文件，询问是否继续
        if i < len(files) and choice != 's':
            cont = input(f"\n继续下一个示例? (y/n): ").lower().strip()
            if cont != 'y':
                break


def run_all_examples(categories: Dict[str, List[Path]]) -> None:
    """运行所有示例"""
    print(f"\n{'='*60}")
    print("运行所有示例")
    print('='*60)
    
    total_files = sum(len(files) for files in categories.values())
    file_count = 0
    success_count = 0
    
    for category_name in sorted(categories.keys()):
        files = categories[category_name]
        
        print(f"\n{'='*60}")
        print(f"分类: {category_name} ({len(files)}个示例)")
        print('='*60)
        
        for file_path in files:
            file_count += 1
            print(f"\n[{file_count}/{total_files}] {file_path.name}")
            
            try:
                success = run_python_file(file_path)
                if success:
                    success_count += 1
            except Exception as e:
                print(f"运行出错: {e}")
            
            # 如果不是最后一个文件，添加短暂暂停
            if file_count < total_files:
                import time
                time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print("运行完成!")
    print(f"总计: {total_files} 个示例")
    print(f"成功: {success_count}")
    print(f"失败: {total_files - success_count}")
    print('='*60)


def create_example_index(categories: Dict[str, List[Path]], output_file: Path) -> None:
    """创建示例索引文件"""
    print(f"\n创建示例索引: {output_file}")
    
    index_content = "# Python3 Learning Examples Index\n\n"
    
    for category_name in sorted(categories.keys()):
        files = categories[category_name]
        index_content += f"## {category_name.capitalize()} Examples\n\n"
        
        for file_path in files:
            # 读取文件描述
            description = get_file_description(file_path)
            
            relative_path = file_path.relative_to(output_file.parent)
            index_content += f"### {file_path.stem}\n"
            index_content += f"- **文件**: `{relative_path}`\n"
            if description:
                index_content += f"- **描述**: {description}\n"
            
            # 获取文件统计
            try:
                line_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8'))
                index_content += f"- **行数**: {line_count}\n"
            except:
                pass
            
            index_content += "\n"
    
    # 写入文件
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"索引已保存到: {output_file}")


def get_file_description(file_path: Path) -> Optional[str]:
    """获取文件描述（从文档字符串）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 查找模块级文档字符串
            import ast
            tree = ast.parse(content)
            
            if isinstance(tree, ast.Module) and tree.body:
                first_node = tree.body[0]
                if isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Constant):
                    docstring = first_node.value.value
                    if isinstance(docstring, str):
                        # 取第一行作为简短描述
                        first_line = docstring.strip().split('\n')[0]
                        return first_line.strip('"\'')
    
    except:
        pass
    
    return None


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="运行Python3学习示例")
    parser.add_argument(
        "--category",
        choices=['basics', 'intermediate', 'advanced', 'web'],
        help="运行特定分类的示例"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="运行所有示例"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有示例"
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="创建示例索引文件"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="交互式运行模式"
    )
    
    args = parser.parse_args()
    
    # 设置环境
    project_root = setup_environment()
    
    # 获取示例分类
    categories = get_example_categories(project_root)
    
    if not categories:
        print("未找到示例文件!")
        return
    
    if args.list:
        print("\n可用示例:")
        print("="*60)
        for category_name in sorted(categories.keys()):
            files = categories[category_name]
            print(f"\n{category_name.upper()} ({len(files)}个):")
            for file_path in files:
                description = get_file_description(file_path)
                if description:
                    print(f"  • {file_path.stem}: {description}")
                else:
                    print(f"  • {file_path.stem}")
        return
    
    if args.index:
        index_file = project_root / "docs" / "examples_index.md"
        create_example_index(categories, index_file)
        return
    
    if args.interactive:
        run_examples_interactive(categories)
        return
    
    if args.category:
        if args.category in categories:
            run_category_examples(args.category, categories[args.category])
        else:
            print(f"分类 '{args.category}' 不存在!")
            print(f"可用分类: {', '.join(categories.keys())}")
    elif args.all:
        run_all_examples(categories)
    else:
        # 默认交互模式
        run_examples_interactive(categories)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"程序出错: {e}")
        import traceback
        traceback.print_exc()