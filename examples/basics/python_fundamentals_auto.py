#!/usr/bin/env python3
"""
Python基础语法示例 - 自动运行版

包含Python基础语法的完整示例，适合初学者学习。
自动运行所有示例，无需交互输入。
"""

print("=" * 60)
print("Python基础语法示例 - 自动运行版")
print("=" * 60)


def demonstrate_variables_and_types():
    """演示变量和数据类型"""
    print("\n1. 变量和数据类型:")
    print("-" * 40)
    
    # 基本数据类型
    name = "Python学习者"
    age = 25
    height = 1.75
    is_student = True
    score = None
    
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
    
    # 列表 (List)
    fruits = ["苹果", "香蕉", "橙子", "葡萄"]
    print(f"水果列表: {fruits}")
    print(f"第一个水果: {fruits[0]}")
    print(f"最后两个水果: {fruits[-2:]}")
    
    # 字典 (Dictionary)
    person = {
        "name": "张三",
        "age": 30,
        "city": "北京",
        "skills": ["Python", "JavaScript", "SQL"]
    }
    print(f"\n个人信息字典: {person}")
    print(f"城市: {person['city']}")
    print(f"技能: {person['skills']}")
    
    # 集合 (Set)
    unique_numbers = {1, 2, 3, 3, 4, 4, 5}
    print(f"\n数字集合 (自动去重): {unique_numbers}")


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
    
    # for循环
    print("\nfor循环示例:")
    print("数字1-5的平方:")
    for i in range(1, 6):
        print(f"  {i}² = {i**2}")


def demonstrate_functions():
    """演示函数"""
    print("\n4. 函数:")
    print("-" * 40)
    
    def greet(name: str, greeting: str = "你好") -> str:
        """打招呼函数"""
        return f"{greeting}, {name}!"
    
    def calculate_area(length: float, width: float = 1.0) -> float:
        """计算矩形面积"""
        return length * width
    
    print("打招呼函数:")
    print(f"  {greet('李四')}")
    print(f"  {greet('王五', 'Hello')}")
    
    print("\n计算面积:")
    print(f"  矩形面积 (5x3): {calculate_area(5, 3)}")


def demonstrate_classes():
    """演示类和对象"""
    print("\n5. 类和对象:")
    print("-" * 40)
    
    class Student:
        """学生类"""
        school = "Python大学"
        
        def __init__(self, name: str, student_id: str):
            self.name = name
            self.student_id = student_id
            self.courses = []
        
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
    
    # 创建对象
    student1 = Student("小明", "2023001")
    student1.enroll("Python编程")
    student1.enroll("数据结构")
    student1.show_info()


def demonstrate_error_handling():
    """演示错误处理"""
    print("\n6. 错误处理:")
    print("-" * 40)
    
    def safe_divide(a: float, b: float) -> float:
        """安全的除法函数"""
        try:
            result = a / b
            return result
        except ZeroDivisionError:
            print(f"  错误: 除数不能为零 (a={a}, b={b})")
            return float('inf')
    
    print("正常除法:")
    result1 = safe_divide(10, 2)
    print(f"  10 ÷ 2 = {result1}")
    
    print("\n除零错误:")
    result2 = safe_divide(10, 0)
    print(f"  10 ÷ 0 = {result2}")


def main():
    """主函数"""
    print("Python基础语法示例 - 自动运行版")
    print("包含6个核心概念的演示")
    print()
    
    # 执行所有演示函数
    functions = [
        demonstrate_variables_and_types,
        demonstrate_collections,
        demonstrate_control_flow,
        demonstrate_functions,
        demonstrate_classes,
        demonstrate_error_handling,
    ]
    
    for i, func in enumerate(functions, 1):
        func()
        print()  # 空行分隔
    
    print("=" * 60)
    print("所有示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        import traceback
        traceback.print_exc()