import types
from enum import Enum, unique
from typing import Text, Dict, Callable, Union, Optional, List, Any
from dataclasses import dataclass
from pydantic import BaseModel


# 定义一个 NotificationType 枚举类。
class NotificationType(Enum):
    """ 自动化通知方式 """
    # 定义了5个枚举常量，分别对应自动化通知的5种方式，每个枚举常量都由名称和值组成。这里的值表示通知方式的代号，名称则表述了该通知方式的语义。
    DEFAULT = '0'
    DING_TALK = '1'
    WECHAT = '2'
    EMAIL = '3'
    FEI_SHU = '4'


# 使用装饰器 @dataclass 定义一个数据类 TestMetrics，该数据类包含了多个测试数据指标。
@dataclass
class TestMetrics:
    """ 用例执行数据 """
    # 使用 docstring 注释对数据类进行描述，表明该数据类用于表示用例执行数据。
    passed: int  # 表示通过的测试用例数
    failed: int  # 表示失败的测试用例数
    broken: int  # 表示中断的测试用例数
    skipped: int  # 表示跳过的测试用例数
    total: int  # 表示总共的测试用例数
    pass_rate: float  # 表示测试通过率
    time: Text  # 表示测试执行的时间


# 定义一个 RequestType 枚举类。
class RequestType(Enum):
    """
    request请求发送，请求参数的数据类型
    """
    # 使用 docstring 注释对枚举类进行描述，表明该枚举类用于定义请求参数的数据类型。定义了6个枚举常量，分别对应请求参数的6种数据类型。每个枚举常量都由名称和值组成。这里的值是字符串类型，表示不同的数据类型。
    JSON = "JSON"
    PARAMS = "PARAMS"
    DATA = "DATA"
    FILE = 'FILE'
    EXPORT = "EXPORT"
    NONE = "NONE"


# 定义一个 TestCaseEnum 枚举类。
class TestCaseEnum(Enum):
    # 定义了多个枚举常量，每个枚举常量都是一个元组类型，由两个元素组成。第一个元素表示测试用例中对应的字段名称，第二个元素表示该字段是否必需。
    URL = ("url", True)
    HOST = ("host", True)
    METHOD = ("method", True)
    DETAIL = ("detail", True)
    IS_RUN = ("is_run", True)
    HEADERS = ("headers", True)
    REQUEST_TYPE = ("requestType", True)
    DATA = ("data", True)
    DE_CASE = ("dependence_case", True)
    DE_CASE_DATA = ("dependence_case_data", False)
    CURRENT_RE_SET_CACHE = ("current_request_set_cache", False)
    SQL = ("sql", False)
    ASSERT_DATA = ("assert", True)
    SETUP_SQL = ("setup_sql", False)
    TEARDOWN = ("teardown", False)
    TEARDOWN_SQL = ("teardown_sql", False)
    SLEEP = ("sleep", False)


# 定义一个 Method 枚举类。
class Method(Enum):
    # 定义了7个枚举常量，每个常量都代表一个 HTTP 请求方法。常量名称即为请求方法名，常量值为对应的字符串类型的请求方法。
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTION = "OPTION"


# 定义了一个名为 load_module_functions 的函数，输入参数 module 为要处理的 Python 模块，函数返回值为一个字典类型，其中键为函数名称，值为函数所在的内存地址。
def load_module_functions(module) -> Dict[Text, Callable]:
    """ 获取 module中方法的名称和所在的内存地址 """
    # 先初始化一个名为 module_functions 的空字典。
    module_functions = {}

    # 使用内置函数 vars() 取出 module 模块中的所有属性，将其转换为字典类型，并使用 for 循环遍历其中的每一项。若遍历到的属性类型为函数类型，则将其加入到 module_functions 字典中，键为函数名称，值为函数所在的内存地址。
    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item
    # 将 module_functions 字典作为函数返回值返回。
    return module_functions


# 定义了一个 DependentType 枚举类，使用装饰器 @unique 来保证枚举常量的唯一性。
@unique
class DependentType(Enum):
    """
    数据依赖相关枚举
    """
    # 定义了4个枚举常量，常量名称即为相关数据的依赖类型，常量值为对应的字符串类型的依赖类型。
    RESPONSE = 'response'
    REQUEST = 'request'
    SQL_DATA = 'sqlData'
    CACHE = "cache"


