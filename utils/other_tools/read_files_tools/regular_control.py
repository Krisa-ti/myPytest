import re
import datetime
import random
from datetime import date, timedelta, datetime
from jsonpath import jsonpath
from faker import Faker
from utils.logging_tool.log_control import ERROR


class Context:
    """ 正则替换 """

    # 用于初始化对象的属性。
    def __init__(self):
        # self.faker 是对象的一个属性，用于存储一个Faker对象，Faker 是一个Python库，用于生成随机数据，如姓名、地址、电话号码等。使用了 locale='zh_CN' 参数来指定生成的数据的语言环境为中文。
        self.faker = Faker(locale='zh_CN')

    @classmethod
    def generate_email(cls) -> str:
        """
        :return: 随机生成邮箱
        """
        Mailbox_number = 'register' + str(random.randint(0, 9999999)) + '@123.com'
        return Mailbox_number

    def generate_google_email(self) -> str:
        """
        :return: 随机生成Google邮箱
        """
        Google_email = 'google' + str(random.randint(0, 9999999)) + '@test.com'
        return Google_email

    def random_int(self) -> int:
        """
        :return: 随机数
        """
        _data = random.randint(0, 5000)
        return _data

    def get_phone(self) -> int:
        """
        :return: 随机生成手机号码
        """
        phone = self.faker.phone_number()
        return phone

    @classmethod
    def get_time(cls) -> str:
        """
        计算当前时间
        :return:
        """
        # 使用 datetime.now() 方法获取当前时间，然后使用 strftime() 方法将时间格式化为 '%Y-%m-%d %H:%M:%S' 的字符串格式。%Y 表示年份（4位数字），%m 表示月份（2位数字），%d 表示日期（2位数字），%H 表示小时（24小时制，2位数字），%M 表示分钟（2位数字），%S 表示秒（2位数字）。因此，now_time 变量将包含当前时间的字符串表示，格式为 '年-月-日 时:分:秒'。
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time

    # 装饰器，用于定义类方法。类方法与实例方法不同，类方法是针对整个类而不是实例的方法。
    @classmethod
    # 这是一个类方法，用于获取接口域名。-> str表示返回类型为字符串。
    def host(cls) -> str:
        from utils import config
        """ 获取接口域名 """
        # 返回config模块中的host变量。
        return config.host

    @classmethod
    # 这是一个类方法，用于获取app的host。-> str表示返回类型为字符串。
    def app_host(cls) -> str:
        from utils import config
        """获取app的host"""
        # 返回config模块中的app_host变量。
        return config.app_host


# 这是一个函数，用于提取sql中的json数据。
def sql_json(js_path, res):
    """ 提取 sql中的 json 数据 """
    # 这是一个jsonpath语法，用于从res变量中提取js_path指定的json数据。[0]表示取第一个元素。
    _json_data = jsonpath(res, js_path)[0]
    # 如果_json_data为False，即提取失败，则抛出ValueError异常。
    if _json_data is False:
        # 抛出ValueError异常，提示sql中的jsonpath获取失败。f""表示格式化字符串。
        raise ValueError(f"sql中的jsonpath获取失败 {res}, {js_path}")
    # 返回提取的json数据。
    return jsonpath(res, js_path)[0]


# 这是一个函数，用于处理sql中的依赖数据。
def sql_regular(value, res=None):
    """
    这里处理sql中的依赖数据，通过获取接口响应的jsonpath的值进行替换
    :param res: jsonpath使用的返回结果
    :param value:
    :return:
    """
    # 使用正则表达式查找value中以$json()格式包含的内容，并将其存储在sql_json_list列表中。
    sql_json_list = re.findall(r"\$json\((.*?)\)\$", value)

    # 循环遍历sql_json_list中的元素。
    for i in sql_json_list:
        # 使用正则表达式构造一个模式，用于匹配以$json()格式包含的内容。
        pattern = re.compile(r'\$json\(' + i.replace('$', "\$").replace('[', '\[') + r'\)\$')
        # 调用sql_json()函数获取json数据，并将其转换为字符串类型。
        key = str(sql_json(i, res))
        # 使用re.sub()函数将匹配到的内容替换成json数据中对应的值，替换次数为1。
        value = re.sub(pattern, key, value, count=1)

    # 返回替换后的value值。
    return value


