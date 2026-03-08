import requests

class PaymentService:
    def pay_order(self,order_id,amount):
        """
        模拟调用第三方支付接口（比如支付宝/微信）
        """
        url = "https://api.alipay.com/mock/pay"  # 假地址
        data = {
            "order_id": order_id,
            "amount": amount,
        }

        try:
            # 真是场景下，这段代码会发起网络请求
            response = requests.post(url,json=data,timeout=5)

            # 假设第三方返回200，且json里success=True 才算成功
            if response.status_code == 200 and response.json().get("success") is True:
                return "支付成功"
            else:
                return "支付失败"
        except requests.exceptions.Timeout:
            return "支付超时"
        except Exception as e:
            return f"支付异常：{str(e)}"