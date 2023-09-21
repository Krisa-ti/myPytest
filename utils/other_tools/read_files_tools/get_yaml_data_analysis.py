from typing import Union, Text, List
from utils.read_files_tools.yaml_control import GetYamlData
from utils.other_tools.models import TestCase
from utils.cache_process.cache_control import CacheHandler
from utils import config
from utils.other_tools.models import RequestType, Method, TestCaseEnum
import os


class CaseDataCheck:
    """
    yaml 数据解析, 判断数据填写是否符合规范
    """

    # 类的构造方法，接收一个参数file_path，用于指定yaml文件的路径。
    def __init__(self, file_path):
        # 将传入的file_path赋值给实例变量self.file_path，以便在类的其他方法中使用。
        self.file_path = file_path
        # 判断指定的文件路径是否存在，如果不存在则抛出FileNotFoundError异常。
        if os.path.exists(self.file_path) is False:
            raise FileNotFoundError("用例地址未找到")

        # 初始化一个实例变量self.case_data，用于存储解析后的yaml数据。
        self.case_data = None
        # 初始化一个实例变量self.case_id，用于存储当前解析的用例ID。
        self.case_id = None

    # 定义一个名为_assert的方法，接收一个参数attr，用于指定需要判断的参数是否存在。
    def _assert(self, attr: Text):
        # 判断指定的参数是否在yaml数据的keys中存在，如果不存在则抛出异常，提示缺少该参数。
        assert attr in self.case_data.keys(), (
            f"用例ID为 {self.case_id} 的用例中缺少 {attr} 参数，请确认用例内容是否编写规范."
            f"当前用例文件路径：{self.file_path}"
        )

    # 定义一个名为check_params_exit的方法，用于检查yaml数据中是否缺少必要的参数。
    def check_params_exit(self):
        # 遍历TestCaseEnum枚举中所有的成员。
        for enum in list(TestCaseEnum._value2member_map_.keys()):
            # 判断枚举成员是否是必要的参数。
            if enum[1]:
                # 调用_assert方法，判断当前枚举成员对应的参数是否存在。
                self._assert(enum[0])

    # 定义一个名为check_params_right的方法，接收两个参数enum_name和attr，用于检查参数是否填写正确。
    def check_params_right(self, enum_name, attr):
        # 获取枚举成员的所有名称。
        _member_names_ = enum_name._member_names_
        # 判断枚举成员是否包含指定的参数，如果不包含则抛出异常，提示参数填写错误。
        assert attr.upper() in _member_names_, (
            f"用例ID为 {self.case_id} 的用例中 {attr} 填写不正确，"
            f"当前框架中只支持 {_member_names_} 类型."
            f"如需新增 method 类型，请联系管理员."
            f"当前用例文件路径：{self.file_path}"
        )
        # 返回大写的参数名称。
        return attr.upper()

    # 装饰器，将方法转换成属性，以便在调用时不需要使用括号。
    @property
    # 定义一个名为get_method的属性方法，用于获取yaml数据中的请求方法。
    def get_method(self) -> Text:

        # 调用check_params_right方法，检查请求方法是否填写正确。
        return self.check_params_right(
            # 枚举类型，指定参数类型为请求方法。
            Method,
            # 从yaml数据中获取请求方法。
            self.case_data.get(TestCaseEnum.METHOD.value[0])
        )

    @property
    # 定义一个名为get_host的属性方法，用于获取完整的请求地址。
    def get_host(self) -> Text:
        # 拼接请求地址，包含主机地址和请求路径。
        host = (
            # 从yaml数据中获取主机地址。
                self.case_data.get(TestCaseEnum.HOST.value[0]) +
                # 从yaml数据中获取请求路径。
                self.case_data.get(TestCaseEnum.URL.value[0])
        )
        # 返回完整的请求地址。
        return host

    @property
    # 定义一个名为get_request_type的属性方法，用于获取yaml数据中的请求类型。
    def get_request_type(self):
        # 调用check_params_right方法，检查请求类型是否填写正确。
        return self.check_params_right(
            # 枚举类型，指定参数类型为请求类型。
            RequestType,
            # 从yaml数据中获取请求类型。
            self.case_data.get(TestCaseEnum.REQUEST_TYPE.value[0])
        )

    @property
    # 定义了一个名为get_dependence_case_data的方法，该方法不需要传入参数，属于类方法。
    def get_dependence_case_data(self):
        # 从self.case_data中获取DE_CASE的值，赋值给变量_dep_data。
        _dep_data = self.case_data.get(TestCaseEnum.DE_CASE.value[0])
        # 如果_dep_data存在。
        if _dep_data:
            # 断言self.case_data中是否存在DE_CASE_DATA的值，如果不存在，抛出异常。
            assert self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0]) is not None, (
                f"程序中检测到您的 case_id 为 {self.case_id} 的用例存在依赖，但是 {_dep_data} 缺少依赖数据."
                f"如已填写，请检查缩进是否正确， 用例路径: {self.file_path}"
            )

        # @返回self.case_data中的DE_CASE_DATA的值。
        return self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0])

    @property
    # 定义了一个名为get_assert的方法，该方法不需要传入参数，属于类方法。
    def get_assert(self):
        # 从self.case_data中获取ASSERT_DATA的值，赋值给变量_assert_data。
        _assert_data = self.case_data.get(TestCaseEnum.ASSERT_DATA.value[0])
        # 断言_assert_data是否存在，如果不存在，抛出异常。
        assert _assert_data is not None, (
            f"用例ID 为 {self.case_id} 未添加断言，用例路径: {self.file_path}"
        )
        # 返回_assert_data的值。
        return _assert_data

    @property
    # 定义了一个名为get_sql的方法，该方法不需要传入参数，属于类方法。
    def get_sql(self):
        # 从self.case_data中获取SQL的值，赋值给变量_sql。
        _sql = self.case_data.get(TestCaseEnum.SQL.value[0])
        # 判断数据库开关为开启状态，并且sql不为空
        if config.mysql_db.switch and _sql is None:
            # 返回None。
            return None
        # 返回_sql的值。
        return _sql