# 定义了一个名为 Assert 的数据类，它继承了 BaseModel 类，即 Assert 类具有了 BaseModel 类的所有属性和方法。
class Assert(BaseModel):
    # 定义了 Assert 类的4个属性。其中，jsonpath 的类型为 Text，表示 JSON 路径；type 的类型为 Text，表示数据的类型；value 的类型为 Any，表示数据的值；AssertType 的类型为 Union[None, Text]，表示断言类型。
    jsonpath: Text
    type: Text
    value: Any
    AssertType: Union[None, Text] = None


# 此数据类 Assert 的作用是定义一个测试断言模型，其中 jsonpath 表示需要测试的数据在 JSON 文件中的路径，value 表示需要测试的数据的具体值，type 表示需要测试的数据的类型，例如字符串、数字等，AssertType 表示测试断言的类型，例如等于断言、不等断言等。使用数据类可以更加方便地处理这些数据，并在使用时有更好的类型提示和验证。


# 定义了一个名为 DependentData 的数据类，它同样继承了 BaseModel 类，即 DependentData 类也具有了 BaseModel 类的所有属性和方法。
class DependentData(BaseModel):
    # 定义了 DependentData 类的4个属性。其中，dependent_type 的类型为 Text，表示依赖的数据类型；jsonpath 的类型为 Text，表示依赖数据在 JSON 文件中的路径；set_cache 的类型为 Optional[Text]，表示需要将依赖数据缓存，可选参数；replace_key 的类型为 Optional[Text]，表示需要替换的依赖数据在 JSON 文件中的路径，可选参数。
    dependent_type: Text
    jsonpath: Text
    set_cache: Optional[Text]
    replace_key: Optional[Text]


# 此数据类 DependentData 的作用是定义测试用例中的数据依赖模型，其中 dependent_type 表示数据依赖类型，例如响应数据、请求数据等；jsonpath 表示需要依赖的数据在 JSON 文件中的路径；set_cache 表示依赖数据是否需要进行缓存；replace_key 表示需要替换的依赖数据在 JSON 文件中的路径。使用数据类可以更加方便地处理这些数据，并在使用时有更好的类型提示和验证。


# 定义了一个名为 DependentCaseData 的数据类，它继承了 BaseModel 类，即 DependentCaseData 类也具有了 BaseModel 类的所有属性和方法。
class DependentCaseData(BaseModel):
    # 定义了 DependentCaseData 类的2个属性。其中，case_id 的类型为 Text，表示测试用例的 ID；dependent_data 的类型为 Union[None, List[DependentData]]，表示测试用例所依赖的数据，可选参数，数据类型为 DependentData 列表。
    case_id: Text
    dependent_data: Union[None, List[DependentData]] = None


# 此数据类 DependentCaseData 的作用是定义测试用例所依赖的数据模型，其中 case_id 表示测试用例的 ID，dependent_data 表示测试用例所依赖的数据，可能有多个依赖数据，所以使用列表存储。DependentCaseData 数据类的属性 dependent_data 是一个可选参数，因为可能存在某些测试用例不需要依赖数据的情况。


# 定义了一个名为 ParamPrepare 的数据类，它继承了 BaseModel 类，即 ParamPrepare 类也具有了 BaseModel 类的所有属性和方法。
class ParamPrepare(BaseModel):
    # 定义了 ParamPrepare 类的3个属性。其中，dependent_type 的类型为 Text，表示依赖的数据类型；jsonpath 的类型为 Text，表示需要依赖数据在 JSON 文件中的路径；set_cache 的类型为 Text，表示需要将依赖数据进行缓存。
    dependent_type: Text
    jsonpath: Text
    set_cache: Text


# 此数据类 ParamPrepare 的作用是定义 API 的参数准备数据模型，其中 dependent_type 表示参数依赖的数据类型，例如响应数据、请求数据等；jsonpath 表示需要依赖的数据在 JSON 文件中的路径；set_cache 表示依赖数据是否需要进行缓存。使用数据类可以更加方便地处理这些数据，并在使用时有更好的类型提示和验证。

# 定义了一个名为 SendRequest 的数据类，它继承了 BaseModel 类，即 SendRequest 类也具有了 BaseModel 类的所有属性和方法。
class SendRequest(BaseModel):
    # 定义了 SendRequest 类的5个属性。其中，dependent_type 的类型为 Text，表示依赖的数据类型；jsonpath, cache_data, set_cache, 和 replace_key 的类型均为可选的 Optional[Text]。
    dependent_type: Text
    jsonpath: Optional[Text]
    cache_data: Optional[Text]
    set_cache: Optional[Text]
    replace_key: Optional[Text]


