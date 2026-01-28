import pytest
import sqlite3 # 引入 Python 自带的数据库库，绕过 Django 的隔离机制

# @pytest.fixture: 这是一个装饰器，告诉 pytest 下面的函数是一个“工具”
# scope="function": 默认值。意思是每个调用它的测试函数执行前，都会运行一次这个 fixture
@pytest.fixture(scope="function")
def cleanup_student():
    """
    环境清理工具 (暴力版)
    直接连接 db.sqlite3 文件进行清理，无视 Django 的测试隔离。
    """
    print("\n[Fixture] 正在准备测试环境...")

    # 1. 直接连接项目根目录下的真实数据库文件
    # 注意：如果你的 db.sqlite3 不在根目录，需要调整路径
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # 前置清理，必须在 yield 之前！
    print("[Fixture] 正在执行前置清理...")
    try:
        cursor.execute("DELETE FROM students_student WHERE student_id LIKE 'TEST_%'")
        conn.commit()
        print(f"[Fixture] 前置清理完毕，删除了 {cursor.rowcount} 条脏数据")
    except Exception as e:
        print(f"[Fixture] 前置清理出错: {e}")

    yield

    # 4. Teardown (后置清理)
    print("\n[Fixture] 测试结束，正在执行后置清理...")
    try:
        cursor.execute("DELETE FROM students_student WHERE student_id LIKE 'TEST_%'")
        conn.commit()
        print(f"[Fixture] 后置清理完毕，删除了 {cursor.rowcount} 条数据")
    except Exception as e:
        print(f"[Fixture] 后置清理出错: {e}")

    # 5. 关闭连接
    conn.close()

