import datetime
from unittest.mock import patch
from autotest.services.coupon import use_coupon

class TestCoupon:

    # 拦截系统的“现在时间”
    @patch('autotest.services.coupon.datetime')
    def test_coupon_expired(self,mock_datetime):
        # 1. 设定剧本：强行篡改宇宙时间！把服务器当前时间修改到 2026年12月1日
        future_time = datetime.datetime(2026,12,1)
        mock_datetime.datetime.now.return_value = future_time

        # 2. 拿一张双十一过期的券来试
        expired_time = datetime.datetime(2026,11,11)
        result = use_coupon(expired_time)

        # 3、断言
        assert result == "优惠券已过期，无法使用"