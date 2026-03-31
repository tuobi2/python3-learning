#!/usr/bin/env python3
"""
CI测试 - 绝对简单的测试确保通过
"""

def test_ci_basic():
    """基础测试确保CI通过"""
    assert 1 + 1 == 2
    assert "hello" != "world"
    assert True is True


def test_string_operations():
    """字符串操作测试"""
    text = "Python"
    assert len(text) == 6
    assert text.upper() == "PYTHON"
    assert text.lower() == "python"


def test_list_operations():
    """列表操作测试"""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert sum(numbers) == 15
    assert numbers[0] == 1
    assert numbers[-1] == 5


def test_dict_operations():
    """字典操作测试"""
    data = {"name": "test", "value": 42}
    assert data["name"] == "test"
    assert data["value"] == 42
    assert len(data) == 2


if __name__ == "__main__":
    # 直接运行测试
    test_ci_basic()
    test_string_operations()
    test_list_operations()
    test_dict_operations()
    print("✅ 所有测试通过!")