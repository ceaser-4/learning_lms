import pytest
from students.models import Student

@pytest.mark.django_db
class TestBusinessRules:

    def test_unique_student_id(self, auth_client):
        """
        测试学号唯一性约束 (Model 层 unique=True)
        """
        # 创建一个合法的学生
        Student.objects.create(name='张三', age=20,gender=1,student_id='STU_999')

        # 尝试创建一个学号一模一样的(模拟bug)
        payload = {
            "name": "李四",
            "age": 22,
            "gender": 1,
            "student_id": "STU_999"
        }
        response = auth_client.post("/api/students/", data=payload)

        # 断言：应该报400错误
        assert response.status_code == 400
        # DRF的唯一性错误通常包含字段名
        assert "student_id" in response.json()

    def test_student_id_format(self, auth_client):
        """
        测试学号格式校验 (Serializer 层 validate)
        """
        # 1. 构造一个错误的学号 (没有 STU 开头)
        payload = {
            "name": "王五",
            "age": 20,
            "gender": 1,
            "student_id": "ERROR_002"
        }
        response = auth_client.post('/api/students/', data=payload)

        # 2. 断言：应该被 Serializer 拦截
        assert response.status_code == 400
        assert "学号必须以 'STU' 开头" in str(response.json())
