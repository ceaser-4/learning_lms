import pytest
import requests

# 定义被测接口的地址
BASE_URL = 'http://127.0.0.1:8000/api/students/'

class TestStudentAPI:
    """
    学生管理系统的接口测试类
    """

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


    def test_create_student(self):
        """
        测试用例2：验证能否成功创建一个学生
        """
        # 准备测试数据
        # json里面字段的内容要和serializer里面定义的一样
        new_student = {
            "name": "自动化测试员",
            "student_id": "TEST_001",  # 注意：学号必须唯一，如果数据库里有了，再跑会报错
            "gender": 1,  # 1代表男
            "age": 25
        }

        # 模拟post请求，把new_student字典转换成json格式发送给服务器
        response = requests.post(BASE_URL, json=new_student)
        # 断言状态码是否为201（drf默认是201）
        assert response.status_code == 201

        # 用断言校验返回的json里是不是创建的数据
        result = response.json()
        assert result["name"] == new_student["name"]
        assert result["student_id"] == new_student["student_id"]