import smtplib
from email.mime.text import MIMEText
from utils.other_tools.allure_data.allure_report_data import TestMetrics, AllureFileClean
from utils import config


# 定义了一个名为SendEmail的类，用于发送测试结果邮件。
class SendEmail:
    """ 发送邮箱 """

    # 定义类的构造方法__init__，接受一个metrics参数，该参数的类型是TestMetrics。
    def __init__(self, metrics: TestMetrics):
        # 将metrics参数赋值给类属性self.metrics。
        self.metrics = metrics
        # 创建一个名为allure_data的类属性，并将AllureFileClean类的实例赋值给它。
        self.allure_data = AllureFileClean()
        # 创建一个名为CaseDetail的类属性，并调用AllureFileClean类实例的get_failed_cases_detail方法，并将返回值赋值给CaseDetail属性。
        self.CaseDetail = self.allure_data.get_failed_cases_detail()

    # @classmethod表示是一个类方法，也就是说，该方法是直接属于类定义的，而不是属于某个类对象的。类方法第一个参数通常是cls，表示类本身，而不是实例对象。通过cls参数可以操作类的属性和方法，也可以实例化类对象。
    @classmethod
    # 定义了一个类方法send_mail，cls表示类本身；user_list：接收邮件的邮箱列表；sub：邮件主题；content：邮件正文；返回值：None。
    def send_mail(cls, user_list: list, sub, content: str) -> None:
        """
        @param user_list: 发件人邮箱
        @param sub:
        @param content: 发送内容
        @return:
        """
        # 将发件人姓名和邮箱地址拼接成发件人字符串。
        user = "皓月" + "<" + config.email.send_user + ">"
        # 创建一个MIMEText对象，用于存储邮件内容。
        message = MIMEText(content, _subtype='plain', _charset='utf-8')
        # 为邮件添加主题、发件人和收件人。
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ";".join(user_list)
        # 创建SMTP对象，连接到SMTP服务器。
        server = smtplib.SMTP()
        server.connect(config.email.email_host)
        # 登录SMTP服务器。
        server.login(config.email.send_user, config.email.stamp_key)
        # 发送邮件，参数依次为发件人、收件人、邮件内容。
        server.sendmail(user, user_list, message.as_string())
        # 关闭与SMTP服务器的连接。
        server.close()

    # 定义了一个实例方法error_mail，用于发送异常邮件通知，self表示实例本身；error_message：报错信息；返回值：None。
    def error_mail(self, error_message: str) -> None:
        """
        执行异常邮件通知
        @param error_message: 报错信息
        @return:
        """
        # 从config文件中获取了邮件列表config.email.send_list，并将其 拆分为多个邮件地址。我们将这些地址的数组作为变量user_list。
        email = config.email.send_list
        user_list = email.split(',')  # 多个邮箱发送，config文件中直接添加  '2393557647@qq.com'
        # 通过将config文件中项目名称 config.project_name 和 "接口自动化执行异常通知" 连接在一起产生邮件的主题 sub。
        sub = config.project_name + "接口自动化执行异常通知"
        # 邮件的正文 content 为以 error_message 为内容的字符串。
        content = f"自动化测试执行完毕，程序中发现异常，请悉知。报错信息如下：\n{error_message}"
        # 使用另一个叫做 self.send_mail() 的私有函数来发送邮件。发送邮件接收三个参数：邮件收件人列表、邮件主题和邮件内容（以HTML格式发送）。
        self.send_mail(user_list, sub, content)

    # 总的来说，该函数是一个封装好的用于发送邮件通知的函数，当出现异常时可以调用该函数来通知相关人员。

    # 定义了一个 send_main 的类方法，不接受任何参数，不返回任何值。
    def send_main(self) -> None:
        """
        发送邮件
        :return:
        """
        # 获取邮件列表
        email = config.email.send_list
        user_list = email.split(',')  # 多个邮箱发送，yaml文件中直接添加  '2393557647@qq.com'

        # 生成邮件主题字符串，将config文件中的项目名称 config.project_name 和 "接口自动化报告" 进行连接。
        sub = config.project_name + "接口自动化报告"
        # 生成邮件正文内容，并使用 self.metrics 变量中的数据填充邮件正文。其中，self.allure_data.get_failed_cases_detail() 可以通过获取 Allure 报告的详细信息，包括测试失败原因等更多细节信息。
        content = f"""
        各位同事, 大家好:
            自动化用例执行完成，执行结果如下:
            用例运行总数: {self.metrics.total} 个
            通过用例个数: {self.metrics.passed} 个
            失败用例个数: {self.metrics.failed} 个
            异常用例个数: {self.metrics.broken} 个
            跳过用例个数: {self.metrics.skipped} 个
            成  功   率: {self.metrics.pass_rate} %
        {self.allure_data.get_failed_cases_detail()}
        **********************************
        jenkins地址：https://121.xx.xx.47:8989/login
        详细情况可登录jenkins平台查看，非相关负责人员可忽略此消息。谢谢。
        """
        # 使用 self.send_mail() 函数发送邮件，具体发送包括邮件收件人列表 user_list，邮件主题 sub 和邮件内容 content（以HTML格式）。
        self.send_mail(user_list, sub, content)