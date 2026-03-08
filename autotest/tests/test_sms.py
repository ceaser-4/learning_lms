from unittest.mock import patch
from autotest.services.sms import send_register_sms

class TestUserRegister:

    # 偷偷把发短信的方法“阉割”掉
    @patch('autotest.services.sms.requests.post')
    def test_register_success(self, mock_post):
        # 设定剧本：假装云厂商返回了 200 (发送成功)
        mock_post.return_value.status_code = 200

        # 此时去跑注册流程，根本不会发起真实网络请求，白嫖成功！
        result = send_register_sms("13800138000", "1234")

        assert result is True
        # 进阶断言：我不仅要知道结果对不对，我还要查岗！
        # 检查代码到底有没有按预期去调用 requests.post，连传的参数都能查！
        mock_post.assert_called_once_with(
            "https://api.aliyun.com/send_sms",
            json={"phone": "13800138000", "code": "1234"}
        )