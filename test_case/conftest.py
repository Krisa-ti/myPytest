import pytest
import time
import allure
import requests
import ast
import json
from common.setting import ensure_path_sep
from utils.other_tools.requests_tool.request_control import cache_regular
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from utils.other_tools.models import TestCase
from utils.other_tools.read_files_tools.clean_files import del_file
from utils.other_tools.allure_data.allure_tools import allure_step, allure_step_no
from utils.cache_process.cache_control import CacheHandler
from utils import config


# @pytest.fixture是Pytest测试框架中使用的装饰器，用于标识一个函数为Pytest用例的fixture函数。通过fixture函数，我们可以在测试用例执行前或执行后，为测试用例提供一些前置条件或后置操作，比如初始化数据库连接、生成测试数据、删除临时文件等等。函数参数中的socpe参数和autouse参数是fixture函数的两个重要参数，分别用于指定fixture函数的作用域和自动调用情况。scope参数用于指定fixture函数的作用范围。常用的值包括：function（默认值）表示仅在当前测试用例中使用，每个测试用例都会重新创建；module表示在当前测试模块中使用，多个测试用例共用，每个测试模块执行前创建；session表示在整个测试session中使用，多个测试模块共用，整个测试会话只创建一次。autouse参数用于指定fixture函数是否自动调用。当autouse=True时，fixture函数会自动被执行；当autouse=False时，需要通过测试用例的参数显式调用才会执行。默认值为False。
@pytest.fixture(scope="session", autouse=False)
# 定义了一个名为clear_report的函数，主要功能是删除测试报告文件。
def clear_report():
    """如clean命名无法删除报告，这里手动删除"""
    # 这行代码调用了一个 del_file() 函数，用于删除给定文件或文件夹。在本例中，该函数会删除当前工作目录下的 report 文件夹。这里的 ensure_path_sep() 函数用于确保路径分隔符是正确的。在 Windows 系统中，路径分隔符通常是反斜杠 \，而在 Unix/Linux 系统中，路径分隔符通常是正斜杠 /。为了保证代码的可移植性，我们通常需要使用 os.path.join() 或 os.path.sep 来获取系统默认的路径分隔符。在本例中，ensure_path_sep() 函数会将输入的路径字符串中的分隔符替换为系统默认的分隔符。
    del_file(ensure_path_sep("\\report"))


# 总的来说，这个函数的作用就是清理测试报告，避免测试结果的污染和影响。


@pytest.fixture(scope="session", autouse=True)
# 定义了一个函数 init_info_accessToken，用于获取访问令牌。
def init_info_accessToken():
    """
    获取AccessToken
    :return:
    """
    # 定义了一个请求的 URL，该 URL 是由 config.host 配置文件中的地址和请求路径 /init/info 拼接而成的。
    url = str(config.host) + "/init/info"
    payload = {}
    headers = {
        'Country': 'USD',
        'Lang': 'en',
        'Currency': 'US',
    }
    # 这里使用 requests 库发送了一个 GET 请求，并将响应结果转换为 JSON 格式。在本例中，该请求会向指定的 URL 发送一个 GET 请求，获取访问令牌。
    response = requests.request("GET", url, headers=headers, data=payload).json()
    # 这行代码从响应结果中获取到访问令牌，并赋值给一个变量 AccessToken。
    AccessToken = response['data']['accessToken']
    # 这行代码将获取到的访问令牌更新到一个缓存中。在本例中，使用的缓存是 CacheHandler 类中的 update_cache() 方法。
    CacheHandler.update_cache(cache_name='Access_Token', value=AccessToken)


# 总的来说，这个函数的主要功能就是请求指定 URL，获取访问令牌，并将访问令牌保存到缓存中，以供后续使用。


# 这是一个 Pytest 的 hook 函数，用于修改测试用例集合。
def pytest_collection_modifyitems(items):
    for item in items:
        # 将测试用例名称从 Unicode 编码转换为原始字符。
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        # 将测试用例的 nodeid 从 Unicode 编码转换为原始字符，nodeid 是在测试用例运行时将其与测试用例的名称和参数等信息进行组合而得到的唯一标识符。
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
    # 这两行代码使用 Python 中的字符串编码和解码函数 encode() 和 decode()，将 item 对象中的名称和节点 ID 转换为中文，以便于控制台的显示。

    # 这里指定要运行的测试用例的名称。
    appoint_items = ["test_Register", "test_LOGIN"]
    # 定义一个空列表来接收筛选出来的测试用例。
    run_items = []
    # 对于要运行的每个测试用例名称，遍历所有测试用例。
    for i in appoint_items:
        for item in items:
            # 获取测试用例名称中的模块名称部分，这个部分是测试用例名称中的第一个 "[]" 内的内容，用于唯一标识所属模块。
            module_item = item.name.split("[")[0]
            # 如果当前测试用例的模块名称与要运行的测试用例名称一致，则将其添加到 run_items 列表中。
            if i == module_item:
                run_items.append(item)

    # 遍历要运行的测试用例列表，以及所有测试用例的列表，获取当前测试用例在两个列表中的索引值。
    for i in run_items:
        run_index = run_items.index(i)
        items_index = items.index(i)

        # 如果当前测试用例不在要运行的测试用例列表的最前面，就将它调整到最前面位置。首先从 items 中找到当前测试用例应该在的位置（即：run_index），然后使用 python 的交换变量值的语法将当前测试用例的位置与 run_index 位置的测试用例交换，从而达到把当前测试用例放到最前面的目的。
        if run_index != items_index:
            n_data = items[run_index]
            run_index = items.index(n_data)
            items[items_index], items[run_index] = items[run_index], items[items_index]


# 总之，这段代码主要是解决pytest测试用例的名称显示和测试用例的执行顺序问题，从而为自动化测试提供更好的支持。