# 此数据类 SendRequest 的作用是定义 API 请求数据模型，其中 dependent_type 表示参数依赖的数据类型，例如响应数据、请求数据等；jsonpath 表示需要从依赖数据中提取的数据在 JSON 文件中的路径，由于该属性为可选参数，所以不一定所有的请求都需要依赖数据；cache_data 表示需要缓存的数据；set_cache 表示缓存的数据是否需要进行缓存，并可以为空；replace_key 表示需要替换的数据键名。


# 定义了一个名为 TearDown 的数据类，它继承了 BaseModel 类，即 TearDown 类也具有了 BaseModel 类的所有属性和方法。
class TearDown(BaseModel):
    # 定义了 TearDown 类的3个属性。其中，case_id 的类型为 Text，表示测试用例的 ID；param_prepare 和 send_request 的类型均为可选参数的列表类型，其中 param_prepare 表示参数准备数据模型的列表，send_request 表示 API 请求数据模型的列表。
    case_id: Text
    param_prepare: Optional[List["ParamPrepare"]]
    send_request: Optional[List["SendRequest"]]


# 此数据类 TearDown 的作用是定义 API 测试用例的后置条件数据模型，其中 case_id 表示测试用例的 ID；param_prepare 表示测试用例后置条件中所需的参数准备数据模型列表，它是可选参数，因为不是所有的测试用例都需要参数准备；send_request 则表示测试用例后置条件中 API 请求数据模型的列表，同样是可选参数。使用数据类可以更加方便地处理这些数据，并在使用时有更好的类型提示和验证，从而减少代码出错的可能。


# 定义了一个名为 CurrentRequestSetCache 的数据类，它继承了 BaseModel 类，即 CurrentRequestSetCache 类也具有了 BaseModel 类的所有属性和方法。
class CurrentRequestSetCache(BaseModel):
    # 定义了 CurrentRequestSetCache 类的3个属性。其中，type、jsonpath 和 name 的类型均为 Text，其中 type 表示当前缓存的类型，具体包括 response 和 request；jsonpath 表示需要从返回结果中提取的数据在 JSON 文件中的路径；name 表示需要缓存的数据的名称。
    type: Text
    jsonpath: Text
    name: Text


# 此数据类 CurrentRequestSetCache 的作用是定义 API 请求数据模型中当前请求需要缓存的数据模型，其中 type 表示缓存的类型，具体包括响应和请求；jsonpath 表示需要从响应结果或请求参数中提取的数据的路径，它是需要自己定义的；name 则表示缓存数据的名称。使用数据类可以更加方便地处理这些数据，并在使用时有更好的类型提示和验证，从而减少代码出错的可能。


# 定义了一个名为 TestCase 的数据类，它同样是继承自 BaseModel 类，即 TestCase 类也具有了 BaseModel 类的所有属性和方法。
class TestCase(BaseModel):
    url: Text  # 表示 API 的请求地址
    method: Text  # 表示请求方式，例如 GET、POST 等
    detail: Text  # 表示测试用例的详细信息
    assert_data: Union[Dict, Text]  # 表示需要进行断言的数据，可能为字典类型，也可能为文本类型
    headers: Union[None, Dict, Text] = {}  # 表示请求头，它是可选参数，默认值为空字典
    requestType: Text  # 表示请求的数据类型，例如 json、form data 等
    is_run: Union[None, bool, Text] = None  # 表示是否需要运行该测试用例，它是可选参数，默认值为 None
    data: Any = None  # 表示请求体数据，它是可选参数
    dependence_case: Union[None, bool] = False  # 表示该测试用例是否依赖其他用例，默认为 False
    dependence_case_data: Optional[Union[None, List["DependentCaseData"], Text]] = None  # 表示该测试用例依赖的其他用例的数据列表，默认为 None
    sql: List = None  # 表示该测试用例执行前需要执行的 SQL 语句列表，它是可选参数
    setup_sql: List = None  # 表示该测试用例执行完后需要执行的 SQL 语句列表，它是可选参数
    status_code: Optional[int] = None  # 表示请求返回的状态码，它是可选参数
    teardown_sql: Optional[List] = None  # 表示该测试用例执行完后需要执行的 SQL 语句列表，它是可选参数
    teardown: Union[List["TearDown"], None] = None  # 表示模拟测试数据的后置条件
    current_request_set_cache: Optional[List["CurrentRequestSetCache"]]  # 表示缓存当前请求需要的数据
    sleep: Optional[Union[int, float]]  # 表示请求完后需要等待的时间，它是可选参数


