#!/usr/bin/env python3
"""
文件工具函数测试
"""

import pytest
import sys
import os
import tempfile
import json
import csv
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    from utils import file_utils
    HAS_FILE_UTILS = True
except ImportError:
    HAS_FILE_UTILS = False
    pytest.skip("file_utils模块未找到", allow_module_level=True)


class TestFileUtils:
    """测试文件工具函数"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.txt")
    
    def teardown_method(self):
        """每个测试方法后的清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_read_write_text_file(self):
        """测试文本文件读写"""
        # 测试数据
        test_content = "Hello, World!\n这是一行中文文本。\nThird line."
        
        # 写入文件
        file_utils.write_text_file(self.test_file, test_content)
        assert os.path.exists(self.test_file)
        
        # 读取文件
        content = file_utils.read_text_file(self.test_file)
        assert content == test_content
        
        # 测试追加模式
        additional_content = "\n这是追加的内容。"
        file_utils.write_text_file(self.test_file, additional_content, mode='a')
        full_content = file_utils.read_text_file(self.test_file)
        assert full_content == test_content + additional_content
    
    def test_read_write_json_file(self):
        """测试JSON文件读写"""
        # 测试数据
        test_data = {
            "name": "张三",
            "age": 25,
            "skills": ["Python", "JavaScript", "SQL"],
            "address": {
                "city": "北京",
                "district": "海淀区"
            }
        }
        
        json_file = os.path.join(self.temp_dir, "test.json")
        
        # 写入JSON文件
        file_utils.write_json_file(json_file, test_data)
        assert os.path.exists(json_file)
        
        # 读取JSON文件
        data = file_utils.read_json_file(json_file)
        assert data == test_data
        
        # 测试缩进
        file_utils.write_json_file(json_file, test_data, indent=4)
        with open(json_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # 检查是否有缩进
            assert any('    ' in line for line in lines)
    
    def test_read_write_csv_file(self):
        """测试CSV文件读写"""
        # 测试数据
        test_data = [
            {"name": "张三", "age": "25", "city": "北京"},
            {"name": "李四", "age": "30", "city": "上海"},
            {"name": "王五", "age": "28", "city": "广州"}
        ]
        
        csv_file = os.path.join(self.temp_dir, "test.csv")
        
        # 写入CSV文件
        file_utils.write_csv_file(csv_file, test_data)
        assert os.path.exists(csv_file)
        
        # 读取CSV文件
        data = file_utils.read_csv_file(csv_file)
        assert len(data) == 3
        assert data[0]["name"] == "张三"
        assert data[1]["city"] == "上海"
        
        # 测试自定义分隔符
        tsv_file = os.path.join(self.temp_dir, "test.tsv")
        file_utils.write_csv_file(tsv_file, test_data, delimiter='\t')
        
        with open(tsv_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert '\t' in content  # 检查是否使用制表符分隔
    
    def test_file_info(self):
        """测试文件信息获取"""
        # 创建测试文件
        test_content = "测试文件内容"
        file_utils.write_text_file(self.test_file, test_content)
        
        # 获取文件信息
        info = file_utils.get_file_info(self.test_file)
        
        # 检查基本信息
        assert info["path"] == os.path.abspath(self.test_file)
        assert info["name"] == "test.txt"
        assert info["stem"] == "test"
        assert info["suffix"] == ".txt"
        assert info["is_file"] is True
        assert info["is_dir"] is False
        
        # 检查文件大小
        assert info["size"] == len(test_content.encode('utf-8'))
        assert "KB" in info["size_human"] or "B" in info["size_human"]
        
        # 检查时间戳
        assert "created" in info
        assert "modified" in info
        assert "accessed" in info
        
        # 检查哈希值
        assert len(info["md5_hash"]) == 32  # MD5哈希是32位十六进制
    
    def test_list_files(self):
        """测试文件列表"""
        # 创建测试文件
        files_to_create = ["test1.py", "test2.txt", "test3.json", "subdir/test4.py"]
        
        for file_name in files_to_create:
            file_path = os.path.join(self.temp_dir, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file_utils.write_text_file(file_path, "content")
        
        # 测试非递归列表
        files = file_utils.list_files(self.temp_dir, recursive=False)
        file_names = [f.name for f in files]
        assert "test1.py" in file_names
        assert "test2.txt" in file_names
        assert "test3.json" in file_names
        assert len(files) == 3  # 不包括子目录中的文件
        
        # 测试递归列表
        files = file_utils.list_files(self.temp_dir, recursive=True)
        file_names = [f.name for f in files]
        assert "test1.py" in file_names
        assert "test4.py" in file_names  # 子目录中的文件
        assert len(files) == 4
        
        # 测试模式匹配
        py_files = file_utils.list_files(self.temp_dir, pattern="*.py", recursive=True)
        py_file_names = [f.name for f in py_files]
        assert "test1.py" in py_file_names
        assert "test4.py" in py_file_names
        assert "test2.txt" not in py_file_names
        assert len(py_files) == 2
    
    def test_find_files_by_extension(self):
        """测试按扩展名查找文件"""
        # 创建测试文件
        extensions = [".py", ".txt", ".json", ".md"]
        for ext in extensions:
            file_path = os.path.join(self.temp_dir, f"test{ext}")
            file_utils.write_text_file(file_path, "content")
        
        # 创建子目录文件
        subdir = os.path.join(self.temp_dir, "subdir")
        os.makedirs(subdir, exist_ok=True)
        for ext in extensions[:2]:  # .py 和 .txt
            file_path = os.path.join(subdir, f"sub_test{ext}")
            file_utils.write_text_file(file_path, "content")
        
        # 查找Python文件
        py_files = file_utils.find_files_by_extension(self.temp_dir, [".py"], recursive=True)
        assert len(py_files) == 2  # test.py 和 subdir/sub_test.py
        
        # 查找多种扩展名
        text_files = file_utils.find_files_by_extension(self.temp_dir, [".txt", ".md"], recursive=True)
        assert len(text_files) == 3  # test.txt, test.md, subdir/sub_test.txt
    
    def test_create_directory(self):
        """测试创建目录"""
        new_dir = os.path.join(self.temp_dir, "new", "nested", "directory")
        
        # 创建目录
        result = file_utils.create_directory(new_dir)
        assert os.path.exists(new_dir)
        assert os.path.isdir(new_dir)
        assert str(result) == new_dir
        
        # 测试已存在的目录
        result2 = file_utils.create_directory(new_dir)
        assert str(result2) == new_dir  # 应该不会报错
    
    def test_copy_file(self):
        """测试复制文件"""
        # 创建源文件
        source_file = os.path.join(self.temp_dir, "source.txt")
        file_utils.write_text_file(source_file, "源文件内容")
        
        # 目标文件
        dest_file = os.path.join(self.temp_dir, "dest.txt")
        
        # 复制文件
        result = file_utils.copy_file(source_file, dest_file)
        assert os.path.exists(dest_file)
        assert str(result) == dest_file
        
        # 验证内容
        source_content = file_utils.read_text_file(source_file)
        dest_content = file_utils.read_text_file(dest_file)
        assert source_content == dest_content
        
        # 测试覆盖
        file_utils.write_text_file(source_file, "新内容")
        file_utils.copy_file(source_file, dest_file, overwrite=True)
        new_content = file_utils.read_text_file(dest_file)
        assert new_content == "新内容"
    
    def test_move_file(self):
        """测试移动文件"""
        # 创建源文件
        source_file = os.path.join(self.temp_dir, "source.txt")
        file_utils.write_text_file(source_file, "要移动的内容")
        
        # 目标文件
        dest_file = os.path.join(self.temp_dir, "moved.txt")
        
        # 移动文件
        result = file_utils.move_file(source_file, dest_file)
        assert not os.path.exists(source_file)  # 源文件应该不存在了
        assert os.path.exists(dest_file)  # 目标文件应该存在
        assert str(result) == dest_file
        
        # 验证内容
        content = file_utils.read_text_file(dest_file)
        assert content == "要移动的内容"
    
    def test_delete_file(self):
        """测试删除文件"""
        # 创建文件
        file_to_delete = os.path.join(self.temp_dir, "to_delete.txt")
        file_utils.write_text_file(file_to_delete, "内容")
        assert os.path.exists(file_to_delete)
        
        # 删除文件
        file_utils.delete_file(file_to_delete)
        assert not os.path.exists(file_to_delete)
        
        # 测试missing_ok参数
        file_utils.delete_file("nonexistent.txt", missing_ok=True)  # 应该不会报错
        
        with pytest.raises(FileNotFoundError):
            file_utils.delete_file("nonexistent.txt", missing_ok=False)
    
    def test_get_file_line_count(self):
        """测试获取文件行数"""
        # 创建多行文件
        lines = ["第一行", "第二行", "第三行", "第四行", "第五行"]
        content = "\n".join(lines)
        file_utils.write_text_file(self.test_file, content)
        
        # 获取行数
        line_count = file_utils.get_file_line_count(self.test_file)
        assert line_count == 5
        
        # 测试空文件
        empty_file = os.path.join(self.temp_dir, "empty.txt")
        file_utils.write_text_file(empty_file, "")
        line_count = file_utils.get_file_line_count(empty_file)
        assert line_count == 1  # 空文件有1行（空行）
    
    def test_search_in_file(self):
        """测试在文件中搜索文本"""
        # 创建测试文件
        content = """这是第一行文本。
第二行包含Python关键字。
第三行也有Python。
第四行没有关键词。
第五行Python再次出现。"""
        
        file_utils.write_text_file(self.test_file, content)
        
        # 搜索不区分大小写
        matches = file_utils.search_in_file(self.test_file, "python", case_sensitive=False)
        assert len(matches) == 3
        
        # 检查匹配详情
        match_lines = [m["line_number"] for m in matches]
        assert match_lines == [2, 3, 5]
        
        # 搜索区分大小写（应该找不到）
        matches = file_utils.search_in_file(self.test_file, "python", case_sensitive=True)
        assert len(matches) == 0
        
        # 搜索区分大小写（找到Python）
        matches = file_utils.search_in_file(self.test_file, "Python", case_sensitive=True)
        assert len(matches) == 3
    
    def test_backup_file(self):
        """测试备份文件"""
        # 创建源文件
        source_file = os.path.join(self.temp_dir, "original.txt")
        file_utils.write_text_file(source_file, "原始内容")
        
        # 备份文件
        backup_path = file_utils.backup_file(source_file, backup_dir=self.temp_dir)
        
        assert os.path.exists(backup_path)
        assert backup_path != source_file
        assert "original_" in str(backup_path)
        assert backup_path.suffix == ".bak"
        
        # 验证备份内容
        original_content = file_utils.read_text_file(source_file)
        backup_content = file_utils.read_text_file(backup_path)
        assert original_content == backup_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])