import pytest
from students.models import Student


def test_file_processing(tmp_path):
    """
    实战 tmp_path：解决环境残留痛点
    tmp_path 是 pytest 自带 fixture，返回一个 pathlib.Path 对象
    """
    # 在临时目录创建一个文件
    p = tmp_path / "hello.txt"
    p.write_text("测试数据")

    # 验证写进去了
    assert p.read_text() == "测试数据"
    # 这里不需要写 os.remove(p)，pytest 会自动打扫战场

@pytest.mark.django_db
def test_performance_sql(auth_client,django_assert_max_num_queries):
    """
    监控 SQL 查询数量。如果一个简单的查询跑了 10 次 SQL，必须报错。
    """
    # 先造两个学生，防止查询为空
    Student.objects.create(name="性能1", student_id="STU_901", age=20)
    Student.objects.create(name="性能2", student_id="STU_902", age=20)

    # 【核心代码】开启监控
    # 意思是：下面这句 get 请求，涉及的数据库查询次数必须 <= 5 次
    with django_assert_max_num_queries(5):
        response = auth_client.get('/api/students/')

    assert response.status_code == 200