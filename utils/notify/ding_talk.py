"""
钉钉通知封装
"""
import base64
import hashlib
import hmac
import time
import urllib.parse
from typing import Any, Text
from dingtalkchatbot.chatbot import DingtalkChatbot, FeedLink
from utils.other_tools.get_local_ip import get_host_ip
from utils.other_tools.allure_data.allure_report_data import AllureFileClean, TestMetrics
from utils import config


# 定义了一个名为DingTalkSendMsg的类。
class DingTalkSendMsg:
    """ 发送钉钉通知 """

    # 定义了一个实例化方法__init__，方法的第一个参数metrics是一个类型为TestMetrics的对象。
    def __init__(self, metrics: TestMetrics):
        # 将传入的metrics对象赋值给self.metrics。
        self.metrics = metrics
        # 生成一个时间戳，将其转换成字符串类型，并将其赋值给self.timeStamp。
        self.timeStamp = str(round(time.time() * 1000))

    # 总之，在DingTalkSendMsg类中，定义了一个实例化方法，在实例化时需要传入一个TestMetrics对象，并且在初始化的时候生成一个时间戳字符串存储在self.timeStamp中。

    # 这是一个函数定义的语句，函数名为xiao_ding，函数的第一个参数为self。
    def xiao_ding(self):
        # 这一行调用了该类中的get_sign方法，获取签名信息。将其赋值给变量sign。
        sign = self.get_sign()
        # 这一行从yaml文件中获取钉钉机器人的webhook，然后将时间戳、签名等参数拼接成一个完整的URL，并将其赋值给变量webhook。
        webhook = config.ding_talk.webhook + "&timestamp=" + self.timeStamp + "&sign=" + sign
        # 这一行用拼接好的URL调用DingtalkChatbot类的构造函数，创建一个聊天机器人实例对象，并将其返回。
        return DingtalkChatbot(webhook)

    # 综上所述，这是一个用于根据钉钉机器人的webhook、时间戳、签名等参数，创建一个DingTalk的发送机器人实例对象，并返回该对象的函数。

    # 这是一个方法定义语句，方法名为get_sign，第一个参数为self，返回一个字符串类型的密钥sign。
    def get_sign(self) -> Text:
        """
        根据时间戳 + "sign" 生成密钥
        :return:
        """
        # 这一行将self.timeStamp和钉钉配置中的密钥secret按照固定格式拼接成待加密的字符串string_to_sign，使用utf-8进行编码，并将结果赋值给变量string_to_sign。
        string_to_sign = f'{self.timeStamp}\n{config.ding_talk.secret}'.encode('utf-8')
        # 这一行使用加密模块hmac对待加密的字符串string_to_sign进行加密，使用config.ding_talk.secret作为密钥，加密算法使用SHA256，并将结果赋值给变量hmac_code。
        hmac_code = hmac.new(
            config.ding_talk.secret.encode('utf-8'),
            string_to_sign,
            digestmod=hashlib.sha256).digest()

        # 这一行对加密后的结果进行进一步处理，首先将其进行Base64编码，再进行URL转义，并将结果赋值给变量sign。
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        # 这一行返回生成的密钥sign。
        return sign

    # 综上所述，代码的作用是根据时间戳和配置中的密钥生成一个密钥字符串，并对其进行加密和处理，生成最终的密钥返回。

    # 这是一个方法定义语句，方法名为send_text，第一个参数为msg，表示需要发送的文本内容，第二个参数为可选参数mobiles，表示需要艾特的用户的电话号码，返回值为None。
    def send_text(
            self,
            msg: Text,
            mobiles=None
    ) -> None:
        """
        发送文本信息
        :param msg: 文本内容
        :param mobiles: 艾特用户电话
        :return:
        """
        # 这是一个条件语句，判断mobiles是否为空，如果为空则表示@所有人，执行下一步操作；如果不为空则执行其他操作。
        if not mobiles:
            # 这一行创建一个钉钉聊天机器人对象，并调用send_text方法向钉钉机器人发送文本消息，文本内容为msg，是否艾特所有人为True。
            self.xiao_ding().send_text(msg=msg, is_at_all=True)
        else:
            # 这是一个条件语句，判断mobiles是否为列表类型的数据，如果是，则执行下一步操作；如果不是，则执行下一步操作。
            if isinstance(mobiles, list):
                # 这一行调用钉钉聊天机器人对象的send_text方法，向钉钉机器人发送文本消息，并且@指定电话号码的用户，电话号码信息存储在参数at_mobiles中。
                self.xiao_ding().send_text(msg=msg, at_mobiles=mobiles)
            else:
                # 这一行抛出一个异常，提示mobiles的类型不正确。
                raise TypeError("mobiles类型错误 不是list类型.")

    # 综上所述，这段代码的作用是向指定的钉钉机器人发送文本信息，并@指定电话号码的用户。如果mobiles为Empty或None，则@所有人，否则@指定电话号码的用户。

    # 这是一个方法定义语句，方法名为send_link，它接收四个参数：title表示链接的标题，text表示链接的内容描述，message_url表示要发送的链接地址，pic_url表示链接的图片地址。该方法返回值为None。
    def send_link(
            self,
            title: Text,
            text: Text,
            message_url: Text,
            pic_url: Text
    ) -> None:
        """
        发送link通知
        :return:
        """
        # 这一行代码创建一个钉钉聊天机器人对象，通过调用钉钉聊天机器人对象的send_link方法来发送指定的链接信息。title参数表示链接的标题，text参数表示链接的内容描述，message_url参数表示要发送的链接地址，pic_url参数表示链接的图片地址。
        self.xiao_ding().send_link(
            title=title,
            text=text,
            message_url=message_url,
            pic_url=pic_url
        )

    # 综上，该方法的作用是以指定的格式，在钉钉聊天机器人上发送链接信息。

    # 这是一个方法定义语句，参数包括title表示消息的标题，msg表示消息的内容，mobiles表示提醒的对象（可以为空），is_at_all表示是否提醒全部对象（默认为False），该方法无返回值。
    def send_markdown(
            self,
            title: Text,
            msg: Text,
            mobiles=None,
            is_at_all=False
    ) -> None:
        """
        :param is_at_all:
        :param mobiles:
        :param title:
        :param msg:
        markdown 格式
        """

        # 这一行代码检查mobiles参数是否为空，如果为空则向is_at_all参数提到的@人员发送消息。
        if mobiles is None:
            # 如果mobiles参数为空，则调用self.xiao_ding().send_markdown方法，发送Markdown格式的消息，包括标题title和文本部分text，可以选择是否提醒所有人。
            self.xiao_ding().send_markdown(title=title, text=msg, is_at_all=is_at_all)
        else:
            # 这一行代码检查mobiles参数是否为列表类型，如果是，则向列表中的电话号码发送消息。
            if isinstance(mobiles, list):
                # 如果mobiles参数为列表类型，则调用self.xiao_ding().send_markdown方法，并在发出的消息中@指定号码。
                self.xiao_ding().send_markdown(title=title, text=msg, at_mobiles=mobiles)
            else:
                # 抛出错误
                raise TypeError("mobiles类型错误 不是list类型.")

    # 综上，该方法的作用是将指定的Markdown格式的内容发送到钉钉聊天机器人，如果没有指定对象则@所有人，否则@指定的列表内的号码。

    # 这是一个Python中的装饰器，用于表明该方法为静态方法，可以通过类名来调用，而不必实例化对象。
    @staticmethod
    # 这是一个静态方法定义语句，接收三个参数：title表示链接的标题，message_url表示要发送的链接地址，pic_url表示链接中的图片地址。该方法返回一个FeedLink对象。
    def feed_link(
            title: Text,
            message_url: Text,
            pic_url: Text
    ) -> Any:
        """ FeedLink 二次封装 """
        # 该行代码创建了一个FeedLink对象并将其返回。FeedLink对象包括title表示链接的标题，message_url表示要发送的链接地址，pic_url表示链接的图片地址。
        return FeedLink(
            title=title,
            message_url=message_url,
            pic_url=pic_url
        )

    # 综上，该方法的作用是将链接信息封装为FeedLink类型的对象，并返回此对象。

    # 这是一个方法定义语句，参数为*arg，表示参数个数不定，可以传入任意个数的参数；该方法返回值为空。
    def send_feed_link(self, *arg) -> None:
        """发送 feed_lik """

        # 该行代码调用了xiao_ding方法，并调用该方法的send_feed_card方法，将所有传入的FeedLink对象作为一个列表传递给send_feed_card方法。
        self.xiao_ding().send_feed_card(list(arg))

    # 综上，该方法的作用是将传入的多个FeedLink类型的对象列表一起发送给钉钉机器人，以展示多个链接预览信息

    # 定义了一个方法send_ding_notification，用于向钉钉机器人发送测试报告。
    def send_ding_notification(self):
        """ 发送钉钉报告通知 """
        # 定义了一个 bool 类型的变量is_at_all，初始化为 False。
        is_at_all = False
        # 如果有测试用例失败或异常情况，将变量is_at_all的值改为 True。
        if self.metrics.failed + self.metrics.broken > 0:
            is_at_all = True
        # 这是一个长的文本字符串，用于组合测试报告的各种信息，包括测试执行的项目名称、执行环境、执行人、执行结果等。
        text = f"#### {config.project_name}通知  " \
               f"\n\n>Python脚本任务: {config.project_name}" \
               f"\n\n>环境: {config.host}\n\n>" \
               f"执行人: {config.tester_name}" \
               f"\n\n>执行结果: {self.metrics.pass_rate}% " \
               f"\n\n>总用例数: {self.metrics.total} " \
               f"\n\n>成功用例数: {self.metrics.passed}" \
               f" \n\n>失败用例数: {self.metrics.failed} " \
               f" \n\n>异常用例数: {self.metrics.broken} " \
               f"\n\n>跳过用例数: {self.metrics.skipped}" \
               f" ![screenshot](" \
               f"https://static001.geekbang.org/infoq/07/07763aea42fc53fe752aef637db02da8.png" \
               f")\n" \
               f" > ###### 测试报告 [详情](http://{get_host_ip()}:8000/index.html) \n"
        # 这行代码实例化了一个DingTalkSendMsg对象，并调用该对象的send_markdown方法，将测试报告信息以 Markdown 格式发送给钉钉机器人。
        DingTalkSendMsg(AllureFileClean().get_case_count()).send_markdown(
            title="【接口自动化通知】",
            msg=text,
            is_at_all=is_at_all
        )
    # 综上，该方法的作用是生成测试报告信息，并将其以 Markdown 格式的文本发送给钉钉机器人。