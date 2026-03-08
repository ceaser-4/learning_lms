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
        ("自动化_张三", "STU_001", 1, 30, 201),
        ("自动化_李四", "STU_002", 2, 20, 201),
        ("自动化_边界", "STU_003", 1, 100, 201),])
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

    @pytest.fixture
    def setup_filter_data(self, auth_client):
        """
        这个 Fixture 负责给下面的测试准备 3 条特定的数据
        注意：因为有 django_db 回滚，每次跑参数化用例时，这里都会重新执行，保证环境干净。
        """
        # 1. 20岁男生
        auth_client.post('/api/students/', {"name": "Filter_张三", "student_id": "STU001", "gender": 1, "age": 20})
        # 2. 20岁女生 (假设你的 gender=2 是女)
        auth_client.post('/api/students/', {"name": "Filter_李四", "student_id": "STU002", "gender": 2, "age": 20})
        # 3. 30岁男生
        auth_client.post('/api/students/', {"name": "Filter_王五", "student_id": "STU003", "gender": 1, "age": 30})

    @pytest.mark.parametrize("query_params, expected_count, check_name", [
        # 用例1: 精确查 20 岁 -> 应该有 2 人 (张三+李四)
        ({"age": 20}, 2, None),

        # 用例2: 组合查 20 岁且是男生 -> 只有 1 人 (张三)
        ({"age": 20, "gender": 1}, 1, "Filter_张三"),

        # 用例3: 模糊搜 "李四" -> 只有 1 人 (李四)
        ({"search": "李四"}, 1, "Filter_李四"),

        # 用例4: 查不存在的 (比如 100 岁) -> 0 人
        ({"age": 100}, 0, None),
    ])
    def test_search_and_filter_pro(self, auth_client, setup_filter_data, query_params, expected_count, check_name):
        """
        专业版: 这里的 setup_filter_data 会先自动运行，把 3 个学生造好
        然后根据 parametrize 的参数，跑 4 次测试
        """
        # 发送 GET 请求，带上查询参数 (data=...)
        # 比如: /api/students/?age=20
        response = auth_client.get('/api/students/', data=query_params)

        # 验证状态码
        assert response.status_code == 200

        # 验证数量
        results = response.json()['results']
        assert len(results) == expected_count

        # 验证具体的人名 (如果有指定的话)
        if check_name:
            assert results[0]['name'] == check_name

    def test_ordering(self, auth_client, setup_filter_data):
        """
        测试排序功能
        场景：
        setup_filter_data 已经自动造了 3 个学生:
        1. 张三 (20岁)
        2. 李四 (20岁)
        3. 王五 (30岁)
        """
        # 1. 测试按年龄倒序 (ordering=-age)
        # 预期顺序：王五(30) -> 张三/李四(20)
        response = auth_client.get('/api/students/', data={'ordering': '-age'})

        assert response.status_code == 200
        results = response.json()['results']

        # 验证：第一名应该是 30 岁的 "Filter_王五"
        assert results[0]['name'] == "Filter_王五"
        # 验证：最后一名应该是 20 岁
        assert results[2]['age'] == 20

        print("\n✅ 排序测试通过！Day 12 完美收官！")
