import pytest
from students.models import Student
import sqlite3 # 引入 Python 自带的数据库库，绕过 Django 的隔离机制

# @pytest.fixture: 这是一个装饰器，告诉 pytest 下面的函数是一个“工具”
# scope="function": 默认值。意思是每个调用它的测试函数执行前，都会运行一次这个 fixture
@pytest.fixture(scope="function")
# def cleanup_student(db):
    # """
    # 环境清理工具：
    # 在测试开始前，什么都不做（或者也可以做准备工作）。
    # 在测试结束后，自动去数据库把 'TEST_001' 删掉。
    # """
    # print("\n[Fixture] 正在准备测试环境...")
    #
    # # yield 之前的代码会在测试用例执行【前】运行
    # # yield 之后的代码会在测试用例执行【后】运行
    # yield
    # # teardown（后置清理）：
    # print("\n[Fixture] 测试结束，正在清理脏数据...")
    # # 利用Django ORM 直接删除数据，比调接口删除更稳定、更快
    # Student.objects.filter(student_id="TEST_001").delete()
    # print("[Fixture] 清理完成！")

def cleanup_student():
    """
    环境清理工具 (暴力版)
    直接连接 db.sqlite3 文件进行清理，无视 Django 的测试隔离。
    """
    print("\n[Fixture] 正在准备测试环境...")

    yield

    print("\n[Fixture] 测试结束，正在清理脏数据 (直连模式)...")

    # 1. 直接连接项目根目录下的真实数据库文件
    # 注意：如果你的 db.sqlite3 不在根目录，需要调整路径
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # 2. 执行原生 SQL 删除语句
    # students_student 是 Django 默认生成的表名 (App名_Model名)
    try:
        cursor.execute("DELETE FROM students_student WHERE student_id='TEST_001'")
        conn.commit()  # 提交事务，确保删除生效
        print(f"[Fixture] 成功删除了 {cursor.rowcount} 条脏数据！")
    except Exception as e:
        print(f"[Fixture] 清理失败: {e}")
    finally:
        conn.close()