# 定义了一个名为 cache_regular 的函数，用于通过正则表达式的方式读取缓存中的内容，参数为 value。
def cache_regular(value):
    from utils.cache_process.cache_control import CacheHandler

    """
    通过正则的方式，读取缓存中的内容
    例：$cache{login_init}
    :param value:
    :return:
    """
    # 正则表达式\$cache\{(.*?)\}用来匹配字符串中以$cache{}包含的内容，.*?表示匹配任意字符，()表示括号内的内容为需要匹配的内容。re.findall()方法返回一个列表，包含所有匹配的结果。
    # 正则获取 $cache{login_init}中的值 --> login_init
    regular_dates = re.findall(r"\$cache\{(.*?)\}", value)

    # for循环遍历regular_dates列表中的所有元素，即匹配到的所有缓存数据。
    for regular_data in regular_dates:
        # 定义了一个缓存数据类型的列表
        value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
        # 如果缓存数据的类型在value_types列表中，则将缓存数据类型和缓存数据名称分别提取出来
        if any(i in regular_data for i in value_types) is True:
            value_types = regular_data.split(":")[0]
            regular_data = regular_data.split(":")[1]
            # 使用re.compile()方法创建一个正则表达式对象pattern，用来匹配需要替换的字符串。
            pattern = re.compile(r'\'\$cache\{' + value_types.split(":")[0] + ":" + regular_data + r'\}\'')
        # 如果缓存数据的类型不在value_types列表中，则直接使用re.compile()方法创建一个正则表达式对象pattern，用来匹配需要替换的字符串。
        else:
            pattern = re.compile(
                r'\$cache\{' + regular_data.replace('$', "\$").replace('[', '\[') + r'\}'
            )
        try:
            # 使用CacheHandler.get_cache()方法读取缓存数据
            cache_data = CacheHandler.get_cache(regular_data)
            # 使用re.sub()方法将匹配到的字符串替换为缓存数据
            value = re.sub(pattern, str(cache_data), value)
        # 如果读取缓存数据或替换字符串过程中出现异常，则跳过并不处理。
        except Exception:
            pass
    # 将处理好的字符串作为函数的返回值。
    return value


# 定义了一个名为 regular 的函数，该函数接受一个参数 target。
def regular(target):
    """
    新版本
    使用正则替换请求数据
    :return:
    """
    try:
        # 定义了一个正则表达式，用于匹配字符串中的 "${{}}" 格式的内容。
        regular_pattern = r'\${{(.*?)}}'
        # 使用 while 循环，当字符串中还存在 "${{}}" 格式的内容时，继续循环。
        while re.findall(regular_pattern, target):
            # 使用 re.search() 函数在字符串中找到第一个匹配的 "${{}}" 格式的内容，并获取其中的关键字。
            key = re.search(regular_pattern, target).group(1)
            # 定义了一个列表，包含了可能出现的数据类型。
            value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
            # 如果关键字中包含了可能出现的数据类型，则执行下面的代码。
            if any(i in key for i in value_types) is True:
                # 从关键字中获取函数名。
                func_name = key.split(":")[1].split("(")[0]
                # 从关键字中获取参数列表字符串，并去除字符串末尾的 ")"。
                value_name = key.split(":")[1].split("(")[1][:-1]
                # 如果参数列表字符串为空，则执行下面的代码。
                if value_name == "":
                    # 从 Context 类中获取函数名为 func_name 的函数，并执行该函数，获取返回值。
                    value_data = getattr(Context(), func_name)()
                # 如果参数列表字符串不为空，则执行下面的代码。
                else:
                    # 从 Context 类中获取函数名为 func_name 的函数，并将参数列表字符串转换为参数列表，执行该函数，获取返回值。
                    value_data = getattr(Context(), func_name)(*value_name.split(","))
                # 定义正则表达式模式，用于匹配字符串中的 "'${{}}'" 格式的内容。
                regular_int_pattern = r'\'\${{(.*?)}}\''
                # 将字符串中第一个匹配的 "'${{}}'" 格式的内容替换为 value_data。
                target = re.sub(regular_int_pattern, str(value_data), target, 1)
            # 如果关键字中不包含可能出现的数据类型，则执行下面的代码。
            else:
                # 从关键字中获取函数名。
                func_name = key.split("(")[0]
                # 从关键字中获取参数列表字符串，并去除字符串末尾的 ")"。
                value_name = key.split("(")[1][:-1]
                # 如果参数列表字符串为空，则执行下面的代码。
                if value_name == "":
                    # 从 Context 类中获取函数名为 func_name 的函数，并执行该函数，获取返回值。
                    value_data = getattr(Context(), func_name)()

                # 如果参数列表字符串不为空，则执行下面的代码。
                else:
                    # 从 Context 类中获取函数名为 func_name 的函数，并将参数列表字符串转换为参数列表，执行该函数，获取返回值。
                    value_data = getattr(Context(), func_name)(*value_name.split(","))
                # 将字符串中第一个匹配的 "${{}}" 格式的内容替换为 value_data。
                target = re.sub(regular_pattern, str(value_data), target, 1)
        # 返回处理后的字符串。
        return target

    # 捕获 AttributeError 异常。
    except AttributeError:
        # 打印错误日志，提示未找到对应的替换的数据。
        ERROR.logger.error("未找到对应的替换的数据, 请检查数据是否正确 %s", target)
        # 抛出异常。
        raise
    # 捕获 IndexError 异常。
    except IndexError:
        # 打印错误日志，提示 yaml 中的 ${{}} 函数方法不正确。
        ERROR.logger.error("yaml中的 ${{}} 函数方法不正确，正确语法实例：${{get_time()}}")
        # 抛出异常。
        raise
