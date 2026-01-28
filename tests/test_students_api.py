import pytest
import requests

# 定义被测接口的地址
BASE_URL = 'http://127.0.0.1:8000/api/students/'

class TestStudentAPI:
    """
    学生管理系统的接口测试类
    """
    # 定义测试数据 (影分身的数据源)
    # 格式：列表里面套元组。每个元组是一组测试数据。
    # 设计 3 个场景：
    # Case 1: 正常男生 (20岁)
    # Case 2: 正常女生 (18岁)
    # Case 3: 边界年龄 (100岁，假设系统允许)
    test_data = [
        ("自动化_张三", "TEST_001", 1, 20, 201),
        ("自动化_李四", "TEST_002", 2, 18, 201),
        ("自动化_王五", "TEST_003", 1, 100, 201),
    ]

    def test_get_students(self):
        """
        测试用例1：验证能否成功获取学生列表
        """
        response = requests.get(BASE_URL)
        # 判定response返回的状态码是否为200
        assert response.status_code == 200
        # 把接口返回的json数据赋值到data变量中
        data = response.json()

        print(f"\n获取到的学生列表：{data}")
        # 断言返回的是一个列表 (因为是获取所有学生)
        assert isinstance(data, list)

    # 2. 应用参数化装饰器
    # "name, s_id, gender, age, expected_status" 对应上面元组里的 5 个值
    # ids 参数用于给每一条用例起个名字，方便在报告里看
    @pytest.mark.parametrize("name, s_id, gender, age, expected_status", test_data,ids=["Male_Normal", "Female_Normal", "Age_Max"])
    def test_create_student_batch(self, cleanup_student, name, s_id, gender, age, expected_status):

        print(f"\n[测试执行] 正在测试：{name},学号：{s_id}")

        # 准备数据
        new_student = {
            "name": name,
            "student_id": s_id,
            "gender": gender,
            "age": age
        }

        # 发送请求
        response = requests.post(BASE_URL, json=new_student)

        # 如果断言失败，就把 response.text (服务器返回的错误详情) 打印出来
        assert response.status_code == expected_status, f"创建失败！服务器返回: {response.text}"

        # 只有创建成功才校验返回数据
        if expected_status == 201:
            result = response.json()
            assert result["name"] == name
            assert result["student_id"] == s_id

