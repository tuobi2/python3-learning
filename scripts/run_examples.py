#!/usr/bin/env python3
"""
运行所有Python示例的脚本
"""

import subprocess
import sys
import os

def run_demo(filename):
    """运行单个Python示例文件"""
    print(f"\n{'='*60}")
    print(f"运行: {filename}")
    print('='*60)
    
    try:
        # 读取文件内容预览
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            print(f"文件大小: {len(content)} 字符, {len(lines)} 行")
            
            # 显示前10行
            print("\n代码预览 (前10行):")
            for i, line in enumerate(lines[:10]):
                print(f"{i+1:3}: {line}")
            
            if len(lines) > 10:
                print(f"... 还有 {len(lines)-10} 行")
    
    except Exception as e:
        print(f"读取文件失败: {e}")
        return False
    
    return True

def main():
    # 检查当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"当前目录: {current_dir}")
    
    # 要运行的示例文件
    demo_files = ['demo.py', 'demo2.py', 'demo3.py']
    
    # 检查文件是否存在
    existing_files = []
    for f in demo_files:
        if os.path.exists(f):
            existing_files.append(f)
        else:
            print(f"警告: 文件 {f} 不存在")
    
    if not existing_files:
        print("没有找到示例文件")
        return
    
    print(f"\n找到 {len(existing_files)} 个示例文件:")
    for f in existing_files:
        print(f"  - {f}")
    
    # 运行每个示例
    for demo_file in existing_files:
        success = run_demo(demo_file)
        
        if success:
            # 询问是否要实际运行
            choice = input(f"\n是否要运行 {demo_file}？(y/n): ").strip().lower()
            if choice == 'y':
                try:
                    print(f"\n执行 {demo_file}...")
                    result = subprocess.run([sys.executable, demo_file], 
                                          capture_output=True, text=True, timeout=10)
                    print("输出:")
                    print(result.stdout)
                    if result.stderr:
                        print("错误:")
                        print(result.stderr)
                except subprocess.TimeoutExpired:
                    print("执行超时")
                except Exception as e:
                    print(f"执行失败: {e}")
        
        print("\n" + "="*60)
    
    print("\n所有示例检查完成！")

if __name__ == "__main__":
    main()