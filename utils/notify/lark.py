"""
发送飞书通知
"""
import json
import logging
import time
import datetime
import requests
import urllib3
from utils.other_tools.allure_data.allure_report_data import TestMetrics
from utils import config

# 这行代码是用来关闭urllib3模块的警告提示，如果不加这行代码，当我们使用requests向HTTPS网站发起请求时，会提示警告信息。
urllib3.disable_warnings()

# 这是Python异常处理语法，在try的代码块中尝试执行代码，如果执行出现异常，则执行except中的异常处理代码块。
try:
    # 这行代码的作用是定义一个JSONDecodeError对象，用来处理在JSON解码过程中出现的异常。如果当前Python版本的标准库中不存在json.decoder.JSONDecodeError，则将该对象定义为ValueError。
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


# 通过上述处理，可以确保无论是在 Python 3.7 及 更早版本下，还是在 Python 3.8及更新版本下，都能正确处理 JSON 数据解码过程中出现的异常。


# 这是一个用于判断字符串是否为空的函数，content是传入的参数，用于判断字符串是否为空。
def is_not_null_and_blank_str(content):
    """
  非空字符串
  :param content: 字符串
  :return: 非空 - True，空 - False
  """
    # 判断content是否是一个非空字符串，其中content and content.strip()的结果是判断content是否有值，以及去掉字符串两端空格后是否有值。函数返回一个bool类型的结果。
    return bool(content and content.strip())


# 综上，该函数的作用是判断传入的字符串是否为空。如果为空字符串，函数返回 False；否则返回 True。


