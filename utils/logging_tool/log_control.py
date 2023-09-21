"""
日志封装，可设置不同等级的日志颜色
"""
import logging
from logging import handlers
from typing import Text
import colorlog
import time
from common.setting import ensure_path_sep


# 定义了一个名为LogHandler的类，用来封装日志的打印。
class LogHandler:
    # 日志级别关系映射
    # 这个类属性定义了日志级别关系映射。这个映射是一个字典，将日志级别名称映射到对应的 Python 标准库 logging 中定义的日志级别常量。
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    # 这个方法名叫做 __init__，用于初始化 LogHandler 实例。

    '''
    这个方法定义了四个参数：filename：日志文件名，类型为字符串，用于指定日志文件的名称。level：日志记录的级别，类型为字符串，默认值为
    info，表示只记录
    info
    以上的日志等级。when：日志文件切割时间，类型为字符串，表示日志文件按照什么样的时间长度进行切割，默认值为
    D，表示按照天进行切割。fmt：日志输出格式，类型为字符串，表示记录日志时使用的格式化输出字符串。
    '''

    def __init__(
            self,
            filename: Text,
            level: Text = "info",
            when: Text = "D",
            fmt: Text = "%(levelname)-8s%(asctime)s%(name)s:%(filename)s:%(lineno)d %(message)s"
    ):
        # 这里调用了logging.getLogger()方法，并使用filename作为参数获得了一个logger对象，用来记录日志。
        self.logger = logging.getLogger(filename)

        # 这里调用了类中定义的log_color()方法，并将返回的格式对象赋给了formatter变量。
        formatter = self.log_color()
        # 设置日志格式
        format_str = logging.Formatter(fmt)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 往屏幕上输出
        screen_output = logging.StreamHandler()
        # 设置屏幕上显示的格式
        screen_output.setFormatter(formatter)
        # 往文件里写入#指定间隔时间自动生成文件的处理器。构造函数中的参数 filename 表示日志文件的完整路径，when 表示日志轮转的时间间隔，backupCount 表示日志文件的备份个数（即保留多少个历史日志文件），encoding 表示日志文件的编码方式。
        time_rotating = handlers.TimedRotatingFileHandler(
            filename=filename,
            when=when,
            backupCount=3,
            encoding='utf-8'
        )
        # 设置文件里写入的格式
        time_rotating.setFormatter(format_str)
        # 把对象加到logger里
        self.logger.addHandler(screen_output)
        self.logger.addHandler(time_rotating)
        self.log_path = ensure_path_sep('\\logs\\log.log')

    # @classmethod 装饰器用于将一个普通的方法转换为类方法，使其能够访问类属性，而不仅仅是实例属性。在类方法中，我们可以通过 cls 参数来直接访问类属性，而不需要创建类的实例对象。
    @classmethod
    def log_color(cls):
        """ 设置日志颜色 """
        # 定义了一个字典 log_colors_config，它包含了五个不同级别的日志消息，以及对应的颜色。
        log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }

        # 创建了一个基于颜色的日志格式化器对象 formatter。该对象的格式与前面提到的方法相同，不同之处仅在于我们将其定义为一个类方法，而非函数。
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
            log_colors=log_colors_config
        )
        # 将 formatter 对象返回，以便其他方法或者类使用它来格式化日志消息。
        return formatter


# 用 time.strftime() 函数获取当前系统时间，并将其转换为 %Y-%m-%d 格式的日期字符串，赋值给 now_time_day 变量。
now_time_day = time.strftime("%Y-%m-%d", time.localtime())
# 定义一个 INFO 变量，使用 LogHandler 类初始化一个 LogHandler 对象，并指定日志文件路径和日志级别参数。ensure_path_sep() 函数用于确保日志文件路径中使用的是正确的路径分隔符，“/” 或 “\”。
INFO = LogHandler(ensure_path_sep(f"\\logs\\info-{now_time_day}.log"), level='info')
# 定义一个 ERROR 变量，使用 LogHandler 类初始化一个 LogHandler 对象，并指定日志文件路径和日志级别参数。
ERROR = LogHandler(ensure_path_sep(f"\\logs\\error-{now_time_day}.log"), level='error')
# 定义一个 WARNING 变量，使用 LogHandler 类初始化一个 LogHandler 对象，并指定日志文件路径但未指定日志级别参数，此时默认记录 WARNING 级别及以上的日志消息。
WARNING = LogHandler(ensure_path_sep(f'\\logs\\warning-{now_time_day}.log'))