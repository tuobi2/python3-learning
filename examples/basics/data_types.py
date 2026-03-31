#!/usr/bin/env python3
"""
Python数据类型详解

详细演示Python的各种数据类型及其操作。
"""

print("=" * 60)
print("Python数据类型详解")
print("=" * 60)


def demonstrate_numbers():
    """演示数字类型"""
    print("\n1. 数字类型 (Numbers):")
    print("-" * 40)
    
    # 整数 (int)
    integer_num = 42
    large_int = 10_000_000  # 使用下划线提高可读性
    binary_num = 0b1010     # 二进制
    octal_num = 0o12        # 八进制
    hex_num = 0xFF          # 十六进制
    
    print(f"整数: {integer_num} (类型: {type(integer_num)})")
    print(f"大整数: {large_int:,}")
    print(f"二进制 0b1010 = {binary_num}")
    print(f"八进制 0o12 = {octal_num}")
    print(f"十六进制 0xFF = {hex_num}")
    
    # 浮点数 (float)
    float_num = 3.14159
    scientific_num = 1.23e-4  # 科学计数法
    
    print(f"\n浮点数: {float_num} (类型: {type(float_num)})")
    print(f"科学计数法: {scientific_num} = {scientific_num:.6f}")
    
    # 复数 (complex)
    complex_num = 3 + 4j
    
    print(f"\n复数: {complex_num}")
    print(f"实部: {complex_num.real}")
    print(f"虚部: {complex_num.imag}")
    print(f"模长: {abs(complex_num)}")
    
    # 数字运算
    print("\n数字运算:")
    a, b = 10, 3
    print(f"{a} + {b} = {a + b}")
    print(f"{a} - {b} = {a - b}")
    print(f"{a} * {b} = {a * b}")
    print(f"{a} / {b} = {a / b:.4f}")
    print(f"{a} // {b} = {a // b} (整除)")
    print(f"{a} % {b} = {a % b} (取余)")
    print(f"{a} ** {b} = {a ** b} (幂运算)")
    
    # 数学函数
    import math
    print(f"\n数学函数:")
    print(f"绝对值: abs(-5) = {abs(-5)}")
    print(f"四舍五入: round(3.14159, 2) = {round(3.14159, 2)}")
    print(f"向上取整: math.ceil(3.2) = {math.ceil(3.2)}")
    print(f"向下取整: math.floor(3.8) = {math.floor(3.8)}")
    print(f"平方根: math.sqrt(16) = {math.sqrt(16)}")


def demonstrate_strings():
    """演示字符串类型"""
    print("\n2. 字符串类型 (Strings):")
    print("-" * 40)
    
    # 字符串创建
    str1 = '单引号字符串'
    str2 = "双引号字符串"
    str3 = '''多行
字符串'''
    str4 = """另一个
多行字符串"""
    
    print("字符串创建:")
    print(f"  单引号: {str1}")
    print(f"  双引号: {str2}")
    print(f"  多行字符串1:\n{str3}")
    print(f"  多行字符串2:\n{str4}")
    
    # 字符串操作
    text = "Python编程学习"
    print(f"\n原始字符串: '{text}'")
    print(f"  长度: {len(text)}")
    print(f"  大写: {text.upper()}")
    print(f"  小写: 'PYTHON'.lower() = {'PYTHON'.lower()}")
    print(f"  首字母大写: {text.capitalize()}")
    print(f"  每个单词首字母大写: 'hello world'.title() = {'hello world'.title()}")
    
    # 字符串查找和替换
    print(f"\n字符串查找和替换:")
    print(f"  包含'Python'吗? {'Python' in text}")
    print(f"  查找'编程'位置: {text.find('编程')}")
    print(f"  从右侧查找: {text.rfind('学习')}")
    print(f"  替换: {text.replace('学习', '实践')}")
    
    # 字符串分割和连接
    csv_data = "苹果,香蕉,橙子,葡萄"
    print(f"\n字符串分割和连接:")
    print(f"  分割CSV: {csv_data.split(',')}")
    print(f"  分割限制次数: {csv_data.split(',', 2)}")
    
    fruits = ['苹果', '香蕉', '橙子']
    print(f"  连接列表: {'、'.join(fruits)}")
    
    # 字符串格式化
    name, age = "张三", 25
    print(f"\n字符串格式化:")
    print(f"  f-string: {name}今年{age}岁")
    print(f"  format方法: {0}今年{1}岁".format(name, age))
    print(f"  %格式化: %s今年%d岁" % (name, age))
    
    # 原始字符串和转义字符
    print(f"\n原始字符串和转义:")
    print(f"  转义字符: 第一行\\n第二行")
    print(f"  原始字符串: r'第一行\\n第二行' = {r'第一行\n第二行'}")
    
    # 字符串检查
    test_str = "Python3"
    print(f"\n字符串检查:")
    print(f"  '{test_str}' 是字母数字吗? {test_str.isalnum()}")
    print(f"  '{test_str}' 是字母吗? {test_str.isalpha()}")
    print(f"  '123' 是数字吗? {'123'.isdigit()}")
    print(f"  '   ' 是空格吗? {'   '.isspace()}")
    print(f"  'Python' 是标题格式吗? {'Python'.istitle()}")