# 定义了一个名为 ResponseData 的数据类，它同样是继承自 BaseModel 类，即 ResponseData 类也具有了 BaseModel 类的所有属性和方法。
class ResponseData(BaseModel):
    url: Text  # 表示 API 的请求地址
    is_run: Union[None, bool, Text]  # 表示是否需要运行该测试用例，它是可选参数，默认值为 None
    detail: Text  # 表示测试用例的详细信息
    response_data: Text  # 表示响应结果的文本内容
    request_body: Any  # 表示请求体数据，它是可选参数
    method: Text  # 表示请求方式，例如 GET、POST 等
    sql_data: Dict  # 表示数据库执行后的结果数据，它是一个字典
    yaml_data: "TestCase"  # 表示该测试用例的详细信息，是一个 TestCase 实例
    headers: Dict  # 表示响应结果的请求头
    cookie: Dict  # 表示响应结果的 cookie 信息
    assert_data: Dict  # 表示需要进行断言的数据，是一个字典
    res_time: Union[int, float]  # 表示响应时间
    status_code: int  # 表示请求返回的状态码
    teardown: List["TearDown"] = None  # 表示模拟测试数据的后置条件
    teardown_sql: Union[None, List]  # 表示该测试用例执行完后需要执行的 SQL 语句列表，它是可选参数
    body: Any  # 表示响应结果的请求体数据


# 定义了一个名为 DingTalk 的数据类，它同样是继承自 BaseModel 类，即 DingTalk 类也具有了 BaseModel 类的所有属性和方法。
class DingTalk(BaseModel):
    # 定义了 DingTalk 类的两个属性
    webhook: Union[Text, None]  # 表示钉钉机器人的 Webhook 地址，是一个文本类型的可选参数，默认值为 None
    secret: Union[Text, None]  # 表示加签的密钥，是一个文本类型的可选参数，默认值为 None


# 这个数据类可以用来存储钉钉机器人的相关信息，方便程序中的调用和使用。由于这两个属性都是可选参数，所以在使用时需要注意判断是否为空。


# 定义了一个名为 MySqlDB 的数据类，它同样是继承自 BaseModel 类，即 MySqlDB 类也具有了 BaseModel 类的所有属性和方法。
class MySqlDB(BaseModel):
    switch: bool = False  # 表示该数据库是否需要连接，是一个布尔类型的可选参数，默认值为 False
    host: Union[Text, None] = None  # 表示数据库的地址，是一个文本类型的可选参数，默认值为 None
    user: Union[Text, None] = None  # 表示连接数据库的用户名，是一个文本类型的可选参数，默认值为 None
    password: Union[Text, None] = None  # 表示连接数据库的密码，是一个文本类型的可选参数，默认值为 None
    port: Union[int, None] = 3306  # 表示连接数据库的端口，是一个整型的可选参数，默认值为 3306


# 这个数据类可以用来存储 MySQL 数据库的相关信息，方便程序中的调用和使用。由于所有属性都是可选参数，所以在使用时需要注意判断是否为空。此外，通过在属性定义中设置默认值，可以方便地进行参数配置。


# 定义了一个名为 Webhook 的数据类，它同样是继承自 BaseModel 类，即 Webhook 类也具有了 BaseModel 类的所有属性和方法。
class Webhook(BaseModel):
    webhook: Union[Text, None]  # 表示 Webhook 地址，是一个文本类型的可选参数，默认值为 None


# 这个数据类可以用来存储 Webhook 的相关信息，方便程序中的调用和使用。由于 webhook 属性是一个可选参数，所以在使用时需要注意判断是否为空。


# 定义了一个名为 Email 的数据类，它同样是继承自 BaseModel 类，即 Email 类也具有了 BaseModel 类的所有属性和方法。
class Email(BaseModel):
    send_user: Union[Text, None]  # 表示发件人邮箱的用户名，是一个文本类型的可选参数，默认值为 None
    email_host: Union[Text, None]  # 表示邮件服务器的地址，是一个文本类型的可选参数，默认值为 None
    stamp_key: Union[Text, None]  # 表示发件人的密码或授权码，是一个文本类型的可选参数，默认值为 None
    send_list: Union[Text, None]  # 表示邮件的接收人列表，是一个文本类型的可选参数，默认值为 None


# 这个数据类可以用来存储发送邮件的相关信息，方便程序中的调用和使用。由于所有属性都是可选参数，所以在使用时需要注意判断是否为空。此外，通过在属性定义中设置默认值，可以方便地进行参数配置。


