#!/usr/bin/env python3
"""
检查Python版本兼容性
"""

import sys
import platform

def check_python_version():
    """检查Python版本"""
    print("=" * 60)
    print("Python版本兼容性检查")
    print("=" * 60)
    
    # 获取Python版本信息
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"当前Python版本: {version_str}")
    print(f"平台: {platform.platform()}")
    print(f"Python实现: {platform.python_implementation()}")
    print(f"构建信息: {platform.python_build()}")
    
    # 检查版本兼容性
    print("\n" + "=" * 60)
    print("版本兼容性检查")
    print("=" * 60)
    
    # 项目支持的Python版本
    supported_versions = [(3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14)]
    
    current_major_minor = (version.major, version.minor)
    
    if current_major_minor in supported_versions:
        print(f"✅ 当前Python版本 {version_str} 在支持列表中")
    else:
        print(f"⚠️  当前Python版本 {version_str} 不在官方支持列表中")
        print(f"   项目官方支持: {', '.join([f'{m}.{n}' for m, n in supported_versions])}")
    
    # 检查Python 3.14特定问题
    if version.major == 3 and version.minor == 14:
        print("\n" + "=" * 60)
        print("Python 3.14 注意事项")
        print("=" * 60)
        print("⚠️  Python 3.14 是最新版本，可能:")
        print("   • 某些依赖包可能尚未完全兼容")
        print("   • GitHub Actions可能不支持此版本")
        print("   • 建议使用 Python 3.9-3.12 进行开发")
    
    # 检查pip版本
    print("\n" + "=" * 60)
    print("pip和包管理检查")
    print("=" * 60)
    
    try:
        import pip
        pip_version = pip.__version__
        print(f"pip版本: {pip_version}")
        
        # 检查pip是否过旧
        major, minor, _ = map(int, pip_version.split('.')[:3])
        if major < 20 or (major == 20 and minor < 3):
            print("⚠️  pip版本较旧，建议升级: python -m pip install --upgrade pip")
        else:
            print("✅ pip版本较新")
            
    except ImportError:
        print("❌ 无法导入pip")
    
    # 检查关键依赖
    print("\n" + "=" * 60)
    print("关键依赖检查")
    print("=" * 60)
    
    dependencies = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "requests",
        "pytest",
        "black",
        "flake8",
        "mypy",
    ]
    
    for dep in dependencies:
        try:
            module = __import__(dep)
            version = getattr(module, '__version__', '未知版本')
            print(f"✅ {dep}: {version}")
        except ImportError:
            print(f"❌ {dep}: 未安装")
    
    # 建议
    print("\n" + "=" * 60)
    print("建议")
    print("=" * 60)
    
    if version.major == 3 and version.minor >= 13:
        print("1. 对于生产环境，建议使用 Python 3.9-3.12 LTS版本")
        print("2. 对于开发环境，可以继续使用 Python 3.14")
        print("3. 如果遇到依赖问题，尝试:")
        print("   • 使用虚拟环境: python -m venv venv")
        print("   • 安装指定版本: pip install 'package==version'")
        print("   • 检查包兼容性: https://pypi.org/project/package/")
    else:
        print("1. 当前Python版本适合开发")
        print("2. 确保使用虚拟环境隔离项目")
        print("3. 定期更新依赖: pip install --upgrade -r requirements.txt")
    
    print("\n" + "=" * 60)
    print("GitHub Actions配置")
    print("=" * 60)
    print("项目配置了以下Python版本测试:")
    print("  • Python 3.9, 3.10, 3.11, 3.12")
    print("访问: https://github.com/tuobi2/python3-learning/actions")
    
    return 0

if __name__ == "__main__":
    sys.exit(check_python_version())