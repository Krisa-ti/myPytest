"""
断言类型封装，支持json响应断言、数据库断言
"""
import ast
import json
from typing import Text, Any
from jsonpath import jsonpath
from utils.other_tools.models import AssertMethod
from utils.logging_tool.log_control import WARNING
from utils.read_files_tools.regular_control import cache_regular
from utils.other_tools.models import load_module_functions
from utils.assertion import assert_type
from utils.other_tools.exceptions import AssertTypeError
from utils import config


# 一个名为 AssertUtil 的类，用于封装测试用例中的断言操作。
class AssertUtil:

    # 这是 AssertUtil 类的构造方法，用于初始化该类的各种属性。
    def __init__(self, assert_data, sql_data, request_data, response_data, status_code):
        """
            :param  response_data：请求的响应数据。
            :param  request_data：请求的请求数据。
            :param  sql_data：SQL 语句执行的结果。
            :param  assert_data：测试用例中的断言部分数据。
            :param  sql_switch：MySQL 数据库的开关，默认从配置文件中获取。
            :param  status_code：请求的响应状态码。
        """

        # 将传入的参数分别作为对象属性进行了初始化，并从配置文件中获取了 MySQL 数据库的开关状态。
        self.response_data = response_data
        self.request_data = request_data
        self.sql_data = sql_data
        self.assert_data = assert_data
        self.sql_switch = config.mysql_db.switch
        self.status_code = status_code

    # @staticmethod 是 Python 中的一个装饰器，用于将一个方法定义为静态方法。在 Python 中，静态方法是属于类的，而不是属于实例的。因此在静态方法中，不能使用 self 关键字来访问实例属性和方法，而是要使用类属性和方法。
    @staticmethod
    # 定义了一个名为literal_eval()的静态方法。这个方法接收一个参数attr，对该参数执行了cache_regular(str(attr))方法后，再使用Python内置的ast模块的literal_eval()方法对其进行转换，并返回转换后的结果。
    def literal_eval(attr):
        # ast.literal_eval()方法帮助我们将一个字符串表达式解析为Python数据类型，比如将字符串'["a", 1, {"key": "value"}]'解析为List类型["a", 1, {"key": "value"}]。在cache_regular()方法中，它的主要功能是在字符串中寻找形如$cache{xxx}的字符串，并从缓存中获取与xxx相关的数据，再进行替换。这样在literal_eval()方法中，我们传递给它的是一个字符串，我们需要对这个字符串中嵌入的缓存变量进行处理后再进行转换。
        return ast.literal_eval(cache_regular(str(attr)))

    # 总之，这段代码提供了一种从缓存中获取数据并将其与外部程序进行交互的机制，并对字符串表达式进行操作和转换。这对于处理数据表达式和进行数据序列化非常有用。

    # @property是一个Python内置的装饰器，用于将一个方法转换为属性。当我们将@property应用于一个类的方法时，它会将该方法转换为只读属性，这意味着我们可以像访问属性一样使用该方法，而不是函数。
    @property
    # 定义了一个名为get_assert_data()的属性方法，该方法返回实例的assert_data属性，并调用cache_regular()方法将assert_data属性中包含的缓存字符串转换成实际数据类型后返回。
    def get_assert_data(self):
        # 该代码段使用Python中的assert语句检查self.assert_data是否为None。如果self.assert_data为None，则会触发一条异常，该异常描述了所在类及其缺失的属性。代码中使用%运算符连接字符串，%s表示需要被替换的格式化字符串。由于self.__class__.__name__表示当前实例所属的类名，因此，当检查失败时，错误消息将会包含所属类的名称。
        assert self.assert_data is not None, (
                "'%s' should either include a `assert_data` attribute, "
                % self.__class__.__name__
        )
        # 该代码行通过调用ast.literal_eval()方法将cache_regular()方法解析后的字符串转换为Python字典或列表对象，并将其作为属性方法的返回值返回。
        return ast.literal_eval(cache_regular(str(self.assert_data)))

    @property
    # 定义了一个名为get_type()的属性方法，该方法返回实例的assert_data字典中的type属性对应的枚举值
    def get_type(self):
        # 该代码段使用Python中的assert语句检查assert_data字典中是否包含type属性。如果不包含，则会触发一条异常，该异常描述了所缺少的属性，并包含assert_data字典作为错误消息。
        assert 'type' in self.get_assert_data.keys(), (
                " 断言数据: '%s' 中缺少 `type` 属性 " % self.get_assert_data
        )
        # 该代码行使用self.get_assert_data.get("type")来获取assert_data字典中的type属性对应的值，并传递给AssertMethod枚举类来获取枚举值。返回值name为枚举值的名称。
        name = AssertMethod(self.get_assert_data.get("type")).name
        # 返回枚举值的名称
        return name

    @property
    # 定义了一个名为get_value()的属性方法，该方法返回实例的assert_data字典中的value属性对应的值。
    def get_value(self):
        # 该代码段使用Python中的assert语句检查assert_data字典中是否包含value属性。如果不包含，则会触发一条异常，该异常描述了所缺少的属性，并包含assert_data字典作为错误消息。
        assert 'value' in self.get_assert_data.keys(), (
                " 断言数据: '%s' 中缺少 `value` 属性 " % self.get_assert_data
        )
        # 该代码行使用self.get_assert_data.get("value")来获取assert_data字典中的value属性对应的值，并将其作为该属性方法的返回值返回。
        return self.get_assert_data.get("value")

    @property
    # 定义了一个名为get_jsonpath()的属性方法，该方法返回实例的assert_data字典中的jsonpath属性对应的值。
    def get_jsonpath(self):
        # 该代码段使用Python中的assert语句检查assert_data字典中是否包含jsonpath属性。如果不包含，则会触发一条异常，该异常描述了所缺少的属性，并包含assert_data字典作为错误消息。
        assert 'jsonpath' in self.get_assert_data.keys(), (
                " 断言数据: '%s' 中缺少 `jsonpath` 属性 " % self.get_assert_data
        )
        # 该代码行使用self.get_assert_data.get("jsonpath")来获取assert_data字典中的jsonpath属性对应的值，并将其作为该属性方法的返回值返回。
        return self.get_assert_data.get("jsonpath")

    @property
    # 定义了一个名为get_assert_type()的属性方法，该方法返回实例的assert_data字典中的AssertType属性对应的值。
    def get_assert_type(self):
        # 该代码段使用Python中的assert语句检查assert_data字典中是否包含AssertType属性。如果不包含，则会触发一条异常，该异常描述了所缺少的属性，并包含assert_data字典作为错误消息。
        assert 'AssertType' in self.get_assert_data.keys(), (
                " 断言数据: '%s' 中缺少 `AssertType` 属性 " % self.get_assert_data
        )
        # 该代码行使用self.get_assert_data.get("AssertType")来获取assert_data字典中的AssertType属性对应的值，并将其作为该属性方法的返回值返回。
        return self.get_assert_data.get("AssertType")

    @property
    # 定义了一个名为get_message()的属性方法，该方法返回实例的assert_data字典中的message属性对应的值。如果message属性不存在，则返回None。
    def get_message(self):
        """
        获取断言描述，如果未填写，则返回 `None`
        :return:
        """
        # 该代码行使用self.get_assert_data.get("message", None)来获取assert_data字典中的message属性对应的值。如果message属性不存在，get()方法会返回None，作为该属性方法的返回值返回。
        return self.get_assert_data.get("message", None)

    @property
    # 定义了一个名为get_sql_data()的属性方法。该方法的作用是从实例的sql_data中提取数据，如果需要，将字节类型转换为字符串类型，并返回提取的数据。方法中还包含一些判断和异常的处理。
    def get_sql_data(self):

        # 如果sql_switch_handle为True，且sql_data为空，则会触发一条异常，该异常说明在需要数据库断言的情况下，未填写要查询的SQL语句。判断数据库开关为开启，并需要数据库断言的情况下，未编写sql，则抛异常。
        if self.sql_switch_handle:
            assert self.sql_data != {'sql': None}, (
                "请在用例中添加您要查询的SQL语句。"
            )

        # 如果sql_data是字节类型，则使用decode()方法将其转换为字符串类型并返回。处理 mysql查询出来的数据类型如果是bytes类型，转换成str类型
        if isinstance(self.sql_data, bytes):
            return self.sql_data.decode('utf=8')

        # 该代码行使用jsonpath库从sql_data中提取数据，并将结果赋值给sql_data变量。如果提取失败，则会触发一条异常，该异常说明在当前语法下无法提取数据。
        sql_data = jsonpath(self.sql_data, self.get_value)
        assert sql_data is not False, (
            f"数据库断言数据提取失败，提取对象: {self.sql_data} , 当前语法: {self.get_value}"
        )

        # 如果sql_data包含多个值，则返回所有值；否则，只返回第一个值。
        if len(sql_data) > 1:
            return sql_data
        return sql_data[0]

    @staticmethod
    # 定义了一个名为functions_mapping()的静态方法。该方法调用了load_module_functions()函数并将其结果返回。具体来说，该方法返回了一个名为assert_type模块中所有函数的字典，该字典的键为函数名，值为函数的内存地址。
    def functions_mapping():
        # 该代码行调用load_module_functions()函数，并将返回的字典作为该方法的返回值。该字典中包含了assert_type模块中所有函数的名称和内存地址。
        return load_module_functions(assert_type)

    @property
    # 定义了get_response_data方法，它有一个self参数。self表示实例本身，在这里，它的作用是让方法可以访问对象的其他属性和方法。
    def get_response_data(self):
        # 我们使用json.loads这个函数将response_data这个字符串转换为Python对象。
        return json.loads(self.response_data)

    @property
    # 定义了sql_switch_handle方法。该方法的作用是用于处理数据库开关的状态，并判断是否要打印断言数据。
    def sql_switch_handle(self):

        """
        判断数据库开关，如果未开启，则打印断言部分的数据
        :return:
        """
        # 这里使用了一个条件语句，如果self.sql_switch属性的值为False，则说明数据库开关未开启。此时会打印一条警告日志（利用日志框架WARNING.logger.warning）并给出相应的提示信息，提示信息中包括了%s占位符，它会在日志中动态地显示当前测试案例的断言数据值。该断言数据的值由self.get_assert_data属性返回。
        if self.sql_switch is False:
            WARNING.logger.warning(
                "检测到数据库状态为关闭状态，程序已为您跳过此断言，断言值:%s" % self.get_assert_data
            )
        # 最后返回self.sql_switch属性的值。如果它的值是True，则意味着数据库开关处于开启状态。对于这种情况，sql_switch_handle方法没有其他作用，只是作为属性在代码中被访问。如果它的值是False，则说明数据库开关被关闭，那么我们就要根据该情况，进行相应的处理（即打印警告消息）。
        return self.sql_switch

    # 定义了一个名为_assert的方法，它有三个参数：check_value，expect_value和message。这个方法的作用是进行断言操作。check_value参数是我们要检查的值，expect_value参数是我们期待的值，而message参数则是一个可选的字符串，用来存放错误信息。
    def _assert(self, check_value: Any, expect_value: Any, message: Text = ""):

        # 先通过self.functions_mapping()方法得到一个字典，这个字典存储了不同类型的断言函数。self.functions_mapping()的定义可以在之前提到过的assert_type.py模块中找到。然后使用self.get_type属性来确定要使用哪个断言函数。get_type属性是在调用Parser对象的parse方法后赋值的。最后传递check_value、expect_value和message这三个参数，调用相应的断言函数进行断言检查。如果检查失败，我们就会使用message参数中的错误信息进行提示。
        self.functions_mapping()[self.get_type](check_value, expect_value, str(message))

    @property
    # 定义了一个名为_assert_resp_data的属性装饰器，表示这是一个只读属性。这个属性的作用是从响应数据中提取出指定路径（jsonpath），返回提取的结果。
    def _assert_resp_data(self):
        # 首先，我们使用jsonpath模块的jsonpath函数，传入响应数据和jsonpath路径，提取出对应路径的数据。
        resp_data = jsonpath(self.get_response_data, self.get_jsonpath)

        # 进行断言检查，确保提取的数据不为False。如果断言失败，会抛出一个错误，提示提取失败。
        assert resp_data is not False, (
            f"jsonpath数据提取失败，提取对象: {self.get_response_data} , 当前语法: {self.get_jsonpath}"
        )

        # 如果提取到的数据有多个值，我们返回一个列表，否则直接返回这个值。
        if len(resp_data) > 1:
            return resp_data
        return resp_data[0]

    @property
    def _assert_request_data(self):
        # 在这里，self.request_data是发送HTTP请求时的参数（payload）。jsonpath接受两个参数，第一个参数是待检索的元素，第二个参数是用来检索数据的语法。jsonpath函数返回满足语法的所有值列表。在这里，req_data是一个列表或空列表。
        req_data = jsonpath(self.request_data, self.get_jsonpath)

        # 这段代码确保了我们从请求参数中成功提取到了指定字段的值。如果提取失败，则抛出异常，其中包含错误信息。
        assert req_data is not False, (
            f"jsonpath数据提取失败，提取对象: {self.request_data} , 当前语法: {self.get_jsonpath}"
        )

        # 这里根据请求参数提取结果的情况，返回对应的值或值列表。如果提取的是单值，则直接返回该值。如果提取的是多个值，则返回所有值的列表。
        if len(req_data) > 1:
            return req_data
        return req_data[0]

    # 定义一个实例方法 assert_type_handle，该方法用来根据不同的断言类型调用对应的断言方法。
    def assert_type_handle(self):
        # 如果断言类型是 R_SQL，则调用 _assert_request_data 方法获取请求参数中的字段值，调用 get_sql_data 获取期望的值，然后通过 _assert 方法进行断言校验。
        if self.get_assert_type == "R_SQL":
            self._assert(self._assert_request_data, self.get_sql_data, self.get_message)
        # 如果断言类型是 SQL 或 D_SQL，则调用 _assert_resp_data 方法获取响应参数中的字段值，调用 get_sql_data 获取期望的值，然后通过 _assert 方法进行断言校验。
        elif self.get_assert_type == "SQL" or self.get_assert_type == "D_SQL":
            self._assert(self._assert_resp_data, self.get_sql_data, self.get_message)
        # 如果断言类型为 None，则调用 _assert_resp_data 方法获取响应参数中的字段值，调用 get_value 获取期望的值，然后通过 _assert 方法进行值比较的断言校验。
        elif self.get_assert_type is None:
            self._assert(self._assert_resp_data, self.get_value, self.get_message)
        # 如果断言类型不符合以上三种情况，则抛出一个自定义的异常 AssertTypeError，提醒用户该断言类型不被支持。
        else:
            raise AssertTypeError("断言失败，目前只支持数据库断言和响应断言")


