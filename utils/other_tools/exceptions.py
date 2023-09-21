# MyBaseFailure 类是一个基本的异常类，其他的异常都是它的子类，继承了它的特性和方法，如异常处理和错误信息的输出等。
class MyBaseFailure(Exception):
    pass
# 这个异常类是用来描述 Jsonpath 提取失败的情况。
class JsonpathExtractionFailed(MyBaseFailure):
    pass
# 这个异常类是用来表示由于某些原因找不到其所需的值而导致的“未找到”错误。
class NotFoundError(MyBaseFailure):
    pass
# 这个异常类是 FileNotFoundError 和 NotFoundError 两个异常类的子类。它是用来描述文件未找到时的情况。
class FileNotFound(FileNotFoundError, NotFoundError):
    pass
# 这个异常类是 NotFoundError 类的子类。它是用来描述在处理 SQL 数据时未找到数据表、字段或行的情况。
class SqlNotFound(NotFoundError):
    pass
# 这个异常类是用来描述断言失败的情况，即函数或方法的返回值与预期值不一致的情况。
class AssertTypeError(MyBaseFailure):
    pass
# 这个异常类是用来描述数据获取失败的情况。
class DataAcquisitionFailed(MyBaseFailure):
    pass
# 这个异常类是用来描述变量或函数参数类型错误的情况。
class ValueTypeError(MyBaseFailure):
    pass
# 这个异常类是用来描述发送消息失败的情况，例如在发送邮件或短信时出错。
class SendMessageError(MyBaseFailure):
    pass
# 这个异常类是用来描述在处理请求或操作时未找到所需值的情况。
class ValueNotFoundError(MyBaseFailure):
    pass