def demonstrate_lists():
    """演示列表类型"""
    print("\n3. 列表类型 (Lists):")
    print("-" * 40)
    
    # 列表创建
    empty_list = []
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, True]
    nested = [[1, 2], [3, 4], [5, 6]]
    
    print("列表创建:")
    print(f"  空列表: {empty_list}")
    print(f"  数字列表: {numbers}")
    print(f"  混合列表: {mixed}")
    print(f"  嵌套列表: {nested}")
    
    # 列表访问
    print(f"\n列表访问:")
    print(f"  第一个元素: numbers[0] = {numbers[0]}")
    print(f"  最后一个元素: numbers[-1] = {numbers[-1]}")
    print(f"  切片: numbers[1:4] = {numbers[1:4]}")
    print(f"  步长切片: numbers[::2] = {numbers[::2]}")
    print(f"  反转: numbers[::-1] = {numbers[::-1]}")
    
    # 列表操作
    fruits = ["苹果", "香蕉"]
    print(f"\n列表操作:")
    print(f"  原始列表: {fruits}")
    
    fruits.append("橙子")
    print(f"  追加后: {fruits}")
    
    fruits.insert(1, "葡萄")
    print(f"  插入后: {fruits}")
    
    fruits.extend(["芒果", "西瓜"])
    print(f"  扩展后: {fruits}")
    
    removed = fruits.pop()  # 移除最后一个
    print(f"  弹出最后一个: {removed}, 剩余: {fruits}")
    
    fruits.remove("葡萄")
    print(f"  移除'葡萄'后: {fruits}")
    
    # 列表方法
    nums = [3, 1, 4, 1, 5, 9, 2]
    print(f"\n列表方法:")
    print(f"  原始: {nums}")
    print(f"  排序: {sorted(nums)}")
    nums.sort()
    print(f"  原地排序后: {nums}")
    
    nums.reverse()
    print(f"  反转后: {nums}")
    
    print(f"  计数1出现次数: {nums.count(1)}")
    print(f"  查找5的位置: {nums.index(5)}")
    
    # 列表推导式
    print(f"\n列表推导式:")
    squares = [x**2 for x in range(1, 6)]
    print(f"  1-5的平方: {squares}")
    
    even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
    print(f"  偶数的平方: {even_squares}")
    
    # 列表复制
    print(f"\n列表复制:")
    original = [1, 2, 3]
    shallow_copy = original.copy()
    deep_copy = original[:]  # 另一种复制方式
    
    shallow_copy[0] = 99
    print(f"  原始: {original}")
    print(f"  浅复制修改后: {shallow_copy}")
    print(f"  深复制: {deep_copy}")


def demonstrate_tuples():
    """演示元组类型"""
    print("\n4. 元组类型 (Tuples):")
    print("-" * 40)
    
    # 元组创建
    empty_tuple = ()
    single_tuple = (42,)  # 注意逗号
    coordinates = (10.5, 20.3)
    mixed = (1, "hello", 3.14)
    nested = ((1, 2), (3, 4))
    
    print("元组创建:")
    print(f"  空元组: {empty_tuple}")
    print(f"  单元素元组: {single_tuple} (注意必须有逗号)")
    print(f"  坐标: {coordinates}")
    print(f"  混合元组: {mixed}")
    print(f"  嵌套元组: {nested}")
    
    # 元组访问
    print(f"\n元组访问:")
    print(f"  第一个元素: coordinates[0] = {coordinates[0]}")
    print(f"  最后一个元素: coordinates[-1] = {coordinates[-1]}")
    print(f"  切片: mixed[1:] = {mixed[1:]}")
    
    # 元组解包
    print(f"\n元组解包:")
    x, y = coordinates
    print(f"  坐标解包: x={x}, y={y}")
    
    # 扩展解包
    first, *middle, last = (1, 2, 3, 4, 5)
    print(f"  扩展解包: first={first}, middle={middle}, last={last}")
    
    # 元组操作
    tuple1 = (1, 2, 3)
    tuple2 = (4, 5, 6)
    
    print(f"\n元组操作:")
    print(f"  连接: {tuple1 + tuple2}")
    print(f"  重复: {tuple1 * 3}")
    print(f"  长度: len({tuple1}) = {len(tuple1)}")
    print(f"  包含检查: 2 in {tuple1} = {2 in tuple1}")
    
    # 元组与列表转换
    print(f"\n元组与列表转换:")
    list_from_tuple = list(tuple1)
    tuple_from_list = tuple([4, 5, 6])
    
    print(f"  元组转列表: {tuple1} -> {list_from_tuple}")
    print(f"  列表转元组: [4, 5, 6] -> {tuple_from_list}")
    
    # 命名元组
    from collections import namedtuple
    
    print(f"\n命名元组:")
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, 20)
    print(f"  创建: {p}")
    print(f"  访问: p.x = {p.x}, p.y = {p.y}")
    print(f"  索引访问: p[0] = {p[0]}")
    print(f"  解包: x, y = p -> x={p.x}, y={p.y}")


