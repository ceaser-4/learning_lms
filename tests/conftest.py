import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient # 引入django的测试客户端


# @pytest.fixture: 这是一个装饰器，告诉 pytest 下面的函数是一个“工具”
# scope="function": 默认值。意思是每个调用它的测试函数执行前，都会运行一次这个 fixture
@pytest.fixture
def api_client():
    # 创建一个APIClient实例
    # 相当于打开了一个没有任何 Cookie、没有登录的浏览器。
    # 用来测试那些“不需要登录就能访问”的接口（如果有的话）。
    return APIClient()

@pytest.fixture
def auth_client(api_client):
    # # get_or_create: 如果数据库里有 'test_admin' 就拿出来，没有就创建一个。
    user , created = User.objects.get_or_create(username='test_admin')
    if created:
        user.set_password('test_admin')
        user.save()

    # 强制鉴权，用这个client发的所有请求都会自动通过IsAuthenticated 检查
    # force_authenticate 是 APIClient 特有的功能。
    # 它的意思是：跳过所有的密码验证、Token 验证，
    # 直接告诉后端：“我是 user，我有权限，让我过。”
    api_client.force_authenticate(user=user)

    return api_client