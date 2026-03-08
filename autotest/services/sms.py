import requests

def send_register_sms(phone_number,code):
    """真实对接云厂商的短信接口，极其烧钱"""
    url = "https://api.aliyun.com/send_sms"
    # 这里会产生真实的扣费和网络请求
    res = requests.post(url,json={"phone":phone_number,"code":code})
    return res.status_code == 200