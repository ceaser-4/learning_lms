# autotest/utils/notify.py
import requests
import json


def send_dingtalk_report():
    # 🚨 把这里的 URL 换成你刚才复制的那个 Webhook 地址！
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=a446288903295bdf681b9ce67eda1300fe3313e4c6f5e6a789cb6454d56822d7"

    # 构建要发送的消息体（这里用的是 Markdown 格式，排版更漂亮）
    payload = {
        "msgtype": "markdown",
        "markdown": {
            # title 是手机通知栏里显示的标题
            "title": "测试通知",
            # text 是群里看到的正文（必须包含你刚才设定的关键词"测试通知"）
            "text": "### 🚀 自动化测试执行完毕 (测试通知)\n\n"
                    "> **运行环境**: Docker + Jenkins 自动化流水线\n\n"
                    "> **运行状态**: ✅ 构建成功\n\n"
                    "> **报告地址**: [点击查看 Allure 详细报告](http://localhost:8080/job/First_Demo/allure/)\n\n"
                    "请开发同学们注意查收！"
        }
    }

    # 必须告诉钉钉，我们发的是 JSON 格式的数据
    headers = {'Content-Type': 'application/json'}

    # 发送 POST 请求
    response = requests.post(url=webhook_url, headers=headers, data=json.dumps(payload))

    print(f"📡 钉钉通知发送结果: {response.text}")


# 本地调试开关
if __name__ == '__main__':
    send_dingtalk_report()