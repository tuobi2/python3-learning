#!/usr/bin/env python3
"""
Python基础语法示例

包含Python基础语法的完整示例，适合初学者学习。
包括变量、数据类型、控制流、函数、类等核心概念。
"""

print("=" * 60)
print("Python基础语法示例")
print("=" * 60)


def demonstrate_variables_and_types():
    """演示变量和数据类型"""
    print("\n1. 变量和数据类型:")
    print("-" * 40)
    
    # 基本数据类型
    name = "Python学习者"          # 字符串
    age = 25                      # 整数
    height = 1.75                 # 浮点数
    is_student = True             # 布尔值
    score = None                  # 空值
    
    print(f"姓名 (str): {name}")
    print(f"年龄 (int): {age}")
    print(f"身高 (float): {height:.2f}米")
    print(f"是否学生 (bool): {is_student}")
    print(f"分数 (None): {score}")
    
    # 类型转换
    print("\n类型转换:")
    age_str = str(age)
    height_int = int(height)
    print(f"年龄转字符串: '{age_str}' (类型: {type(age_str)})")
    print(f"身高转整数: {height_int} (类型: {type(height_int)})")


def demonstrate_collections():
    """演示集合数据类型"""
    print("\n2. 集合数据类型:")
    print("-" * 40)
    
    # 列表 (List) - 有序，可修改
    fruits = ["苹果", "香蕉", "橙子", "葡萄"]
    print(f"水果列表: {fruits}")
    print(f"第一个水果: {fruits[0]}")
    print(f"最后两个水果: {fruits[-2:]}")
    print(f"列表长度: {len(fruits)}")
    
    # 列表操作
    fruits.append("芒果")
    fruits.insert(1, "梨")
    print(f"添加后: {fruits}")
    
    # 元组 (Tuple) - 有序，不可修改
    coordinates = (10.5, 20.3)
    print(f"\n坐标元组: {coordinates}")
    print(f"X坐标: {coordinates[0]}")
    print(f"Y坐标: {coordinates[1]}")
    
    # 字典 (Dictionary) - 键值对
    person = {
        "name": "张三",
        "age": 30,
        "city": "北京",
        "skills": ["Python", "JavaScript", "SQL"]
    }
    print(f"\n个人信息字典: {person}")
    print(f"城市: {person['city']}")
    print(f"技能: {person['skills']}")
    print(f"是否有email键: {'email' in person}")
    
    # 集合 (Set) - 无序，不重复
    unique_numbers = {1, 2, 3, 3, 4, 4, 5}
    print(f"\n数字集合 (自动去重): {unique_numbers}")
    print(f"集合大小: {len(unique_numbers)}")


def demonstrate_control_flow():
    """演示控制流"""
    print("\n3. 控制流:")
    print("-" * 40)
    
    # 条件判断
    score = 85
    if score >= 90:
        grade = "优秀"
    elif score >= 80:
        grade = "良好"
    elif score >= 60:
        grade = "及格"
    else:
        grade = "不及格"
    print(f"分数: {score}, 等级: {grade}")
    
    # 三元表达式
    status = "通过" if score >= 60 else "不通过"
    print(f"考试状态: {status}")
    
    # for循环
    print("\nfor循环示例:")
    print("数字1-5的平方:")
    for i in range(1, 6):
        print(f"  {i}² = {i**2}")
    
    # while循环
    print("\nwhile循环示例:")
    count = 1
    while count <= 3:
        print(f"  计数: {count}")
        count += 1
    
    # 循环控制
    print("\n循环控制 (break/continue):")
    for i in range(1, 11):
        if i == 3:
            continue  # 跳过3
        if i == 8:
            break     # 到8时停止
        print(f"  i = {i}")