# 定义了一个名为case_process的方法，需要传入一个case_id_switch参数，属于类方法。
def case_process(self, case_id_switch: Union[None, bool] = None):
    # 从self.file_path中获取yaml文件中的数据，赋值给变量data。
    data = GetYamlData(self.file_path).get_yaml_data()
    case_list = []
    # 循环遍历data中的每一个元素，赋值给变量key和values。
    for key, values in data.items():
        # 如果key不等于case_common。
        if key != 'case_common':
            # 将values赋值给self.case_data。
            self.case_data = values
            # 将key赋值给self.case_id。
            self.case_id = key
            # 调用CaseDataCheck类中的check_params_exit方法，检查yaml文件中的参数是否正确。
            super().check_params_exit()
            # 定义一个字典case_date，用于存储每一个测试用例的数据。
            case_date = {
                'method': self.get_method,  # 获取请求方法。
                'is_run': self.case_data.get(TestCaseEnum.IS_RUN.value[0]),  # 获取是否执行该测试用例。
                'url': self.get_host,  # 获取请求url。
                'detail': self.case_data.get(TestCaseEnum.DETAIL.value[0]),  # 获取测试用例的描述信息。
                'headers': self.case_data.get(TestCaseEnum.HEADERS.value[0]),  # 获取请求头信息。
                'requestType': super().get_request_type,  # 获取请求类型。
                'data': self.case_data.get(TestCaseEnum.DATA.value[0]),  # 获取请求数据。
                'dependence_case': self.case_data.get(TestCaseEnum.DE_CASE.value[0]),  # 获取依赖的测试用例。
                'dependence_case_data': self.get_dependence_case_data,  # 获取依赖测试用例的返回数据。
                "current_request_set_cache": self.case_data.get(TestCaseEnum.CURRENT_RE_SET_CACHE.value[0]),
                # 获取当前请求的缓存设置。
                "sql": self.get_sql,  # 获取执行的sql语句。
                "assert_data": self.get_assert,  # 获取断言数据。
                "setup_sql": self.case_data.get(TestCaseEnum.SETUP_SQL.value[0]),  # 获取测试用例执行前需要执行的sql语句。
                "teardown": self.case_data.get(TestCaseEnum.TEARDOWN.value[0]),  # 获取测试用例执行后需要执行的方法。
                "teardown_sql": self.case_data.get(TestCaseEnum.TEARDOWN_SQL.value[0]),  # 获取测试用例执行后需要执行的sql语句。
                "sleep": self.case_data.get(TestCaseEnum.SLEEP.value[0]),  # 获取测试用例执行前需要等待的时间。
            }
            # 如果case_id_switch为True，则将测试用例的id和数据存储为字典的形式
            if case_id_switch is True:
                case_list.append({key: TestCase(**case_date).dict()})
            # 否则直接存储测试用例的数据。
            else:
                case_list.append(TestCase(**case_date).dict())

    # 返回case_list
    return case_list


class GetTestCase:

    # 该标记表示该方法是一个静态方法，可以通过类名直接调用，不需要实例化类。
    @staticmethod
    # 定义了一个名为case_data的方法，该方法需要传入一个参数case_id_lists，该参数是一个列表类型，用于存储测试用例的id。
    def case_data(case_id_lists: List):
        # 初始化一个空列表，用于存储测试用例数据。
        case_lists = []
        # 循环遍历case_id_lists中的每一个元素，赋值给变量i。
        for i in case_id_lists:
            # 通过调用CacheHandler类的get_cache方法，获取指定测试用例的数据，并将其赋值给变量_data。
            _data = CacheHandler.get_cache(i)
            # 将获取到的测试用例数据存储到case_lists列表中。
            case_lists.append(_data)

        # 返回存储测试用例数据的列表case_lists。
        return case_lists
