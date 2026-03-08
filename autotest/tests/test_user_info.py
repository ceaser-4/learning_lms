from unittest.mock import patch
import redis
from autotest.services.user_info import get_user_profile

class TestHighAvailability:

    # 拦截Redis的get方法
    @patch("autotest.services.user_info.redis_client.get")
    # 拦截数据库的 get 方法，为了方便测试，也 Mock 掉
    @patch('autotest.services.user_info.Student.objects.get')
    def test_redis_down_fallback(self, mock_db_get, mock_redis_get):
        # 1. 设定剧本 A：只要一调 Redis，立马抛出连接失败异常！(破坏狂模式)
        mock_redis_get.side_effect = redis.ConnectionError("Connection refused")
        # 2. 设定剧本 B：假装数据库里能查到这个人
        mock_db_get.return_value = {"name": "罗翔", "id": 1}

        # 3. 运行代码
        result = get_user_profile(1)

        # 4. 断言：在 Redis 彻底崩溃的情况下，用户依然能拿到数据
        assert result["name"] == "罗翔"
        # 验证兜底逻辑确实被触发了（数据库被查了一次）
        mock_db_get.assert_called_once()