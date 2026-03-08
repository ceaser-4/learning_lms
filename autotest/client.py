import requests
from autotest.config import Config
from requests.auth import HTTPBasicAuth

class RestClient:
    """
    HTTP 请求基类
    作用：封装 requests，自动处理 URL 拼接、Session 保持、日志打印
    """
    def __init__(self):
        # 核心：使用session()而不是直接用requests
        # 作用：它会自动帮你保存  Cookie/SessionID
        # 只要登录一次，后面的请求都会自动带上身份信息，不用手动传token
        self.session = requests.Session()
        self.base_url = Config.BASE_URL

        self.session.auth = HTTPBasicAuth(Config.AUTH_USER, Config.AUTH_PASS)

    def request(self,method,path,**kwargs):
        """
        统一请求入口
        :param method: GET/POST/PUT/DELETE
        :param path: 接口路径 (如 /api/students/)
        :param kwargs: 其他参数 (json, params, headers)
        """
        # 自动拼接完整url
        url = self.base_url + path

        # 打印日志
        print(f"\n----------Request------------")
        print(f"METHOD: {method}")
        print(f"URL: {url}")
        print(f"DATA: {kwargs.get('json',kwargs.get('data'))}")

        try:
            # 发送真实请求
            # 这里调用的是requests.Session.request
            response = self.session.request(method,url,**kwargs)

            #打印响应
            print(f"---------------Response----------------")
            print(f"STATUS: {response.status_code}")
            print(f"BODY: {response.text}")

            return response

        except Exception as e:
            # 全局异常处理：如果断网了，或者服务器挂了
            print(f"❌ 致命错误: 接口请求失败 - {e}")
            raise e

    # 封装常用方法
    def get(self,path,**kwargs):
        return self.request('GET',path,**kwargs)

    def post(self,path,**kwargs):
        return self.request('POST',path,**kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request("PATCH", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)