# 定义了一个名为 Config 的数据类，它同样是继承自 BaseModel 类，即 Config 类也具有了 BaseModel 类的所有属性和方法。
class Config(BaseModel):
    project_name: Text  # 表示项目的名称，是一个文本类型的必选参数
    env: Text  # 表示运行的环境，是一个文本类型的必选参数
    tester_name: Text  # 表示测试人员的姓名，是一个文本类型的必选参数
    notification_type: Text = '0'  # 表示通知的方式，是一个文本类型的可选参数，它的默认值为 '0'
    excel_report: bool  # 表示是否生成 Excel 报告，是一个布尔类型的必选参数
    ding_talk: "DingTalk"  # 表示钉钉机器人的相关信息，是一个 DingTalk 类的实例，是一个必选参数
    mysql_db: "MySqlDB"  # 表示 MySQL 数据库的相关信息，是一个 MySqlDB 类的实例，是一个必选参数
    mirror_source: Text  # 表示测试用例所在的镜像源，是一个文本类型的必选参数
    wechat: "Webhook"  # 表示微信机器人的相关信息，是一个 Webhook 类的实例，是一个必选参数
    email: "Email"  # 表示邮件相关信息，是一个 Email 类的实例，是一个必选参数
    lark: "Webhook"  # 表示飞书机器人的相关信息，是一个 Webhook 类的实例，是一个必选参数
    real_time_update_test_cases: bool = False  # 表示是否实时更新测试用例，是一个布尔类型的可选参数，它的默认值为 False
    host: Text  # 表示测试服务器的地址，是一个文本类型的必选参数
    app_host: Union[Text, None]  # 表示被测应用程序的地址，是一个文本类型的可选参数，默认值为 None


# 这个数据类封装了一个测试框架的配置信息，包括项目名称、测试环境、测试人员信息、通知方式、测试用例相关信息、被测应用程序相关信息等。可以通过实例化 Config 类来快速配置测试框架的相关信息。由于部分属性有默认值，因此在实例化时可以只传递必选参数。


# 定义了一个名为 AllureAttachmentType 的枚举类，它继承自 Python 内置的 Enum 类，表示这是一个枚举类。同时使用 @unique 修饰符确保枚举类成员的值各不相同。
@unique
class AllureAttachmentType(Enum):
    """
    allure 报告的文件类型枚举
    """
    # 定义了一个包含 19 个成员的枚举，每个成员表示一种 Allure 报告中的文件类型。其中，每个成员都由一个名称和一个值构成，名称即为成员名称（如 TEXT、CSV），而值则为成员的实际取值（如 "text"、"csv"）。枚举中的所有成员都是不可变的，例如不能重新赋值或删除成员。
    TEXT = "txt"
    CSV = "csv"
    TSV = "tsv"
    URI_LIST = "uri"

    HTML = "html"
    XML = "xml"
    JSON = "json"
    YAML = "yaml"
    PCAP = "pcap"

    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"

    MP4 = "mp4"
    OGG = "ogg"
    WEBM = "webm"

    PDF = "pdf"


# 这个枚举类可以用于定义 Allure 报告中的文件类型，所以在测试框架中被广泛使用。它可以帮助开发人员、测试人员和其他相关人员快速识别和解析 Allure 报告中包含的文件类型。


@unique
class AssertMethod(Enum):
    """断言类型"""
    # 是否相等
    equals = "=="
    # 判断实际结果小于预期结果
    less_than = "lt"
    # 判断实际结果小于等于预期结果
    less_than_or_equals = "le"
    # 判断实际结果大于预期结果
    greater_than = "gt"
    # 判断实际结果大于等于预期结果
    greater_than_or_equals = "ge"
    # 判断实际结果不等于预期结果
    not_equals = "not_eq"
    # 判断字符串是否相等
    string_equals = "str_eq"
    # 判断长度是否相等
    length_equals = "len_eq"
    # 判断长度大于
    length_greater_than = "len_gt"
    # 判断长度大于等于
    length_greater_than_or_equals = 'len_ge'
    # 判断长度小于
    length_less_than = "len_lt"
    # 判断长度小于等于
    length_less_than_or_equals = 'len_le'
    # 判断期望结果内容包含在实际结果中
    contains = "contains"
    # 判断实际结果包含在期望结果中
    contained_by = 'contained_by'
    # 检查响应内容的开头是否和预期结果内容的开头相等
    startswith = 'startswith'
    # 检查响应内容的结尾是否和预期结果内容相等
    endswith = 'endswith'
    # 去重无序判断是否相等
    setlist = 'setlist'
    # list转成str 去重无序判断是否相等
    str_set = 'str_set'
    # 可散列判断
    counter = 'counter'