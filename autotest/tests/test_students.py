import pytest
import time
from autotest.services.student_api import StudentApI

class TestStudentOpenAPI:

    def setup_method(self):
        # 每次测试前，实例化一个API客户端
        self.student_api = StudentApI()

    def test_create_student_success(self):
        """
        测试目标：正常创建学生
        """
        # 动态生成唯一的学号
        # time.time() 会返回类似 1739268888.123 的数字
        # 取整数部分，拼出来的学号就是 STU_1739268888，保证不重复
        unique_id = f"STU_{int(time.time())}"

        print(f"DEBUG: 正在尝试创建学号： {unique_id}")
        # 1、调用业务层（不管url是多少，不管http协议）
        res = self.student_api.create_student(
            name = "黑盒张三",
            student_id = unique_id,
            age=22
        )

        # 如果返回结果不通过，返回报错原因
        if res.status_code != 201:
            print(f"创建失败，后端返回：{res.text}")

        # 2、断言状态码
        assert res.status_code == 201

        # 3、断言返回的json结构
        data = res.json()
        assert data['name'] == "黑盒张三"
        assert data['student_id'] == unique_id
        assert "id" in data #确保服务器生成了ID

    def test_get_students_list(self):
        """
        测试目标：查询列表
        """
        # 设置唯一学号，与上方同理
        unique_id = f"STU_{int(time.time())}_2"
        # 1、可能环境里已经有很多脏数据了
        # 先创建一个数据，确保有数据
        self.student_api.create_student("黑盒李四",unique_id)

        # 2、查询
        res = self.student_api.get_student()
        assert res.status_code == 200

        # 3、解析响应
        data = res.json()

        print(f"DEBUG RESPONSE: {data}")

        # 4、智能提取列表（兼容分页）
        # 逻辑：如果 data 是字典且包含 'results'，说明是分页数据，取 results 里的内容
        # 否则，假设 data 本身就是列表
        if isinstance(data, dict) and "results" in data:
            student_list = data["results"]
        elif isinstance(data, list):
            student_list = data
        else:
            student_list = []

        # 5、验证
        all_names = [s['name'] for s in student_list]
        assert "黑盒李四" in all_names

    def test_student_lifecycle_scenario(self):
        """
        测试场景：生命周期闭环 (CRUD)
        创建 -> 查询 -> 修改 -> 删除 -> 再查询(确认删除)
        """
        # ==========================================
        # 1. CREATE (创建)
        # ==========================================
        unique_id = f"STU_AUTO_{int(time.time())}"
        print(f"\n🚀 Step 1: 创建学生 {unique_id}")

        res_create = self.student_api.create_student(
            name="生命周期测试员",
            student_id=unique_id,
            age=18
        )
        assert res_create.status_code == 201

        # 🟢【核心修改点】
        # 要拿两个 ID：
        # db_id (30): 它是数据库的主键，专门用来拼 URL (GET /api/students/30/)
        # stu_no (STU_...): 它是业务学号，用来核对数据
        db_id = res_create.json()['id']
        stu_no = res_create.json()['student_id']

        # ==========================================
        # 2. READ (查询详情)
        # ==========================================
        print(f"🔍 Step 2: 查询学生 {db_id}")

        res_get = self.student_api.get_student_detail(db_id)
        assert res_get.status_code == 200
        assert res_get.json()['name'] == "生命周期测试员"

        # ==========================================
        # 3. UPDATE (修改)
        # ==========================================
        print(f"✏️ Step 3: 修改学生姓名 (使用 PATCH)")

        # ❌ 原代码 (PUT): 需要传一大堆
        # res_update = self.student_api.update_student(
        #     db_id,
        #     name="已修改的名字",
        #     student_id=stu_no,
        #     age=20,
        #     gender=1
        # )

        # ✅ 新代码 (PATCH):
        res_update = self.student_api.partial_update_student(
            db_id,  # 只要告诉我改谁
            name="已修改的名字"  # 只要告诉我改什么
        )

        assert res_update.status_code == 200
        assert res_update.json()['name'] == "已修改的名字"
        # 验证一下没传的字段是不是没变？
        assert res_update.json()['student_id'] == stu_no

        # ==========================================
        # 4. DELETE (删除)
        # ==========================================
        print(f"🗑️ Step 4: 删除学生")

        res_delete = self.student_api.delete_student(db_id)
        # 删除通常返回 204 (No Content)
        assert res_delete.status_code == 204

        # ==========================================
        # 5. VERIFY DELETE (确认已删除)
        # ==========================================
        print(f"👻 Step 5: 确认学生已消失")

        # 再次尝试查询，应该查不到
        res_check = self.student_api.get_student_detail(db_id)
        # 预期结果是 404 Not Found
        assert res_check.status_code == 404