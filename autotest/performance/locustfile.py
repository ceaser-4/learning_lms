# autotest/performance/locustfile.py
from locust import HttpUser, task, between

class TeacherPlatformUser(HttpUser):
    # wait_time 模拟真实用户的操作停顿时间（1到3秒之间）
    wait_time = between(1, 3)

    # @task(2) 代表权重，这个动作（看列表）执行的概率是看详情的2倍
    @task(2)
    def view_teacher_list(self):
        """模拟高频动作：成百上千的用户同时刷新教师列表"""
        # catch_response=True 允许我们在代码里自己定义什么是“成功”
        with self.client.get("/api/teachers/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"查询失败，状态码: {response.status_code}")

    @task(1)
    def view_single_teacher(self):
        """模拟低频动作：部分用户点进某个老师的详情页"""
        with self.client.get("/api/teachers/1/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # 就算数据库里没这个老师，对服务器性能来说也是处理完了，算作压测成功
                response.success()
            else:
                response.failure(f"详情查询异常，状态码: {response.status_code}")