# 这是一个FeiShuTalkChatBot类的构造函数__init__，用于初始化FeiShuTalkChatBot类的实例变量。
class FeiShuTalkChatBot:
    """飞书机器人通知"""

    # metrics是TestMetrics类的实例变量，是用于记录测试结果的指标类的一个实例。构造函数，接收一个TestMetrics类型的参数metrics，并将其保存为FeiShuTalkChatBot类的实例变量metrics。
    def __init__(self, metrics: TestMetrics):
        self.metrics = metrics

    # 综上，这个类是用于飞书机器人通知，并且将测试结果的指标类作为实例变量来保存，方便后续调用。

    # 接收一个字符类型的参数msg，表示要发送的文本消息。
    def send_text(self, msg: str):
        """
    消息类型为text类型
    :param msg: 消息内容
    :return: 返回消息发送结果
    """
        # 定义一个字典类型的变量data，表示要发送的消息类型为"text"。
        data = {"msg_type": "text", "at": {}}
        # 使用下面定义好的函数is_not_null_and_blank_str判断msg是否为空。
        if is_not_null_and_blank_str(msg):
            # 如果msg非空，将msg作为文本内容添加到data的content中。
            data["content"] = {"text": msg}
        else:
            # 如果msg为空，输出日志和错误信息。
            logging.error("text类型，消息内容不能为空！")
            raise ValueError("text类型，消息内容不能为空！")
        # 这是一个Python内置的logging库，用来打印和记录日志信息。通过设置logging的不同级别，可以控制输出不同类型的日志信息，如调试信息、错误信息等。这里使用的是调试信息级别（debug），用来输出程序运行时的详细信息。'text类型：%s'，这是一个格式化字符串，其中%s是一个占位符，表示这个位置可以被任何类型的数据替换。具体替换的数据是在后面的参数中传入的，即data。
        logging.debug('text类型：%s', data)
        # 调用类中的post方法，将发送文本消息的请求发送出去，并返回发送结果。
        return self.post()

    # 综上，send_text方法是用于发送文本消息的，并且判断了msg是否为空。如果为空，则输出错误信息并抛出异常；否则，发送文本消息，并返回发送结果。

    def post(self):
        """
    发送消息（内容UTF-8编码）
    :return: 返回消息发送结果
    """
        # 用于创建一个字典 rich_text，包含需要发送的消息内容。 字典中包含“send“，”text“和”at“等字典， text又包含了标题、测试人员姓名、测试环境等字符串，还包含一个记录各种数值数据的列表。这些数值数据包括成功率、通过的用例数、失败的用例数、异常的用例数和当前时间等。其中的值都是从配置文件中获取的，例如 config.tester_name 和 config.env。最后一项是一张测试结果的图片，图片的地址可以从远程服务器上获取。
        rich_text = {
            "email": "2393557647@qq.com",
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "【自动化测试通知】",
                        "content": [
                            [
                                {
                                    "tag": "a",
                                    "text": "测试报告",
                                    "href": "https://192.168.xx.72:8080"
                                },
                                {
                                    "tag": "at",
                                    "user_id": "ou_18eac85d35a26f989317ad4f02e8bbbb"
                                    # "text":"皓月"
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": "测试  人员 : "
                                },
                                {
                                    "tag": "text",
                                    "text": f"{config.tester_name}"
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": "运行  环境 : "
                                },
                                {
                                    "tag": "text",
                                    "text": f"{config.env}"
                                }
                            ],
                            [{
                                "tag": "text",
                                "text": "成   功   率 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.pass_rate} %"
                                }],  # 成功率

                            [{
                                "tag": "text",
                                "text": "成功用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.passed}"
                                }],  # 成功用例数

                            [{
                                "tag": "text",
                                "text": "失败用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.failed}"
                                }],  # 失败用例数
                            [{
                                "tag": "text",
                                "text": "异常用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.failed}"
                                }],  # 损坏用例数
                            [
                                {
                                    "tag": "text",
                                    "text": "时  间 : "
                                },
                                {
                                    "tag": "text",
                                    "text": f"{datetime.datetime.now().strftime('%Y-%m-%d')}"
                                }
                            ],

                            [
                                {
                                    "tag": "img",
                                    "image_key": "d640eeea-4d2f-4cb3-88d8-c964fab53987",
                                    "width": 300,
                                    "height": 300
                                }
                            ]
                        ]
                    }
                }
            }
        }
        # 字典 headers 用于存储向服务器发送请求时的请求头信息。在这个字典中，我们指定了消息为 Json 类型，同时指定编码。
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        # 消息内容被转化为Json格式，并赋给变量post_data。
        post_data = json.dumps(rich_text)
        # 我们使用requests库中的post()方法发送一个POST请求，请求包含了上面提到的内容，包括飞书机器人的连接地址、请求头信息、发送的数据内容。 这里的标志verify=False用于禁用SSL安全，可用于自签名的SSL证书。
        response = requests.post(
            config.lark.webhook,
            headers=headers,
            data=post_data,
            verify=False
        )
        # 我们使用 json() 方法将响应转换为 Json 格式并赋给变量 result。
        result = response.json()

        # 如果返回的结果字典中键 ‘StatusCode’ 对应的值不为0，则代表发送失败。
        if result.get('StatusCode') != 0:
            # 我们获取当前时间 time_now，同时检查响应结果字典中是否有 errmsg 这个键，如果有这个键，则将值赋给变量 result_msg，否则赋值为未知异常。
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            result_msg = result['errmsg'] if result.get('errmsg', False) else '未知异常'
            # 我们定义了一个 error_data 变量，包含一个消息文本字典。此字典中定义了消息内容、消息类型和是否需要 at。如果消息发送失败，则需要通过此字典向管理员群发送消息通知。
            error_data = {
                "msgtype": "text",
                "text": {
                    "content": f"[注意-自动通知]飞书机器人消息发送失败，时间：{time_now}，"
                               f"原因：{result_msg}，请及时跟进，谢谢!"
                },
                "at": {
                    "isAtAll": False
                }
            }
            # 如果出现了消息发送失败的情况，则使用 Python 标准库的 logging 模块，记录细节日志（使用 "error" 级别）。同时将错误信息的内容附加到日志消息中去。
            logging.error("消息发送失败，自动通知：%s", error_data)
            # 我们使用requests库向飞书机器人的Webhook地址发送错误消息。此时再次发送消息会通过其他通道（例如短信或者微信）通知管理员，提醒他们尽快解决这个问题。
            requests.post(config.lark.webhook, headers=headers, data=json.dumps(error_data))
        # 最后返回的是响应结果字典 result，包括响应消息是否成功、成功/失败的消息和其他相关的响应元数据。
        return result