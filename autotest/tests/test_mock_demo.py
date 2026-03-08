import pytest
from unittest.mock import patch,Mock
from autotest.services.payment import PaymentService

class TestPaymentService:
    # 场景1：模拟支付成功
    # @patch 的意思是：在这个测试函数执行期间
    # 把 'autotest.services.payment.requests.post' 这个方法
    # 偷偷换成一个假对象 (mock_post)
    @patch('autotest.services.payment.requests.post')
    def test_pay_success(self,mock_post):
        # 1. 设定剧本：我们要让那个假对象返回什么？
        # 我们模拟 response.status_code = 200
        mock_post.return_value.status_code = 200
        # 我们模拟 response.json() 返回字典
        mock_post.return_value.json.return_value = {"success": True}

        # 2、调用被测代码
        pay = PaymentService()
        # 注意：这里虽然代码里写的是 requests.post，但实际上调用的已经是我们的 mock_post 了
        result = pay.pay_order("ORDER_20260218",100)

        # 3、断言结果
        print(f"\n模拟成功场景的结果：{result}")
        assert result == "支付成功"

    # 场景2：模拟支付超时 (面试高频考点！)
    # 真实的超时很难复现，但用 Mock 一行代码就搞定
    @patch('autotest.services.payment.requests.post')
    def test_pay_timeout(self,mock_post):
        # 1. 设定剧本：这次我们不让它返回东西，而是直接抛出一个异常
        import requests
        mock_post.side_effect = requests.exceptions.Timeout("连接超时啦")

        # 2、调用被测代码
        pay = PaymentService()
        result = pay.pay_order("ORDER_TIMEOUT",100)

        # 3、断言结果
        print(f"模拟超时场景的结果: {result}")
        assert result == "支付超时"