def demonstrate_dictionaries():
    """演示字典类型"""
    print("\n5. 字典类型 (Dictionaries):")
    print("-" * 40)
    
    # 字典创建
    empty_dict = {}
    person = {"name": "张三", "age": 25, "city": "北京"}
    dict_from_keys = dict.fromkeys(['a', 'b', 'c'], 0)
    dict_from_pairs = dict([('x', 10), ('y', 20)])
    
    print("字典创建:")
    print(f"  空字典: {empty_dict}")
    print(f"  个人信息: {person}")
    print(f"  fromkeys创建: {dict_from_keys}")
    print(f"  键值对列表创建: {dict_from_pairs}")
    
    # 字典访问
    print(f"\n字典访问:")
    print(f"  访问name: person['name'] = {person['name']}")
    print(f"  get方法: person.get('age') = {person.get('age')}")
    print(f"  获取不存在的键: person.get('email', '无邮箱') = {person.get('email', '无邮箱')}")
    
    # 检查键是否存在
    print(f"\n检查键是否存在:")
    print(f"  'name' in person = {'name' in person}")
    print(f"  'email' in person = {'email' in person}")
    
    # 字典操作
    print(f"\n字典操作:")
    person["email"] = "zhangsan@example.com"
    print(f"  添加email后: {person}")
    
    person["age"] = 26
    print(f"  修改age后: {person}")
    
    removed = person.pop("city")
    print(f"  移除city: {removed}, 剩余: {person}")
    
    # 字典方法
    print(f"\n字典方法:")
    print(f"  所有键: {list(person.keys())}")
    print(f"  所有值: {list(person.values())}")
    print(f"  所有键值对: {list(person.items())}")
    
    # 字典更新
    update_data = {"age": 27, "job": "工程师"}
    person.update(update_data)
    print(f"  更新后: {person}")
    
    # 字典推导式
    print(f"\n字典推导式:")
    squares = {x: x**2 for x in range(1, 6)}
    print(f"  平方字典: {squares}")
    
    # 嵌套字典
    print(f"\n嵌套字典:")
    students = {
        "001": {"name": "张三", "score": 85},
        "002": {"name": "李四", "score": 92},
        "003": {"name": "王五", "score": 78}
    }
    print(f"  学生数据: {students}")
    print(f"  学生001的分数: {students['001']['score']}")
    
    # 默认字典
    from collections import defaultdict
    
    print(f"\n默认字典:")
    word_count = defaultdict(int)
    words = ["apple", "banana", "apple", "orange", "banana", "apple"]
    
    for word in words:
        word_count[word] += 1
    
    print(f"  单词计数: {dict(word_count)}")


def demonstrate_sets():
    """演示集合类型"""
    print("\n6. 集合类型 (Sets):")
    print("-" * 40)
    
    # 集合创建
    empty_set = set()
    numbers = {1, 2, 3, 4, 5}
    from_list = set([1, 2, 2, 3, 3, 4])  # 自动去重
    mixed = {1, "hello", 3.14}
    
    print("集合创建:")
    print(f"  空集合: {empty_set}")
    print(f"  数字集合: {numbers}")
    print(f"  从列表创建(自动去重): {from_list}")
    print(f"  混合集合: {mixed}")
    
    # 集合操作
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}
    
    print(f"\n集合操作:")
    print(f"  集合A: {set_a}")
    print(f"  集合B: {set_b}")
    print(f"  并集: {set_a | set_b}")
    print(f"  交集: {set_a & set_b}")
    print(f"  差集(A-B): {set_a - set_b}")
    print(f"  差集(B-A): {set_b - set_a}")
    print(f"  对称差集: {set_a ^ set_b}")
    
    # 集合方法
    print(f"\n集合方法:")
    set_a.add(6)
    print(f"  添加6后: {set_a}")
    
    set_a.update([7, 8, 9])
    print(f"  更新多个元素后: {set_a}")
    
    set_a.remove(9)  # 如果不存在会报错
    print(f"  移除9后: {set_a}")
    
    set_a.discard(10)  # 如果不存在不会报错
    print(f"  尝试移除10(不存在): {set_a}")
    
    popped = set_a.pop()  # 随机移除一个元素
    print(f"  随机移除一个: {popped}, 剩余: {set_a}")
    
    # 集合检查
    print(f