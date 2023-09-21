import json
import shutil
import ast
import xlwings
from common.setting import ensure_path_sep
from utils.read_files_tools.get_all_files_path import get_all_files
from utils.notify.wechat_send import WeChatSend
from utils.other_tools.allure_data.allure_report_data import AllureFileClean


# TODO 还需要处理动态值
# 定义一个名为ErrorTestCase的类。
class ErrorTestCase:
    """ 收集错误的excel """

    # 定义一个名为__init__的方法，用于初始化对象，并接受一个默认参数self。
    def __init__(self):
        # 设置test_case_path属性，将其初始化为\report\html\data\test-cases\字符串。ensure_path_sep函数可能会在字符串结尾添加路径分隔符("/")或者""，以保证路径的完整性。
        self.test_case_path = ensure_path_sep("\\report\\html\\data\\test-cases\\")

    # 定义一个名为get_error_case_data的方法，用于获取失败用例的数据，其中self参数是该类的实例本身。
    def get_error_case_data(self):
        """
        收集所有失败用例的数据
        @return:
        """
        # 调用名为get_all_files的函数，传入test_case_path属性作为参数，获取该路径下的所有文件路径并返回path。
        path = get_all_files(self.test_case_path)
        # 创建一个空的列表files，用于存储所有执行失败的用例数据。
        files = []
        # 遍历path列表。
        for i in path:
            # 用"r"模式打开文件路径i，命名为file。encoding='utf-8'指定打开文件的字符编码，这里使用utf-8格式打开文件。
            with open(i, 'r', encoding='utf-8') as file:
                # 用json.load()方法从文件file中读取内容，并将读取的内容存储在date变量中。
                date = json.load(file)
                # 使用if语句判断读取的内容中的状态是否为failed或者broken，如果是则进入if语句块。
                if date['status'] == 'failed' or date['status'] == 'broken':
                    # 将符合条件的date添加到files列表中。
                    files.append(date)
        # 打印files列表中收集到的所有执行失败的用例数据。
        print(files)
        # 返回files列表。
        return files

    @classmethod
    # 定义一个名为get_case_name的方法，并且该方法接受两个参数，一个是cls表示该方法属于该类，第二个参数是test_case，表示要处理的测试用例。
    def get_case_name(cls, test_case):
        """
        收集测试用例名称
        @return:
        """
        # 获取测试用例字典中的name属性，通过字符串的split()方法，按照'['进行分割，并且将分割后的结果存储在name列表中。
        name = test_case['name'].split('[')
        # 获取列表中的第二个元素，并使用切片操作去掉该元素的最后一个字符']'，将获取到的值存储在case_name变量中。
        case_name = name[1][:-1]
        # 返回得到的测试用例名称。
        return case_name

    @classmethod
    # 定义了一个名为get_parameters的方法，用于获取allure报告中parameters参数中的内容，即请求前的数据。如果测试用例未发送请求导致异常情况，则该函数用于依然能够处理该用例。
    def get_parameters(cls, test_case):
        """
        获取allure报告中的 parameters 参数内容, 请求前的数据
        用于兼容用例执行异常，未发送请求导致的情况
        @return:
        """
        # 获取测试用例字典中的parameters参数的第一个字典中的value属性。
        parameters = test_case['parameters'][0]['value']
        # 通过ast.literal_eval()方法对parameters进行字面上的评估，将字符串转换为相应的Python数据类型并进行返回。这里的parameters是一个字符串形式的dict类型，使用该方法能够将其转化为Python的dict类型，以方便处理。
        return ast.literal_eval(parameters)

    @classmethod
    # 定义了一个名为get_test_stage的方法，用于获取allure报告中请求后的数据。
    def get_test_stage(cls, test_case):
        """
        获取allure报告中请求后的数据
        @return:
        """
        # 获取测试用例字典中的testStage字典中的steps属性，并将其存储在test_stage变量中。
        test_stage = test_case['testStage']['steps']
        # 将获取到的测试步骤数据进行返回。
        return test_stage

    # 定义了一个名为get_case_url的方法，用于获取测试用例的url
    def get_case_url(self, test_case):
        """
        获取测试用例的 url
        @param test_case:
        @return:
        """
        # 如果测试用例的状态为broken，即测试用例的步骤数据异常。
        if test_case['testStage']['status'] == 'broken':
            # 调用get_parameters方法获取测试用例请求前的数据，再从中取出url属性的值，然后将其存储到_url变量中。
            _url = self.get_parameters(test_case)['url']
        # 如果测试用例的状态不为broken。
        else:
            # 调用get_test_stage方法获取测试用例请求后的数据，然后从中取出倒数第七个步骤的name属性的值的子串，存储在_url变量中。
            _url = self.get_test_stage(test_case)[-7]['name'][7:]
        # 将获取到的url数据进行返回。
        return _url

    # 定义了一个名为get_method的方法，用于获取测试用例的请求方式。
    def get_method(self, test_case):
        """
        获取用例中的请求方式
        @param test_case:
        @return:
        """
        # 如果测试用例的状态为broken，即测试用例的步骤数据异常。
        if test_case['testStage']['status'] == 'broken':
            # 调用get_parameters方法获取测试用例请求前的数据，再从中取出method属性的值，然后将其存储到_method变量中。
            _method = self.get_parameters(test_case)['method']
        # 如果测试用例的状态不为broken。
        else:
            # 调用get_test_stage方法获取测试用例请求后的数据，然后从中取出倒数第六个步骤的name属性的值的子串，存储在_method变量中。
            _method = self.get_test_stage(test_case)[-6]['name'][6:]
        # 将获取到的请求方式进行返回。
        return _method

    # 定义了一个名为get_headers的方法，用于获取测试用例的请求头信息。
    def get_headers(self, test_case):
        """
        获取用例中的请求头
        @return:
        """
        # 如果测试用例的状态为broken，即测试用例的步骤数据异常。
        if test_case['testStage']['status'] == 'broken':
            # 调用get_parameters方法获取测试用例请求前的数据，再从中取出headers属性的值，然后将其存储到_headers变量中。
            _headers = self.get_parameters(test_case)['headers']
        # 如果测试用例的状态不为broken。
        else:
            # 从测试用例请求后的数据中取出倒数第五个步骤的attachments属性的第一个元素，从中取出source属性的值，即请求头附件的文件名。
            _headers_attachment = self.get_test_stage(test_case)[-5]['attachments'][0]['source']
            # 拼接请求头附件文件的完整路径，并将其存储到path变量中。
            path = ensure_path_sep("\\report\\html\\data\\attachments\\" + _headers_attachment)
            # 打开该文件，并将其存储到file变量中。
            with open(path, 'r', encoding='utf-8') as file:
                # 读取file变量中的JSON格式内容，并将其存储到_headers变量中。
                _headers = json.load(file)
        # 将获取到的请求头内容进行返回。
        return _headers

    # 定义了一个名为get_request_type的方法，用于获取测试用例的请求类型。
    def get_request_type(self, test_case):
        """
        获取用例的请求类型
        @param test_case:
        @return:
        """
        # 调用get_parameters方法获取测试用例请求前的数据，再从中取出requestType属性的值，并将其存储在request_type变量中。
        request_type = self.get_parameters(test_case)['requestType']
        # 将获取到的请求类型进行返回。
        return request_type

    # 定义了一个名为get_case_data的方法，用于获取测试用例的请求体内容。
    def get_case_data(self, test_case):
        """
        获取用例内容
        @return:
        """
        # 如果测试用例的状态为broken，即测试用例的步骤数据异常。
        if test_case['testStage']['status'] == 'broken':
            # 调用get_parameters方法获取测试用例请求前的数据，再从中取出data属性的值，然后将其存储到_case_data变量中。
            _case_data = self.get_parameters(test_case)['data']
        # 如果测试用例的状态不为broken。
        else:
            # 从测试用例请求后的数据中取出倒数第四个步骤的attachments属性的第一个元素，从中取出source属性的值，即请求体附件的文件名。
            _case_data_attachments = self.get_test_stage(test_case)[-4]['attachments'][0]['source']
            # 拼接请求体附件文件的完整路径，并将其存储到path变量中。
            path = ensure_path_sep("\\report\\html\\data\\attachments\\" + _case_data_attachments)
            # 打开该文件，并将其存储到file变量中。
            with open(path, 'r', encoding='utf-8') as file:
                # 读取file变量中的JSON格式内容，并将其存储到_case_data变量中。
                _case_data = json.load(file)
        # 将获取到的请求体内容进行返回。
        return _case_data

    # 定义了一个名为get_dependence_case的方法，用于获取测试用例的依赖用例信息。
    def get_dependence_case(self, test_case):
        """
        获取依赖用例
        @param test_case:
        @return:
        """
        # 调用get_parameters方法获取测试用例请求前的数据，再从中取出dependence_case_data属性的值，并将其存储在_dependence_case_data变量中。
        _dependence_case_data = self.get_parameters(test_case)['dependence_case_data']
        # 将获取到的依赖用例信息进行返回。
        return _dependence_case_data

    # 定义了一个名为get_sql的方法，用于获取测试用例的SQL语句。
    def get_sql(self, test_case):
        """
        获取 sql 数据
        @param test_case:
        @return:
        """
        # 调用get_parameters方法获取测试用例请求前的数据，再从中取出sql属性的值，并将其存储在sql变量中。
        sql = self.get_parameters(test_case)['sql']
        # 将获取到的SQL语句进行返回。
        return sql

    # 定义了一个名为get_assert的方法，用于获取测试用例的断言数据。
    def get_assert(self, test_case):
        """
        获取断言数据
        @param test_case:
        @return:
        """
        # 调用get_parameters方法获取测试用例请求前的数据，再从中取出assert_data属性的值，并将其存储在assert_data变量中。
        assert_data = self.get_parameters(test_case)['assert_data']
        # 将获取到的断言数据进行返回。
        return assert_data

    @classmethod
    # 定义一个名为get_response的方法，并且该方法接受两个参数，一个是cls，表示该方法是一个类方法，第二个参数是test_case，表示要处理的测试用例。
    def get_response(cls, test_case):
        """
        获取响应内容的数据
        @param test_case:
        @return:
        """
        # 如果测试用例的状态为broken，代表该测试用例没有响应数据，将其状态信息作为响应内容。
        if test_case['testStage']['status'] == 'broken':
            # 将测试用例状态信息作为响应内容，并将其存储在_res_date变量中。
            _res_date = test_case['testStage']['statusMessage']
        # 如果测试用例状态不是broken，则尝试获取响应数据。
        else:
            try:
                # 获取最后一步操作的附件中的响应数据路径。
                res_data_attachments = \
                    test_case['testStage']['steps'][-1]['attachments'][0]['source']
                # 拼接出响应数据的完整路径。
                path = ensure_path_sep("\\report\\html\\data\\attachments\\" + res_data_attachments)
                # 打开响应数据所在文件，读取其中的JSON数据，并将其赋值给_res_date变量。
                with open(path, 'r', encoding='utf-8') as file:
                    _res_date = json.load(file)
            # 如果找不到响应数据所在文件，则代表程序中没有提取到响应数据，将None赋值给_res_date变量。
            except FileNotFoundError:
                _res_date = None
        # 将获取到的响应数据进行返回。
        return _res_date

    @classmethod
    # 定义了一个名为get_case_time的类方法，用于获取测试用例的运行时长。
    def get_case_time(cls, test_case):
        """
        获取用例运行时长
        @param test_case:
        @return:
        """

        # 获取测试用例运行时长，并将其单位转换为毫秒，并将其存储在case_time变量中。
        case_time = str(test_case['time']['duration']) + "ms"
        # 将获取到的运行时长进行返回。
        return case_time

    @classmethod
    # 定义了一个名为get_uid的类方法，用于获取测试用例在Allure报告中的唯一标识符（uid）。
    def get_uid(cls, test_case):
        """
        获取 allure 报告中的 uid
        @param test_case:
        @return:
        """
        # 获取测试用例的唯一标识符（uid），并将其存储在uid变量中。
        uid = test_case['uid']
        # 将获取到的uid进行返回。
        return uid


