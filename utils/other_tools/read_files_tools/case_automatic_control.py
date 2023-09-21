import os
from typing import Text
from common.setting import ensure_path_sep
from utils.other_tools.read_files_tools.testcase_template import write_testcase_file
from utils.other_tools.read_files_tools.yaml_control import GetYamlData
from utils.other_tools.read_files_tools.get_all_files_path import get_all_files


# 定义了一个名为 TestCaseAutomaticGeneration 的类，用于自动生成测试用例代码。
class TestCaseAutomaticGeneration:

    # 类的 __init__() 方法中初始化了 self.yaml_case_data 和 self.file_path，它们分别用于存储读取的测试用例数据和测试用例文件路径。
    def __init__(self):
        # 它是一个成员变量，用于存储 YAML 格式的测试用例数据。
        self.yaml_case_data = None
        # 它是一个成员变量，用于存储测试用例数据文件的路径。
        self.file_path = None

    # @property 可以将一个方法转换成一个属性，可以像访问普通属性一样，使用 obj.case_date_path 的方式访问该属性。
    @property
    # 定义了一个名为 case_date_path 的属性，并使用了 ensure_path_sep("\\data") 方法返回一个格式化后的路径字符串。
    def case_date_path(self) -> Text:
        """返回 yaml 用例文件路径"""
        return ensure_path_sep("\\data")

    @property
    # 定义了一个名为 case_path 的属性，它指定了测试用例代码存放的路径，并使用了 ensure_path_sep("\\test_case") 方法对路径进行了格式化。
    def case_path(self) -> Text:
        """ 存放用例代码路径"""
        return ensure_path_sep("\\test_case")

    @property
    # 定义了一个名为 allure_epic 的属性，它用于获取指定的 YAML 文件中的测试数据中的 allureEpic 字段。如果该字段不存在或为空，则代码会抛出一个 AssertionError，其中包含了有关错误的详细信息，例如文件路径和字段名称，并提示用户进行检查。
    def allure_epic(self):
        # 从当前实例的 yaml_case_data 属性中获取 case_common 键所对应的值中的 allureEpic 键所对应的值，并将其赋值给 _allure_epic 变量。如果没有找到或者为空，那么 _allure_epic 将会是 None。
        _allure_epic = self.yaml_case_data.get("case_common").get("allureEpic")
        # 检查 _allure_epic 是否为空。如果为空，则使用 assert 关键字抛出一个断言错误，其中包含了错误信息。该错误信息包含了文件路径和缺失的字段名称。
        assert _allure_epic is not None, (
                "用例中 allureEpic 为必填项，请检查用例内容, 用例路径：'%s'" % self.file_path
        )
        # 返回 _allure_epic 的值作为这个属性的值，也就是当前 YAML 文件中的 allureEpic 字段的值。
        return _allure_epic

    @property
    def allure_feature(self):
        # 从 yaml_case_data 属性中获取当前 YAML 文件中的 case_common 键所对应的值中的 allureFeature 键所对应的值，并将其赋值给 _allure_feature 变量。如果没有找到或者为空，那么 _allure_feature 将会是 None。
        _allure_feature = self.yaml_case_data.get("case_common").get("allureFeature")
        # 检查 _allure_feature 是否为空。如果为空，则使用 assert 关键字抛出一个断言错误，其中包含了错误信息。该错误信息包含了文件路径和缺失的字段名称。
        assert _allure_feature is not None, (
                "用例中 allureFeature 为必填项，请检查用例内容, 用例路径：'%s'" % self.file_path
        )
        # 返回 _allure_feature 的值作为这个属性的值，也就是当前 YAML 文件中的 allureFeature 字段的值。
        return _allure_feature

    @property
    def allure_story(self):
        # 从 yaml_case_data 属性中获取当前 YAML 文件中的 case_common 键所对应的值中的 allureStory 键所对应的值，并将其赋值给 _allure_story 变量。如果没有找到或者为空，那么 _allure_story 将会是 None。
        _allure_story = self.yaml_case_data.get("case_common").get("allureStory")
        # 检查 _allure_story 是否为空。如果为空，则使用 assert 关键字抛出一个断言错误，其中包含了错误信息。该错误信息包含了文件路径和缺失的字段名称。
        assert _allure_story is not None, (
                "用例中 allureStory 为必填项，请检查用例内容, 用例路径：'%s'" % self.file_path
        )
        # 返回 _allure_story 的值作为这个属性的值，也就是当前 YAML 文件中的 allureStory 字段的值。
        return _allure_story

    @property
    def file_name(self) -> Text:
        """
        通过 yaml文件的命名，将名称转换成 py文件的名称
        :return:  示例： DateDemo.py
        """
        # 获取 self.file_path 属性中除去 self.case_date_path 前缀的部分，并将其赋值给 yaml_path 变量。
        i = len(self.case_date_path)
        yaml_path = self.file_path[i:]
        # 这里初始化了一个 file_name 变量为 None。
        file_name = None
        # if-elif 循环检查 yaml_path 变量中是否包含 .yaml 或 .yml 字符串，如果包含，则将其替换成 .py 字符串，并将结果赋值给 file_name 变量。路径转换
        if '.yaml' in yaml_path:
            file_name = yaml_path.replace('.yaml', '.py')
        elif '.yml' in yaml_path:
            file_name = yaml_path.replace('.yml', '.py')
        # 返回 file_name 变量的值作为这个方法的返回值。
        return file_name

    @property
    def get_test_class_title(self):
        """
        自动生成类名称
        :return: sup_apply_list --> SupApplyList
        """
        # 获取 self.file_name 中的文件名，去除了 .py 后缀，并将结果赋值给 _file_name 变量。
        _file_name = os.path.split(self.file_name)[1][:-3]
        # 使用 _file_name 的值初始化了一个 _name 列表，并且获取了 _name 的长度。
        _name = _file_name.split("_")
        _name_len = len(_name)
        # for 循环将 _name 中的每个单词首字母转换成大写字母。将文件名称格式，转换成类名称: sup_apply_list --> SupApplyList
        for i in range(_name_len):
            _name[i] = _name[i].capitalize()
        # 将 _name 中的所有单词合并成一个字符串，赋值给 _class_name 变量。
        _class_name = "".join(_name)

        # 返回 _class_name 变量的值作为这个方法的返回值，也就是测试用例所对应的类的名称。
        return _class_name

    @property
    def func_title(self) -> Text:
        """
        函数名称
        :return:
        """
        # 返回了 self.file_name 中的文件名，去除了 .py 后缀，作为函数的返回值。因为 self.file_name 中已经是 .py 后缀的文件名了，所以返回值就是一个函数名。
        return os.path.split(self.file_name)[1][:-3]

    @property
    def spilt_path(self):
        # 使用 os.sep 分隔符将路径字符串拆分成列表，把结果赋值给新的 path 变量。
        path = self.file_name.split(os.sep)
        # 将列表中最后一个元素修改为 "test_" + path[-1]，也就是在该文件名前面添加 "test_"。
        path[-1] = path[-1].replace(path[-1], "test_" + path[-1])
        # spilt_path 方法返回修改后的 path 列表，也即是测试用例文件的所在路径。
        return path

    @property
    def get_case_path(self):
        """
        根据 yaml 中的用例，生成对应 testCase 层代码的路径
        :return: D:\\Project\\test_case\\test_case_demo.py
        """
        # 将 spilt_path 方法返回的路径列表加上分隔符，生成新路径字符串。比如，如果原路径是 ['home', 'user', 'Documents', 'test.py']，那么这一行代码返回的结果就是 'home/user/Documents/test.py'。
        new_name = os.sep.join(self.spilt_path)
        # 调用了 ensure_path_sep 方法，确保路径字符串最后一个字符是路径分隔符。然后，将字符串 "\test_case" 与新生成的路径使用 + 拼接，并返回该字符串。比如，如果原路径是 D:\Project\test.py，那么这一行代码返回的结果就是 D:\Project\test_case\test.py。
        return ensure_path_sep("\\test_case" + new_name)

    @property
    def case_ids(self):
        # 使用列表推导式，遍历 yaml_case_data （即测试数据）中所有的键，如果该键不等于 "case_common"，那么返回该键。也就是说，这里会返回一个列表，表示测试数据中所有测试用例的 id 字段。
        return [k for k in self.yaml_case_data.keys() if k != "case_common"]

    @property
    def get_file_name(self):
        # 判断生成的 testcase 文件名称，需要以test_ 开头
        # 根据 spilt_path 方法返回的文件路径，提取出文件名称。然后，使用 replace 方法将文件名替换为以 "test_" 开头的新文件名。比如，如果原文件名是 sample.py，那么这一行代码返回的结果就是 test_sample.py。
        case_name = self.spilt_path[-1].replace(
            self.spilt_path[-1], "test_" + self.spilt_path[-1]
        )
        # 返回新的测试用例 Python 文件名。
        return case_name

    def mk_dir(self) -> None:
        """ 判断生成自动化代码的文件夹路径是否存在，如果不存在，则自动创建 """
        # 调用 os.path.split 方法，将 get_case_path (测试数据文件路径) 分解成目录路径和文件名，这样就可以提取出测试数据文件所在的目录路径了。
        _case_dir_path = os.path.split(self.get_case_path)[0]
        # 通过 os.path.exists 方法判断目录路径是否存在，如果不存在就使用 os.makedirs 方法创建目录。也就是说，这个函数的作用是创建测试数据文件所在目录的子目录，用于存储生成的测试用例代码文件。
        if not os.path.exists(_case_dir_path):
            os.makedirs(_case_dir_path)

    def get_case_automatic(self) -> None:
        """ 自动生成 测试代码"""
        # 使用 get_all_files 方法获取测试数据文件夹下所有的 YAML 文件路径，并将结果存储到 file_path 变量中。这些 YAML 文件将作为测试用例的源数据。
        file_path = get_all_files(file_path=ensure_path_sep("\\data"), yaml_data_switch=True)

        # 使用 for 循环遍历所有的测试数据文件。
        for file in file_path:
            # if 语句判断当前文件不是代理拦截的 YAML 文件。如果是，则不生成测试用例代码。
            if 'proxy_data.yaml' not in file:
                # 这里调用了 GetYamlData 类的 get_yaml_data 方法，获取 YAML 文件的数据内容，并将其保存到 yaml_case_data 变量中。
                self.yaml_case_data = GetYamlData(file).get_yaml_data()
                # 将当前文件路径保存到 file_path 变量中
                self.file_path = file
                # 调用 mk_dir 方法，在测试用例代码所需的目录路径不存在时创建目录。
                self.mk_dir()
                # 这里调用 write_testcase_file 函数，生成测试用例 Python 文件。
                write_testcase_file(
                    allure_epic=self.allure_epic,
                    allure_feature=self.allure_feature,
                    class_title=self.get_test_class_title,
                    func_title=self.func_title,
                    case_path=self.get_case_path,
                    case_ids=self.case_ids,
                    file_name=self.get_file_name,
                    allure_story=self.allure_story
                )


if __name__ == '__main__':
    # 创建了 TestCaseAutomaticGeneration 类的一个实例，并调用 get_case_automatic 方法，来自动生成测试用例代码。也就是说，当你直接运行这个脚本的时候，就会自动生成测试用例代码。
    TestCaseAutomaticGeneration().get_case_automatic()