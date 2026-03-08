from autotest.client import RestClient

class StudentApI(RestClient):
    """
    学生模块的接口封装
    """
    def create_student(self,name,student_id,gender=1,age=20):
        """
        业务动作：创建学生
        """
        data = {
            "name":name,
            "student_id":student_id,
            "gender":gender,
            "age":age
        }
        # 继承了 RestClient,直接用self.post
        return self.post("/api/students/", json=data)

    def get_student(self):
        """
        业务动作：获取所有学生
        """
        return self.get("/api/students/")

    def get_student_detail(self, pk):
        """查询单个学生详情"""
        # 假设接口是 /api/students/STU_123/
        return self.get(f"/api/students/{pk}/")

    def update_student(self, pk, **kwargs):
        """修改学生信息"""
        # 通常修改是用 PUT 或 PATCH，这里假设用 PUT
        return self.put(f"/api/students/{pk}/", json=kwargs)

    def delete_student(self, pk):
        """删除学生"""
        return self.delete(f"/api/students/{pk}/")

    def partial_update_student(self, pk, **kwargs):
        """
        局部修改：只改传进来的字段
        """
        # 注意：这里调用的是 self.patch
        return self.patch(f"/api/students/{pk}/", json=kwargs)

class TeacherApI(RestClient):
    def __init__(self):
        super().__init__()
