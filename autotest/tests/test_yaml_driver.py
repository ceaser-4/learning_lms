import pytest
from autotest.client import RestClient
from autotest.utils.yaml_loader import load_yaml_data

# 1、初始化一个客户端
client = RestClient()

# 2、读取YAML数据
test_data = load_yaml_data("teacher_cases.yaml")

class TestYamlDriver:
    # pytest参数化
    @pytest.mark.parametrize("case_info", test_data)
    def test_run_from_yaml(self, case_info):
        print(f"\n🚀 正在执行 YAML 用例: {case_info['case_name']}")

        #发送请求，动态获取YAML里的method，url，data
        res = client.request(
            method=case_info['method'],
            path=case_info['url'],
            json=case_info['data']
        )
        # 断言校验
        print(f"实际状态码: {res.status_code}, 预期: {case_info['expect']['status_code']}")
        assert res.status_code == case_info['expect']['status_code']

        # 数据清理逻辑(teardown)
        # 如果这是一个post请求，并且成功创建(201)
        if case_info['method'].upper() == "POST" and res.status_code == 201:
            created_id = res.json().get('id') #获取数据库生成的真实ID
            if created_id:
                # 拼装删除的URL，比如/api/teachers/5/
                delete_path = f"{case_info['url']}{created_id}/"
                print(f"🧹 触发自动清理: 正在删除刚刚创建的数据 (ID={created_id})")
                client.request(method="DELETE",path=delete_path)