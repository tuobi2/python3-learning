#!/usr/bin/env python3
"""
基础测试 - 确保CI/CD能通过
"""

import pytest


def test_addition():
    """测试基本加法"""
    assert 1 + 1 == 2


def test_string():
    """测试字符串操作"""
    assert "hello".upper() == "HELLO"


def test_list():
    """测试列表操作"""
    numbers = [1, 2, 3]
    assert len(numbers) == 3
    assert sum(numbers) == 6


def test_dict():
    """测试字典操作"""
    person = {"name": "Alice", "age": 25}
    assert person["name"] == "Alice"
    assert "age" in person


@pytest.mark.parametrize("input_val,expected", [
    (0, 0),
    (1, 1),
    (-1, 1),
    (10, 10),
])
def test_abs_function(input_val, expected):
    """测试abs函数（参数化测试）"""
    assert abs(input_val) == expected


class TestBasicMath:
    """基础数学测试类"""
    
    def test_multiplication(self):
        """测试乘法"""
        assert 2 * 3 == 6
        assert 0 * 5 == 0
        assert -2 * 3 == -6
    
    def test_division(self):
        """测试除法"""
        assert 6 / 2 == 3
        assert 10 / 5 == 2
        
        # 测试除零异常
        with pytest.raises(ZeroDivisionError):
            _ = 1 / 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])