def demonstrate_functions():
    """演示函数"""
    print("\n4. 函数:")
    print("-" * 40)
    
    # 基本函数
    def greet(name: str, greeting: str = "你好") -> str:
        """
        打招呼函数
        
        Args:
            name: 姓名
            greeting: 问候语，默认为"你好"
        
        Returns:
            完整的问候语
        """
        return f"{greeting}, {name}!"
    
    # 带默认参数的函数
    def calculate_area(length: float, width: float = 1.0) -> float:
        """计算矩形面积"""
        return length * width
    
    # 可变参数
    def sum_numbers(*args: float) -> float:
        """计算任意数量数字的和"""
        return sum(args)
    
    # 关键字参数
    def print_info(**kwargs):
        """打印关键字参数"""
        for key, value in kwargs.items():
            print(f"  {key}: {value}")
    
    # 测试函数
    print("打招呼函数:")
    print(f"  {greet('李四')}")
    print(f"  {greet('王五', 'Hello')}")
    
    print("\n计算面积:")
    print(f"  矩形面积 (5x3): {calculate_area(5, 3)}")
    print(f"  矩形面积 (5x默认): {calculate_area(5)}")
    
    print("\n求和函数:")
    print(f"  1+2+3 = {sum_numbers(1, 2, 3)}")
    print(f"  1+2+3+4+5 = {sum_numbers(1, 2, 3, 4, 5)}")
    
    print("\n关键字参数:")
    print_info(name="张三", age=25, city="北京")


def demonstrate_classes():
    """演示类和对象"""
    print("\n5. 类和对象:")
    print("-" * 40)
    
    class Student:
        """学生类"""
        
        # 类属性
        school = "Python大学"
        
        def __init__(self, name: str, student_id: str):
            """初始化方法"""
            self.name = name
            self.student_id = student_id
            self.courses = []  # 实例属性
        
        def enroll(self, course_name: str) -> None:
            """选课方法"""
            self.courses.append(course_name)
            print(f"  {self.name} 选了 {course_name} 课程")
        
        def show_info(self) -> None:
            """显示学生信息"""
            print(f"\n学生信息:")
            print(f"  姓名: {self.name}")
            print(f"  学号: {self.student_id}")
            print(f"  学校: {self.school}")
            print(f"  课程: {', '.join(self.courses) if self.courses else '暂无课程'}")
        
        @classmethod
        def change_school(cls, new_school: str) -> None:
            """类方法：修改学校"""
            cls.school = new_school
            print(f"  学校已改为: {new_school}")
        
        @staticmethod
        def is_valid_id(student_id: str) -> bool:
            """静态方法：验证学号"""
            return len(student_id) == 7 and student_id.isdigit()
    
    # 创建对象
    student1 = Student("小明", "2023001")
    student2 = Student("小红", "2023002")
    
    # 调用方法
    student1.enroll("Python编程")
    student1.enroll("数据结构")
    student2.enroll("算法分析")
    
    student1.show_info()
    student2.show_info()
    
    # 类方法调用
    Student.change_school("人工智能学院")
    student1.show_info()
    
    # 静态方法调用
    print(f"\n学号验证:")
    print(f"  '2023001' 是否有效: {Student.is_valid_id('2023001')}")
    print(f"  'ABC123' 是否有效: {Student.is_valid_id('ABC123')}")