# 定义了一个Pytest的测试用例配置函数，用于对测试用例进行标记和配置相关信息。
def pytest_configure(config):
    '''
    这段代码中使用了 config.addinivalue_line() 方法，来向 pytest 的配置文件添加标记。它的第一个参数是一个字符串 "markers"，表示添加标记。第二个参数是添加的标记名称，这里我们添加了两个标记，分别为 "smoke" 和 "回归测试"。

   添加标记后，在写测试用例时，就可以使用 @ pytest.mark. < marker_name > 的方式对测试用例进行标记。例如，可以使用 @ pytest.mark.smoke
   标记专注于快速测试且需要经常运行的测试用例，以便在快速运行中先执行。然后，我们可以运行
   pytest - m
   smoke
   命令，只运行带有 @ pytest.mark.smoke
   标记的测试用例。
   同样，我们可以使用 @ pytest.mark.回归测试
   标记需要从以前版本迁移或重构的测试用例。然后，我们可以运行
   pytest - m
   回归测试
   命令，只运行带有 @ pytest.mark.回归测试
   标记的测试用例。这使得我们可以轻松地在测试套件中分出不同的测试类别，从而更好地管理测试用例。
   config.addinivalue_line("markers", 'smoke')
   config.addinivalue_line("markers", '回归测试')
   '''

@pytest.fixture(scope="function", autouse=True)
# 自定义函数case_skip，它接受一个参数 in_data，表示输入的测试用例对象。
def case_skip(in_data):
    # 这里的意思是将输入参数 in_data 转换为一个 TestCase 类对象，并将其赋值给 in_data 变量。该类对象用于存储测试用例的相关信息，例如 URL、请求方式、请求头、请求数据、依赖数据和预期数据等信息。
    in_data = TestCase(**in_data)
    # 这行代码用于判断测试用例是否需要跳过。in_data.is_run 表示测试用例是否被标记为执行，这个标记通常是用于控制测试用例的执行。如果该标记为 False，则说明该测试用例被标记为跳过，因此函数会调用 pytest 的 skip() 方法来跳过该测试用例的执行。
    if ast.literal_eval(cache_regular(str(in_data.is_run))) is False:
        # 这行代码用于添加更详细的测试用例名称。allure.dynamic.title() 方法可以用于添加 Allure 报告的测试用例名称，并支持一些动态的参数，例如本例中的 in_data.detail，该参数代表测试用例的详细描述信息。这样，可以在 Allure 报告中看到更详细的测试用例的名称。
        allure.dynamic.title(in_data.detail)
        # 这几行代码使用 Allure Test Report 库的 allure_step() 和 allure_step_no() 方法，用于添加更详细的测试用例的报告信息。例如，该函数调用了多次 allure_step_no() 方法，用于展示测试用例中的操作步骤，并且将测试用例的请求 URL 和请求方式作为展示的参数。此外，该函数还将测试用例的请求头、请求数据、依赖数据和预期数据等信息，通过调用 allure_step() 方法添加到了 Allure 报告中。
        allure_step_no(f"请求URL: {in_data.is_run}")
        allure_step_no(f"请求方式: {in_data.method}")
        allure_step("请求头: ", in_data.headers)
        allure_step("请求数据: ", in_data.data)
        allure_step("依赖数据: ", in_data.dependence_case_data)
        allure_step("预期数据: ", in_data.assert_data)
        # 这行代码用于调用 pytest 的 skip() 方法，来跳过该测试用例的执行。如果测试用例被标记为跳过，则会直接执行该行代码，并跳过该测试用例的执行。
        pytest.skip()


# 总的来说，这个函数的作用是用于处理 pytest 测试套件中的跳过用例，并添加更详细的测试用例名称和报告信息。其中，函数调用了 Allure Test Report 库的方法，使得测试用例结果更加详尽、易读和易于维护。


# 定义了一个Pytest的测试用例收尾函数，用于生成测试报告并收集测试结果。
def pytest_terminal_summary(terminalreporter):
    # 这几行代码用于统计测试结果的各项指标。其中，terminalreporter.stats 属性是一个字典对象，存储了测试用例的各项状态，例如 'passed'、'failed'、'error'、'skipped' 等，这些属性的值是一个列表，其中每个元素都表示一个测试用例对象。这里的代码使用列表解析式和 len() 函数来计算各个状态的测试用例数。另外，_TOTAL 变量表示测试套件中全部测试用例的数量，_TIMES 记录了测试用例的执行时长。
    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    # 这里的代码使用日志记录了测试结果的统计信息。其中，INFO.logger.error() 方法用于记录用例总数和异常用例数，ERROR.logger.error() 方法用于记录失败用例数，WARNING.logger.warning() 方法用于记录跳过用例数，INFO.logger.info() 方法用于记录用例执行时长。
    INFO.logger.error(f"用例总数: {_TOTAL}")
    INFO.logger.error(f"异常用例数: {_ERROR}")
    ERROR.logger.error(f"失败用例数: {_FAILED}")
    WARNING.logger.warning(f"跳过用例数: {_SKIPPED}")
    INFO.logger.info("用例执行时长: %.2f" % _TIMES + " s")

    # 这里的代码是为了计算测试用例的成功率，并且将其记录到日志中。如果测试用例总数为 0，会触发 ZeroDivisionError 异常，此时依然需要将成功率记录为 0。
    try:
        _RATE = _PASSED / _TOTAL * 100
        INFO.logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        INFO.logger.info("用例成功率: 0.00 %")

# 总的来说，这段代码的作用是在 pytest 测试运行结束后，统计各个状态的测试用例数和用例成功率，然后将这些信息记录到日志中，方便开发人员查看和分析测试结果。