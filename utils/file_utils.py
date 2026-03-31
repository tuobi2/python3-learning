#!/usr/bin/env python3
"""
文件操作工具函数

提供常用的文件操作功能，包括：
- 文件读写
- 目录操作
- 文件信息获取
- 文件类型检查
"""

import os
import shutil
import json
import csv
import yaml
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import hashlib


def read_text_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """
    读取文本文件内容
    
    Args:
        file_path: 文件路径
        encoding: 文件编码，默认为utf-8
    
    Returns:
        文件内容字符串
    
    Raises:
        FileNotFoundError: 文件不存在
        IOError: 读取文件失败
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if not file_path.is_file():
        raise IOError(f"路径不是文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                return f.read()
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"无法解码文件: {file_path}")


def write_text_file(
    file_path: Union[str, Path],
    content: str,
    encoding: str = 'utf-8',
    mode: str = 'w'
) -> None:
    """
    写入文本文件
    
    Args:
        file_path: 文件路径
        content: 要写入的内容
        encoding: 文件编码，默认为utf-8
        mode: 写入模式，'w'为覆盖，'a'为追加
    
    Raises:
        IOError: 写入文件失败
    """
    file_path = Path(file_path)
    
    # 确保目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(file_path, mode, encoding=encoding) as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"写入文件失败: {file_path}, 错误: {e}")


def read_json_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> Any:
    """
    读取JSON文件
    
    Args:
        file_path: JSON文件路径
        encoding: 文件编码
    
    Returns:
        JSON解析后的Python对象
    
    Raises:
        FileNotFoundError: 文件不存在
        json.JSONDecodeError: JSON解析错误
    """
    content = read_text_file(file_path, encoding)
    return json.loads(content)


def write_json_file(
    file_path: Union[str, Path],
    data: Any,
    indent: int = 2,
    ensure_ascii: bool = False,
    encoding: str = 'utf-8'
) -> None:
    """
    写入JSON文件
    
    Args:
        file_path: 文件路径
        data: 要写入的数据
        indent: 缩进空格数
        ensure_ascii: 是否确保ASCII编码
        encoding: 文件编码
    """
    json_str = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)
    write_text_file(file_path, json_str, encoding)


def read_csv_file(
    file_path: Union[str, Path],
    encoding: str = 'utf-8',
    delimiter: str = ','
) -> List[Dict[str, str]]:
    """
    读取CSV文件
    
    Args:
        file_path: CSV文件路径
        encoding: 文件编码
        delimiter: 分隔符
    
    Returns:
        字典列表，每行一个字典
    
    Raises:
        FileNotFoundError: 文件不存在
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    data = []
    with open(file_path, 'r', encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            data.append(dict(row))
    
    return data


def write_csv_file(
    file_path: Union[str, Path],
    data: List[Dict[str, Any]],
    fieldnames: Optional[List[str]] = None,
    encoding: str = 'utf-8',
    delimiter: str = ','
) -> None:
    """
    写入CSV文件
    
    Args:
        file_path: 文件路径
        data: 要写入的数据（字典列表）
        fieldnames: 字段名列表，如果为None则使用第一个字典的键
        encoding: 文件编码
        delimiter: 分隔符
    """
    file_path = Path(file_path)
    
    if not data:
        raise ValueError("数据不能为空")
    
    if fieldnames is None:
        fieldnames = list(data[0].keys())
    
    # 确保目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding=encoding, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)


def read_yaml_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> Any:
    """
    读取YAML文件
    
    Args:
        file_path: YAML文件路径
        encoding: 文件编码
    
    Returns:
        YAML解析后的Python对象
    
    Raises:
        FileNotFoundError: 文件不存在
        yaml.YAMLError: YAML解析错误
    """
    try:
        import yaml
    except ImportError:
        raise ImportError("请安装PyYAML: pip install PyYAML")
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    with open(file_path, 'r', encoding=encoding) as f:
        return yaml.safe_load(f)


def write_yaml_file(
    file_path: Union[str, Path],
    data: Any,
    encoding: str = 'utf-8',
    default_flow_style: bool = False
) -> None:
    """
    写入YAML文件
    
    Args:
        file_path: 文件路径
        data: 要写入的数据
        encoding: 文件编码
        default_flow_style: YAML流样式
    """
    try:
        import yaml
    except ImportError:
        raise ImportError("请安装PyYAML: pip install PyYAML")
    
    file_path = Path(file_path)
    
    # 确保目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding=encoding) as f:
        yaml.dump(data, f, default_flow_style=default_flow_style, allow_unicode=True)


def read_pickle_file(file_path: Union[str, Path]) -> Any:
    """
    读取pickle文件
    
    Args:
        file_path: pickle文件路径
    
    Returns:
        反序列化的Python对象
    
    Raises:
        FileNotFoundError: 文件不存在
        pickle.UnpicklingError: 反序列化错误
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    with open(file_path, 'rb') as f:
        return pickle.load(f)


def write_pickle_file(file_path: Union[str, Path], data: Any) -> None:
    """
    写入pickle文件
    
    Args:
        file_path: 文件路径
        data: 要序列化的数据
    """
    file_path = Path(file_path)
    
    # 确保目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)


def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    获取文件详细信息
    
    Args:
        file_path: 文件路径
    
    Returns:
        包含文件信息的字典
    
    Raises:
        FileNotFoundError: 文件不存在
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    stat = file_path.stat()
    
    # 计算文件哈希
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    
    return {
        'path': str(file_path.absolute()),
        'name': file_path.name,
        'stem': file_path.stem,
        'suffix': file_path.suffix,
        'parent': str(file_path.parent),
        'size': stat.st_size,
        'size_human': _format_size(stat.st_size),
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
        'is_file': file_path.is_file(),
        'is_dir': file_path.is_dir(),
        'is_symlink': file_path.is_symlink(),
        'md5_hash': hash_md5.hexdigest(),
        'permissions': oct(stat.st_mode)[-3:],
        'owner': stat.st_uid,
        'group': stat.st_gid,
    }


def _format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def list_files(
    directory: Union[str, Path],
    pattern: str = "*",
    recursive: bool = False,
    include_dirs: bool = False,
    include_files: bool = True
) -> List[Path]:
    """
    列出目录中的文件
    
    Args:
        directory: 目录路径
        pattern: 文件匹配模式，如 "*.py"
        recursive: 是否递归搜索子目录
        include_dirs: 是否包含目录
        include_files: 是否包含文件
    
    Returns:
        文件路径列表
    
    Raises:
        NotADirectoryError: 路径不是目录
    """
    directory = Path(directory)
    
    if not directory.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")
    
    if not directory.is_dir():
        raise NotADirectoryError(f"路径不是目录: {directory}")
    
    if recursive:
        paths = list(directory.rglob(pattern))
    else:
        paths = list(directory.glob(pattern))
    
    # 过滤类型
    filtered_paths = []
    for path in paths:
        if path.is_dir() and include_dirs:
            filtered_paths.append(path)
        elif path.is_file() and include_files:
            filtered_paths.append(path)
    
    return sorted(filtered_paths)


def find_files_by_extension(
    directory: Union[str, Path],
    extensions: List[str],
    recursive: bool = True
) -> List[Path]:
    """
    按扩展名查找文件
    
    Args:
        directory: 目录路径
        extensions: 扩展名列表，如 [".py", ".txt"]
        recursive: 是否递归搜索
    
    Returns:
        匹配的文件路径列表
    """
    directory = Path(directory)
    all_files = []
    
    for ext in extensions:
        pattern = f"*{ext}"
        files = list_files(directory, pattern, recursive, include_dirs=False)
        all_files.extend(files)
    
    return sorted(set(all_files))


def create_directory(directory: Union[str, Path], parents: bool = True) -> Path:
    """
    创建目录
    
    Args:
        directory: 目录路径
        parents: 是否创建父目录
    
    Returns:
        创建的目录路径
    """
    directory = Path(directory)
    directory.mkdir(parents=parents, exist_ok=True)
    return directory


def copy_file(
    source: Union[str, Path],
    destination: Union[str, Path],
    overwrite: bool = False
) -> Path:
    """
    复制文件
    
    Args:
        source: 源文件路径
        destination: 目标文件路径
        overwrite: 是否覆盖已存在的文件
    
    Returns:
        目标文件路径
    
    Raises:
        FileNotFoundError: 源文件不存在
        FileExistsError: 目标文件已存在且不允许覆盖
    """
    source = Path(source)
    destination = Path(destination)
    
    if not source.exists():
        raise FileNotFoundError(f"源文件不存在: {source}")
    
    if destination.exists() and not overwrite:
        raise FileExistsError(f"目标文件已存在: {destination}")
    
    # 确保目标目录存在
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(source, destination)
    return destination


def move_file(
    source: Union[str, Path],
    destination: Union[str, Path],
    overwrite: bool = False
) -> Path:
    """
    移动文件
    
    Args:
        source: 源文件路径
        destination: 目标文件路径
        overwrite: 是否覆盖已存在的文件
    
    Returns:
        目标文件路径
    """
    source = Path(source)
    destination = Path(destination)
    
    if not source.exists():
        raise FileNotFoundError(f"源文件不存在: {source}")
    
    if destination.exists() and not overwrite:
        raise FileExistsError(f"目标文件已存在: {destination}")
    
    # 确保目标目录存在
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.move(source, destination)
    return destination


def delete_file(file_path: Union[str, Path], missing_ok: bool = False) -> None:
    """
    删除文件
    
    Args:
        file_path: 文件路径
        missing_ok: 如果文件不存在是否忽略错误
    """
    file_path = Path(file_path)
    
    try:
        file_path.unlink()
    except FileNotFoundError:
        if not missing_ok:
            raise


def delete_directory(
    directory: Union[str, Path],
    recursive: bool = False,
    missing_ok: bool = False
) -> None:
    """
    删除目录
    
    Args:
        directory: 目录路径
        recursive: 是否递归删除
        missing_ok: 如果目录不存在是否忽略错误
    """
    directory = Path(directory)
    
    if recursive:
        try:
            shutil.rmtree(directory)
        except FileNotFoundError:
            if not missing_ok:
                raise
    else:
        try:
            directory.rmdir()
        except FileNotFoundError:
            if not missing_ok:
                raise


def get_file_line_count(file_path: Union[str, Path]) -> int:
    """
    获取文件行数
    
    Args:
        file_path: 文件路径
    
    Returns:
        文件行数
    
    Raises:
        FileNotFoundError: 文件不存在
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    count = 0
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for _ in f:
            count += 1
    
    return count


def search_in_file(
    file_path: Union[str, Path],
    search_text: str,
    case_sensitive: bool = False,
    encoding: str = 'utf-8'
) -> List[Dict[str, Any]]:
    """
    在文件中搜索文本
    
    Args:
        file_path: 文件路径
        search_text: 搜索文本
        case_sensitive: 是否区分大小写
        encoding: 文件编码
    
    Returns:
        匹配行信息列表
    
    Raises:
        FileNotFoundError: 文件不存在
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if not case_sensitive:
        search_text = search_text.lower()
    
    matches = []
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            line_content = line.rstrip('\n')
            
            if not case_sensitive:
                line_check = line_content.lower()
            else:
                line_check = line_content
            
            if search_text in line_check:
                matches.append({
                    'line_number': line_num,
                    'content': line_content,
                    'start_position': line_check.find(search_text),
                    'end_position': line_check.find(search_text) + len(search_text)
                })
    
    return matches


def backup_file(
    file_path: Union[str, Path],
    backup_dir: Optional[Union[str, Path]] = None,
    suffix: str = ".bak"
) -> Path:
    """
    备份文件
    
    Args:
        file_path: 要备份的文件路径
        backup_dir: 备份目录，如果为None则在原目录备份
        suffix: 备份文件后缀
    
    Returns:
        备份文件路径
    
    Raises:
        FileNotFoundError: 源文件不存在
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if backup_dir is None:
        backup_dir = file_path.parent
    
    backup_dir = Path(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{timestamp}{suffix}"
    backup_path = backup_dir / backup_name
    
    copy_file(file_path, backup_path, overwrite=True)
    return backup_path


# 示例使用
if __name__ == "__main__":