# 定义了一个名为 Assert 的类，该类继承了 AssertUtil 类，即该类继承了 AssertUtil 类中的所有属性和方法。
class Assert(AssertUtil):

    # 定义名为 assert_data_list 的方法。
    def assert_data_list(self):
        # 初始化一个空列表 assert_list，用于存储每一项测试数据的断言结果。
        assert_list = []
        # 遍历 assert_data 字典中的键值对，assert_data 是 AssertUtil 类中的一个数据成员，存储了当前测试用例所需要验证的数据。
        for k, v in self.assert_data.items():
            # 根据键 k 是不是 "status_code" 来判断当前项是不是用于验证响应状态码。
            if k == "status_code":
                # 如果当前项用于验证响应状态码，那么使用断言方法 assert 判断 self.status_code 是否等于 v，如果不等于，则抛出异常信息 "响应状态码断言失败"。
                assert self.status_code == v, "响应状态码断言失败"
            # 如果当前项不是用于验证响应状态码，那么将其对应的值 v 添加到 assert_list 中。
            else:
                assert_list.append(v)
        # 遍历结束后返回 assert_list 列表，其中包含了每一项测试数据所对应的断言结果。
        return assert_list

    # 定义了名为 assert_type_handle 的方法。
    def assert_type_handle(self):
        # 使用 for 循环遍历 self.assert_data_list() 方法返回的每一项测试数据的断言结果，并将其赋值给变量 i。
        for i in self.assert_data_list():
            # 将变量 i 赋值给 self.assert_data 成员变量，这样的话，在后面的方法中就能使用 self.assert_data 来引用当前遍历到的测试数据了。
            self.assert_data = i
            #使用
            super()
            #调用继承自
            AssertUtil
            '''
            类的
            assert_type_handle
            方法，该方法的作用是根据当前测试数据的类型，进行对应的验证。这里使用
            '''

            super()
            '''
            目的是将具体的实现交给父类去处理，而当前方法只负责调用，以达到代码的重用性。
            '''

            super().assert_type_handle()

# 这个类提供了一种便利的方式来进行多个断言的校验，只需要传入一个断言数据字典，该类就会按照断言类型和断言数值进行校验，并抛出校验失败的异常信息。
