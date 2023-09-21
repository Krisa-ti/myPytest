from common.setting import ensure_path_sep
from utils.read_files_tools.get_yaml_data_analysis import CaseData
from utils.read_files_tools.get_all_files_path import get_all_files
from utils.cache_process.cache_control import CacheHandler, _cache_config


# 定义一个名为`write_case_process`的函数。
def write_case_process():
    """
    获取所有用例，写入用例池中
    :return:
    """

    # 循环获取所有存放用例的文件路径，并将解析yaml格式的数据存到`case_process`中。
    for i in get_all_files(file_path=ensure_path_sep("\\data"), yaml_data_switch=True):
        # 利用`CaseData`类读取`i`文件的yaml格式数据，并调用`case_process`方法，将测试用例数据处理后返回到`case_process`数组中。
        case_process = CaseData(i).case_process(case_id_switch=True)
        # 判断`case_process`的值是否为`None`。
        if case_process is not None:
            # 如果`case_process`的值不为`None`，则遍历其中的每个测试用例数据。
            for case in case_process:
                # 遍历当前测试用例下的每个键值对，其中`k`为测试用例ID，`v`为测试用例数据。
                for k, v in case.items():
                    # 判断当前测试用例ID是否已经存在于缓存池中。
                    case_id_exit = k in _cache_config.keys()
                    # 如果当前测试用例ID不存在于缓存池中，则通过`CacheHandler`类中的`update_cache`方法，将当前测试用例数据写入缓存池中。
                    if case_id_exit is False:
                        # 是一个成员方法，用于向一个名为cache_name的缓存对象中写入一个键值对。其中，k代表键名，v代表该键对应的值。
                        CacheHandler.update_cache(cache_name=k, value=v)
                    # 如果当前测试用例ID已经存在于缓存池中，则抛出一个异常。
                    elif case_id_exit is True:
                        # 抛出`ValueError`异常，并提示当前测试用例ID存在重复项，需要进行修改，同时展示文件路径。
                        raise ValueError(f"case_id: {k} 存在重复项, 请修改case_id\n"
                                         f"文件路径: {i}")


# 调用`write_case_process`函数开始执行代码
write_case_process()
'''
以上代码是一个用于读取测试用例文件，并将测试用例数据写入缓存池的函数。
总的来说，以上代码的功能就是将所有配置好的测试用例数据，读取后写入到缓存池中，以便后面的测试用例运行时能够实时获取并使用数据。
'''
