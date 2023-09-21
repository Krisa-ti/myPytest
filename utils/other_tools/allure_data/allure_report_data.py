"""
描述: 收集 allure 报告
"""

import json
from typing import List, Text
from common.setting import ensure_path_sep
from utils.other_tools.read_files_tools.get_all_files_path import get_all_files
from utils.other_tools.models import TestMetrics


# 定义了一个名为 AllureFileClean 的类
class AllureFileClean:
    """allure 报告数据清洗，提取业务需要得数据"""

    # @classmethod 是 Python 中的一个装饰器，用来指示一个类方法。类方法与实例方法的不同之处在于，类方法第一个参数必须是类本身，Python 会自动传入该参数，通常命名为 cls，而不是 self，这也是 @classmethod 装饰器的作用之一。通过类名可以直接调用类方法，而不需要实例化对象。
    @classmethod
    # 使用了一个类装饰器 cls，其返回值是一个列表，该列表中的元素是一个测试用例数据。
    def get_testcases(cls) -> List:
        """ 获取所有 allure 报告中执行用例的情况"""
        # 创建一个空列表 files 用于存放读取到的测试用例数据。
        files = []
        # 使用 get_all_files 函数来获取所有测试用例文件的路径，并通过迭代器 for 循环遍历每个路径。ensure_path_sep 函数将文件路径格式化为当前操作系统的标准格式（加上 \ 或 / 等分隔符），以确保路径可用。
        for i in get_all_files(ensure_path_sep("\\report\\html\\data\\test-cases")):
            # 使用 Python 的 with 语句打开测试用例文件，并赋值给变量 file，指定使用 utf-8 编码方式打开文件。
            with open(i, 'r', encoding='utf-8') as file:
                # 从打开的文件中读取 JSON 数据，并使用 json.load 函数将其加载到 date 变量中。
                date = json.load(file)
                # 将从文件中获取的数据 date 添加到 files 列表中。
                files.append(date)
        # 当获取所有测试用例文件的数据后，返回 files 列表作为结果，结束 get_testcases 方法的执行。
        return files

    # 总的来说，这段代码的作用是遍历指定路径下的所有测试用例文件，将其中的 JSON 数据提取出来，并将所有数据放入列表 files 中，最后返回该列表。这个过程可以以简单而灵活的方式提取并汇总数据，方便后续的数据处理和分析。

    # 定义了一个名为 get_failed_case 的方法，返回一个 List 类型对象。
    def get_failed_case(self) -> List:
        """ 获取到所有失败的用例标题和用例代码路径"""
        # 创建一个名为 error_case 的空列表，用于存储所有失败和中断的测试用例的标题和代码路径。
        error_case = []
        # 使用 for 循环遍历所有测试用例数据（该方法调用了 get_testcases 函数来获取测试用例数据列表，这个函数我们前面已经讲过）。
        for i in self.get_testcases():
            # 对于每个测试用例数据，如果它的执行状态为 'failed' 或 'broken'，则将其标题和代码路径作为元组 (title, path) 添加到 error_case 列表中。
            if i['status'] == 'failed' or i['status'] == 'broken':
                error_case.append((i['name'], i['fullName']))
        # 当循环遍历完所有测试用例数据，返回 error_case 列表作为结果。
        return error_case

    # 定义了一个名为 get_failed_cases_detail 的方法，返回一个 Text 类型（即 str 类型）对象。
    def get_failed_cases_detail(self) -> Text:
        """ 返回所有失败的测试用例相关内容 """
        # 调用 get_failed_case 方法获取所有失败和中断的测试用例的标题和代码路径。
        date = self.get_failed_case()
        # 创建一个空字符串变量 values，用于拼接所有失败用例的详细信息。
        values = ""
        # 如果存在失败用例，则将 values 设置为 失败用例:\n，表示下面的字符串是所有失败用例的详细信息。
        if len(date) >= 1:
            values = "失败用例:\n"
            # 添加一行格式化的分隔符，用于区分每个测试用例的详细信息
            values += "        **********************************\n"
            # 遍历所有失败和中断的测试用例数据，对于每个测试用例数据，将其标题和代码路径拼接成字符串，并添加到 values 变量中。
            for i in date:
                values += "        " + i[0] + ":" + i[1] + "\n"
        # 当循环遍历完所有失败和中断的测试用例数据后，返回 values，即所有失败用例的详细信息字符串。
        return values

    @classmethod
    # get_case_count 的类方法，用于统计用例的数量和成功率。
    def get_case_count(cls) -> "TestMetrics":
        """ 统计用例数量 """
        # 用 try 语句块来处理可能抛出的异常情况。
        try:
            # 定义变量 file_name 来保存所有测试用例执行结果的统计数据路径，确保文件路径的结尾符为 / 。
            file_name = ensure_path_sep("/report/html/widgets/summary.json")
            # 使用 with 语句打开文件并读取 JSON 数据，确保文件以 utf-8 编码打开。
            with open(file_name, 'r', encoding='utf-8') as file:
                # 使用 json.load 加载文件数据为 Python 对象，并保存到变量 data 中。
                data = json.load(file)
            # 获取统计数据中的用例总数。
            _case_count = data['statistic']
            # # 获取统计数据中的测试执行时间。
            _time = data['time']
            # 创建集合 keep_keys 来存储要保留的统计数据键名。
            keep_keys = {"passed", "failed", "broken", "skipped", "total"}
            # 使用字典推导式，将 _case_count 子字典中存在于 keep_keys 集合中的键名和对应的值，在新的字典 run_case_data 中保存下来。
            run_case_data = {k: v for k, v in data['statistic'].items() if k in keep_keys}
            # 判断运行用例总数大于0则执行下面代码块
            if _case_count["total"] > 0:
                # 计算测试用例的通过率，并将其存储在run_case_data["pass_rate"]键中，保留两位小数。
                run_case_data["pass_rate"] = round(
                    (_case_count["passed"] + _case_count["skipped"]) / _case_count["total"] * 100, 2
                )
            else:
                # 如果没有运行的用例，则将通过率设置为0.0。
                run_case_data["pass_rate"] = 0.0
            # 如果测试用例总数为0，则将时间数据存储在run_case_data['time']键中，否则将运行时间除以1000，保留两位小数，并将其存储在run_case_data['time']键中。
            run_case_data['time'] = _time if run_case_data['total'] == 0 else round(_time['duration'] / 1000, 2)
            # 使用run_case_data创建一个TestMetrics对象，并将其作为函数的返回值。
            return TestMetrics(**run_case_data)
        # 如果读取文件时出现FileNotFoundError异常，则捕获该异常并将其存储在exc中。
        except FileNotFoundError as exc:
            # 从exc中重新抛出一个FileNotFoundError异常，并将新异常的说明文本存储在异常对象实例中。
            raise FileNotFoundError(
                "程序中检查到您未生成allure报告，"
                "通常可能导致的原因是allure环境未配置正确"
            ) from exc