# 定义了用于整理运行失败的测试用例成excel报告的方法
class ErrorCaseExcel:
    """ 收集运行失败的用例，整理成excel报告 """

    # 定义类的构造方法。
    def __init__(self):
        # 定义一个名为_excel_template的私有变量，表示excel模板文件的路径。
        _excel_template = ensure_path_sep("\\utils\\other_tools\\allure_data\\自动化异常测试用例.xlsx")
        # 定义一个名为self._file_path的变量，表示生成excel报告的文件路径。
        self._file_path = ensure_path_sep("\\Files\\" + "自动化异常测试用例.xlsx")
        # 将_excel_template模板文件复制到self._file_path路径下。
        shutil.copyfile(src=_excel_template, dst=self._file_path)
        # 创建一个Excel应用程序对象。
        self.app = xlwings.App(visible=False, add_book=False)
        # 打开excel报告文件，返回一个xlwings.Book对象。
        self.w_book = self.app.books.open(self._file_path, read_only=False)

        # 选取指定名称的工作表异常用例。
        self.sheet = self.w_book.sheets['异常用例']  # 或通过索引选取
        # 创建一个ErrorTestCase对象，用于收集运行失败的测试用例。
        self.case_data = ErrorTestCase()

    # 定义一个名为background_color的方法，参数是self，表示类的实例本身，position表示要设置背景颜色的单元格位置，rgb表示要设置的背景色的RGB值。
    def background_color(self, position: str, rgb: tuple):
        """
        excel 单元格设置背景色
        @param rgb: rgb 颜色 rgb=(0，255，0)
        @param position: 位置，如 A1, B1...
        @return:
        """
        # 获取工作表中指定位置的单元格范围对象。
        rng = self.sheet.range(position)
        # 设置单元格范围对象的颜色属性为RGB值rgb，并将值赋给变量excel_rgb。
        excel_rgb = rng.color = rgb
        # 将设置的颜色RGB值返回。
        return excel_rgb

    # 定义一个名为column_width的方法，参数是self，表示类的实例本身，position表示要设置列宽的列的位置（如"A"，"B"等），width表示要设置的列宽度。
    def column_width(self, position: str, width: int):
        """
        设置列宽
        @return:
        """
        # 获取工作表中指定列的范围对象。
        rng = self.sheet.range(position)
        # 将指定列的列宽设置为width，并将值赋给变量excel_column_width。
        excel_column_width = rng.column_width = width
        # 将设置的列宽度返回。
        return excel_column_width

    # 定义一个名为row_height的方法，参数是self，表示类的实例本身，position表示要设置行高的行的位置，height表示要设置的行高度。
    def row_height(self, position, height):
        """
        设置行高
        @param position:
        @param height:
        @return:
        """
        # 获取工作表中指定行的范围对象。
        rng = self.sheet.range(position)
        # 将指定行的行高设置为height，并将值赋给变量excel_row_height。
        excel_row_height = rng.row_height = height
        # 将设置的行高度返回。
        return excel_row_height

    # 定义一个名为column_width_adaptation的方法，参数是self，表示类的实例本身，position表示要进行宽度自适应的列的范围
    def column_width_adaptation(self, position):
        """
        excel 所有列宽度自适应
        @return:
        """
        # 获取工作表中指定范围的对象。
        rng = self.sheet.range(position)
        # 将该范围内所有列的宽度自适应调整。
        auto_fit = rng.columns.autofit()
        #返回自适应后的结果。
        return auto_fit

    # 定义一个名为row_width_adaptation的方法，参数是self，表示类的实例本身，position表示要进行宽度自适应的行的范围。
    def row_width_adaptation(self, position):
        """
        excel 设置所有行宽自适应
        @return:
        """
        # 获取工作表中指定范围的对象。
        rng = self.sheet.range(position)
        # 将该范围内所有行的宽度自适应调整。
        row_adaptation = rng.rows.autofit()
        # 返回自适应后的结果。
        return row_adaptation

    # 定义一个名为write_excel_content的方法。参数是self，表示类的实例本身，position表示要写入的位置，value表示要写入的内容，均为字符串类型。
    def write_excel_content(self, position: str, value: str):
        """
        excel 中写入内容
        @param value:
        @param position:
        @return:
        """
        # 将给定位置的单元格赋值为给定的值。由于sheet是当前实例的一个属性，因此可以使用self.sheet来获取该工作表对象。range(position)表示获取给定位置的单元格对象，然后对其value属性进行赋值操作。
        self.sheet.range(position).value = value

    # 定义一个名为write_case的方法，参数是self，表示类的实例本身。
    def write_case(self):
        """
        用例中写入失败用例数据
        @return:
        """

        # 从case_data对象获取失败用例数据。
        _data = self.case_data.get_error_case_data()
        # 如果存在失败用例，则继续执行。
        if len(_data) > 0:
            # 设置行号开始的编号，默认从第二行开始。
            num = 2
            # 遍历失败用例数据。
            for data in _data:
                # 在第num行的“A”列中写入用例的唯一标识。
                self.write_excel_content(position="A" + str(num), value=str(self.case_data.get_uid(data)))
                # 在第num行的“B”列中写入用例的名称。
                self.write_excel_content(position='B' + str(num), value=str(self.case_data.get_case_name(data)))
                # 在第num行的“C”列中写入用例的 URL。
                self.write_excel_content(position="C" + str(num), value=str(self.case_data.get_case_url(data)))
                # 在第num行的“D”列中写入用例的请求方法名。
                self.write_excel_content(position="D" + str(num), value=str(self.case_data.get_method(data)))
                # 在第num行的“E”列中写入用例的请求类型。
                self.write_excel_content(position="E" + str(num), value=str(self.case_data.get_request_type(data)))
                # 在第num行的“F”列中写入用例的头部信息。
                self.write_excel_content(position="F" + str(num), value=str(self.case_data.get_headers(data)))
                # 在第num行的“G”列中写入用例的请求数据。
                self.write_excel_content(position="G" + str(num), value=str(self.case_data.get_case_data(data)))
                # 在第num行的“H”列中写入用例依赖的其他用例。
                self.write_excel_content(position="H" + str(num), value=str(self.case_data.get_dependence_case(data)))
                # 在第num行的“I”列中写入用例的断言信息。
                self.write_excel_content(position="I" + str(num), value=str(self.case_data.get_assert(data)))
                # 在第num行的“J”列中写入用例的 SQL 语句。
                self.write_excel_content(position="J" + str(num), value=str(self.case_data.get_sql(data)))
                # 在第num行的“K”列中写入用例的执行时间。
                self.write_excel_content(position="K" + str(num), value=str(self.case_data.get_case_time(data)))
                # 在第num行的“L”列中写入用例的响应信息。
                self.write_excel_content(position="L" + str(num), value=str(self.case_data.get_response(data)))
                # 将行号加一，以便写入下一个用例。
                num += 1
            # 保存文件修改。
            self.w_book.save()
            # 关闭工作簿。
            self.w_book.close()
            # 结束 Excel 进程。
            self.app.quit()
            # 通知企业微信发送文件消息，包括更新的用例数量和文件路径。
            WeChatSend(AllureFileClean().get_case_count()).send_file_msg(self._file_path)


if __name__ == '__main__':
    ErrorCaseExcel().write_case()