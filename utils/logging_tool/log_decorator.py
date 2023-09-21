"""
日志装饰器，控制程序日志输入，默认为 True
如设置 False，则程序不会打印日志
"""
import ast
from functools import wraps
from utils.read_files_tools.regular_control import cache_regular
from utils.logging_tool.log_control import INFO, ERROR


# 定义了一个装饰器函数log_decorator()，并对参数switch进行了注释。
def log_decorator(switch: bool):
    """
    封装日志装饰器, 打印请求信息
    :param switch: 定义日志开关
    :return:
    """

    # 这里使用了Python的高级特性——装饰器。首先定义了一个内层函数（swapper），并将其作为参数返回。swapper函数将用来替代被装饰的原函数（func）进行执行。
    def decorator(func):
        # 保留原函数的一些属性，如函数名和帮助文档
        @wraps(func)
        def swapper(*args, **kwargs):

            # 判断日志为开启状态，才打印日志，这里调用了原函数，并将其返回值赋给了res变量。
            res = func(*args, **kwargs)
            # 判断日志开关为开启状态，这里判断日志开关switch是否为True（即是否需要打印日志）。
            if switch:
                # 这里定义了一个日志信息的字符串_log_msg，用于记录请求的详细信息。使用多个格式化字符串（以斜杠\连接）将请求的各个方面（如请求路径、请求方式等）格式化成字符串，并用换行符连接在一起。具体内容可以根据需要进行增删改。
                _log_msg = f"\n======================================================\n" \
                           f"用例标题: {res.detail}\n" \
                           f"请求路径: {res.url}\n" \
                           f"请求方式: {res.method}\n" \
                           f"请求头:   {res.headers}\n" \
                           f"请求内容: {res.request_body}\n" \
                           f"接口响应内容: {res.response_data}\n" \
                           f"接口响应时长: {res.res_time} ms\n" \
                           f"Http状态码: {res.status_code}\n" \
                           "====================================================="
                # 这里的cache_regular()是一个缓存函数的调用，它的作用是将res.is_run转换成字符串并加密缓存，具体实现过程可以简单理解成它用于优化性能。ast.literal_eval()函数可以安全地解析成Python字面量的字符串，并将其转换成相应的数据类型。因为res.is_run可能是一个bool值或None，所以这里需要将解析后的数据赋值给变量_is_run。
                _is_run = ast.literal_eval(cache_regular(str(res.is_run)))
                # 这里判断应该将日志信息记录在哪个日志文件中。如果用例执行成功且res.is_run为True或None，则将日志信息记录到INFO日志文件中并进行绿色输出。
                if _is_run in (True, None) and res.status_code == 200:
                    INFO.logger.info(_log_msg)
                # 如果用例执行失败，则将日志信息记录到ERROR日志文件中，并进行红色输出。
                else:
                    ERROR.logger.error(_log_msg)
            # 将原函数（func）的返回值返回给外层函数使用。
            return res

        # 返回内部函数swapper
        return swapper

    # 返回嵌套函数decorator
    return decorator