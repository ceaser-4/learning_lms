import pytest

@pytest.mark.django_db
class TestStudentAPI:
    """
    学生管理系统的接口测试类
    """

    def test_get_students(self,auth_client):
        """
        测试用例1：验证能否成功获取学生列表
        """
        response = auth_client.get('/api/students/')
        # 判定response返回的状态码是否为200
        assert response.status_code == 200
        # 把接口返回的json数据赋值到data变量中
        data = response.json()

        print(f"\n获取到的学生列表：{data}")
        # 断言返回的是一个列表 (因为是获取所有学生)
        assert isinstance(data['results'], list)

    # 2. 应用参数化装饰器
    # "name, s_id, gender, age, expected_status" 对应上面元组里的 5 个值
    # ids 参数用于给每一条用例起个名字，方便在报告里看
    @pytest.mark.parametrize("name, s_id, gender, age, expected_status", [
        ("自动化_张三", "TEST_001", 1, 30, 201),
        ("自动化_李四", "TEST_002", 2, 20, 201),
        ("自动化_边界", "TEST_003", 1, 100, 201),])
    def test_create_student_batch(self, auth_client , name, s_id, gender, age, expected_status):

        # 准备数据
        payload = {
            "name": name,
            "student_id": s_id,
            "gender": gender,
            "age": age
        }

        # 发送请求
        # client.post(路径, 数据, 格式)
        # 注意: 这里最好加上 format='json'，确保数据是以 JSON 格式发送的
        response = auth_client.post('/api/students/', data=payload, format='json')

        # 只有创建成功才校验返回数据
        if response.status_code != expected_status:
            print(f"\n[ERROR] 期望 {expected_status}, 实际 {response.status_code}")
            print(f"[Error] 服务器返回：{response.json()}")

        # 断言判定实际code是否与用例中预期的code相同
        assert response.status_code == expected_status



