"""
统计请求运行时长装饰器，如请求响应时间超时
程序中会输入红色日志，提示时间 http 请求超时，默认时长为 3000ms
"""
from utils.logging_tool.log_control import ERROR


# 这是装饰器函数的定义，接收一个整数参数number表示函数预期运行时间，单位为毫秒。参数类型注解int表示该参数应为整数类型。
def execution_duration(number: int):
    """
    封装统计函数执行时间装饰器
    :param number: 函数预计运行时长
    :return:
    """

    # 装饰器的内部函数decorator，接收一个函数作为参数，并返回一个新函数swapper。
    def decorator(func):
        # 这里定义了新函数swapper，它接收任意数量的位置参数(*args)和关键字参数(**kwargs)。这些参数将在被装饰的函数调用时被传递给它。
        def swapper(*args, **kwargs):
            # 这里调用了被装饰的函数func，并传入了之前定义的位置和关键字参数。函数调用的返回结果保存在一个变量res中。
            res = func(*args, **kwargs)
            # 在调用完被装饰的函数后，从返回结果res中获取该函数的时间戳属性，用于后续计算函数的运行时间。
            run_time = res.res_time
            # 这里用获取的运行时间和预期时间number比较，如果运行时间超时了number，就打印错误信息。具体来说，输出一条警告日志，其中包含了运行时间、测试用例数据以及一些分隔符，易于查看和定位问题。
            if run_time > number:
                ERROR.logger.error(
                    "\n==============================================\n"
                    "测试用例执行时间较长，请关注.\n"
                    "函数运行时间: %s ms\n"
                    "测试用例相关数据: %s\n"
                    "================================================="
                    , run_time, res)
            # 将函数的返回值res返回回去。
            return res

        # 将新的函数swapper返回回去，以便在后续的函数中调用。
        return swapper

    # 将内部函数decorator返回，作为最终的装饰器函数。这个函数用于封装待装饰的函数，以统计其运行时间。
    return decorator