def demonstrate_file_operations():
    """演示文件操作"""
    print("\n6. 文件操作:")
    print("-" * 40)
    
    import tempfile
    import os
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        f.write("这是一个临时文件\n")
        f.write("用于演示Python文件操作\n")
        f.write("文件操作包括：\n")
        f.write("1. 创建文件\n")
        f.write("2. 写入内容\n")
        f.write("3. 读取内容\n")
        f.write("4. 删除文件\n")
        temp_file = f.name
    
    print(f"创建了临时文件: {temp_file}")
    
    # 读取文件
    print("\n读取文件内容:")
    try:
        with open(temp_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                print(f"  第{line_num:2}行: {line.strip()}")
    except FileNotFoundError:
        print("  文件不存在")
    except IOError as e:
        print(f"  读取文件错误: {e}")
    
    # 追加内容
    print("\n追加内容到文件:")
    try:
        with open(temp_file, 'a', encoding='utf-8') as f:
            f.write("5. 追加内容\n")
        print("  内容追加成功")
    except IOError as e:
        print(f"  追加内容错误: {e}")
    
    # 删除文件
    print(f"\n删除临时文件: {os.path.basename(temp_file)}")
    try:
        os.unlink(temp_file)
        print("  文件删除成功")
    except OSError as e:
        print(f"  删除文件错误: {e}")


def demonstrate_error_handling():
    """演示错误处理"""
    print("\n7. 错误处理:")
    print("-" * 40)
    
    def safe_divide(a: float, b: float) -> float:
        """安全的除法函数"""
        try:
            result = a / b
            return result
        except ZeroDivisionError:
            print(f"  错误: 除数不能为零 (a={a}, b={b})")
            return float('inf')  # 返回无穷大
        except TypeError as e:
            print(f"  类型错误: {e}")
            raise  # 重新抛出异常
        finally:
            print(f"  除法运算完成: {a} ÷ {b}")
    
    # 测试正常情况
    print("正常除法:")
    result1 = safe_divide(10, 2)
    print(f"  10 ÷ 2 = {result1}")
    
    # 测试除零错误
    print("\n除零错误:")
    result2 = safe_divide(10, 0)
    print(f"  10 ÷ 0 = {result2}")
    
    # 测试类型错误
    print("\n类型错误:")
    try:
        result3 = safe_divide(10, 'a')
    except TypeError as e:
        print(f"  捕获到类型错误: {e}")


def demonstrate_standard_library():
    """演示标准库使用"""
    print("\n8. 标准库示例:")
    print("-" * 40)
    
    import datetime
    import math
    import random
    import json
    
    # datetime模块
    now = datetime.datetime.now()
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"今天是: {now.strftime('%A')}")
    
    # math模块
    print(f"\n数学计算:")
    print(f"  π的值: {math.pi:.4f}")
    print(f"  e的值: {math.e:.4f}")
    print(f"  2的平方根: {math.sqrt(2):.4f}")
    print(f"  5的阶乘: {math.factorial(5)}")
    
    # random模块
    print(f"\n随机数:")
    print(f"  随机整数 (1-100): {random.randint(1, 100)}")
    print(f"  随机浮点数: {random.random():.4f}")
    print(f"  随机选择: {random.choice(['苹果', '香蕉', '橙子'])}")
    
    # json模块
    print(f"\nJSON处理:")
    data = {
        "name": "张三",
        "age": 30,
        "skills": ["Python", "Java"],
        "is_student": False
    }
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    print(f"  JSON字符串:\n{json_str}")
    
    # 解析JSON
    parsed_data = json.loads(json_str)
    print(f"  解析后姓名: {parsed_data['name']}")


def demonstrate_list_comprehensions():
    """演示列表推导式"""
    print("\n9. 列表推导式:")
    print("-" * 40)
    
    # 基本列表推导式
    squares = [x**2 for x in range(1, 11)]
    print(f"1-10的平方: {squares}")
    
    # 带条件的列表推导式
    even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
    print(f"偶数的平方: {even_squares}")
    
    # 嵌套循环的列表推导式
    pairs = [(x, y) for x in range(1, 4) for y in range(1, 4)]
    print(f"坐标对: {pairs}")
    
    # 字典推导式
    square_dict = {x: x**2 for x in range(1, 6)}
    print(f"平方字典: {square_dict}")
    
    # 集合推导式
    unique_squares = {x**2 for x in range(-5, 6)}
    print(f"唯一平方值: {sorted(unique_squares)}")


def main():
    """主函数"""
    print("Python基础语法示例程序")
    print("包含10个核心概念的演示")
    print()
    
    # 执行所有演示函数
    functions = [
        demonstrate_variables_and_types,
        demonstrate_collections,
        demonstrate_control_flow,
        demonstrate_functions,
        demonstrate_classes,
        demonstrate_file_operations,
        demonstrate_error_handling,
        demonstrate_standard_library,
        demonstrate_list_comprehensions,
    ]
    
    for i, func in enumerate(functions, 1):
        func()
        if i < len(functions):
            input(f"\n按Enter继续第{i+1}部分...")
    
    print("\n" + "=" * 60)
    print("所有示例演示完成！")
    print("=" * 60)
    print("\n建议:")
    print("1. 修改代码并观察变化")
    print("2. 添加自己的示例")
    print("3. 查阅Python官方文档")
    print("4. 尝试解决实际问题")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        import traceback
        traceback.print_exc()