#!/usr/bin/env python3
"""
Python基础语法单元测试
"""

import pytest
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

# 注意：python_fundamentals_auto.py是一个直接运行的脚本，不是模块
# 我们只测试Python基础语法，不导入示例文件


class TestPythonBasics:
    """测试Python基础语法"""
    
    def test_variable_types(self):
        """测试变量类型"""
        # 这里可以测试基础语法示例中的函数
        # 由于示例是直接运行的，我们需要重构或模拟测试
        pass
    
    def test_string_operations(self):
        """测试字符串操作"""
        assert "hello".upper() == "HELLO"
        assert " world ".strip() == "world"
        assert len("python") == 6
    
    def test_list_operations(self):
        """测试列表操作"""
        numbers = [1, 2, 3, 4, 5]
        assert len(numbers) == 5
        assert sum(numbers) == 15
        assert numbers[0] == 1
        assert numbers[-1] == 5
        
        # 列表推导式
        squares = [x**2 for x in numbers]
        assert squares == [1, 4, 9, 16, 25]
    
    def test_dict_operations(self):
        """测试字典操作"""
        person = {
            "name": "张三",
            "age": 25,
            "city": "北京"
        }
        
        assert person["name"] == "张三"
        assert "age" in person
        assert len(person) == 3
        
        # 更新字典
        person["age"] = 26
        assert person["age"] == 26
    
    def test_set_operations(self):
        """测试集合操作"""
        set1 = {1, 2, 3, 4, 5}
        set2 = {4, 5, 6, 7, 8}
        
        # 并集
        union = set1 | set2
        assert union == {1, 2, 3, 4, 5, 6, 7, 8}
        
        # 交集
        intersection = set1 & set2
        assert intersection == {4, 5}
        
        # 差集
        difference = set1 - set2
        assert difference == {1, 2, 3}
    
    @pytest.mark.parametrize("input_val,expected", [
        (1, 1),
        (0, 0),
        (-1, 1),
        (10, 10),
    ])
    def test_abs_function(self, input_val, expected):
        """测试abs函数（参数化测试）"""
        assert abs(input_val) == expected
    
    def test_exception_handling(self):
        """测试异常处理"""
        with pytest.raises(ZeroDivisionError):
            result = 1 / 0
        
        with pytest.raises(KeyError):
            d = {}
            value = d["nonexistent"]


class TestControlFlow:
    """测试控制流"""
    
    def test_if_else(self):
        """测试if-else语句"""
        def check_number(num):
            if num > 0:
                return "positive"
            elif num < 0:
                return "negative"
            else:
                return "zero"
        
        assert check_number(5) == "positive"
        assert check_number(-3) == "negative"
        assert check_number(0) == "zero"
    
    def test_for_loop(self):
        """测试for循环"""
        numbers = list(range(1, 6))
        result = []
        
        for num in numbers:
            result.append(num * 2)
        
        assert result == [2, 4, 6, 8, 10]
    
    def test_while_loop(self):
        """测试while循环"""
        count = 0
        result = []
        
        while count < 5:
            result.append(count)
            count += 1
        
        assert result == [0, 1, 2, 3, 4]
    
    def test_list_comprehension(self):
        """测试列表推导式"""
        # 简单的列表推导式
        squares = [x**2 for x in range(1, 6)]
        assert squares == [1, 4, 9, 16, 25]
        
        # 带条件的列表推导式
        evens = [x for x in range(10) if x % 2 == 0]
        assert evens == [0, 2, 4, 6, 8]


class TestFunctions:
    """测试函数"""
    
    def test_basic_function(self):
        """测试基本函数"""
        def add(a, b):
            return a + b
        
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
    
    def test_function_with_default_args(self):
        """测试带默认参数的函数"""
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"
        
        assert greet("Alice") == "Hello, Alice!"
        assert greet("Bob", "Hi") == "Hi, Bob!"
    
    def test_function_with_keyword_args(self):
        """测试关键字参数"""
        def create_person(name, age, city):
            return {"name": name, "age": age, "city": city}
        
        # 使用关键字参数
        person = create_person(name="张三", age=25, city="北京")
        assert person == {"name": "张三", "age": 25, "city": "北京"}
        
        # 混合使用位置参数和关键字参数
        person2 = create_person("李四", city="上海", age=30)
        assert person2 == {"name": "李四", "age": 30, "city": "上海"}
    
    def test_variable_length_args(self):
        """测试可变长度参数"""
        def sum_all(*args):
            return sum(args)
        
        assert sum_all(1, 2, 3) == 6
        assert sum_all(1, 2, 3, 4, 5) == 15
        assert sum_all() == 0
    
    def test_keyword_args(self):
        """测试关键字参数"""
        def print_info(**kwargs):
            return kwargs
        
        info = print_info(name="Alice", age=25, city="New York")
        assert info == {"name": "Alice", "age": 25, "city": "New York"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])