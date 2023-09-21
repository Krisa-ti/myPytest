"""
# @describe: 判断程序是否每次会更新依赖库，如有更新，则自动安装
"""
import os
import chardet
from common.setting import ensure_path_sep
from utils.logging_tool.log_control import INFO
from utils import config

# 这是一个使用 os.system 命令来执行系统命令 pip3 install chardet 的语句。该语句用于在 Python 环境中通过 PyPI 安装 chardet 库。 os.system 函数将给定的字符串作为一个命令运行，并返回其执行结果。具体来说，pip3 是 Python3 中的包管理器工具，install 是 它的一个子命令，用于安装第三方库，而 chardet 则是要安装的库名。执行该语句将自动下载并安装 chardet 库，以便在 Python 中使用它的功能。
os.system("pip3 install chardet")


# 定义一个名为 InstallRequirements 的类。
class InstallRequirements:
    """ 自动识别安装最新的依赖库 """

    # 定义该类的构造函数，它将在创建类的新实例时自动调用。
    def __init__(self):
        # 设置 version_library_comparisons.txt 文件的路径。函数ensure_path_sep用于确保路径分隔符为正斜杠。
        self.version_library_comparisons_path = ensure_path_sep("\\utils\\other_tools\\install_tool\\") \
 \
            # 设置 requirements.txt 文件的路径。该路径使用os模块函数os.path.dirname获取当前文件所在的目录两级上的目录（即项目的根目录），并拼接 os.sep 和文件名requirements.txt。                                      + "version_library_comparisons.txt"
        self.requirements_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) \
                                 + os.sep + "requirements.txt"

        # 从 config 中获取镜像 URL，该 URL 作为从镜像源下载软件包的基础 URL。
        self.mirror_url = config.mirror_source

    # 定义一个名为 read_version_library_comparisons_txt 的方法，它将从文件中读取字符串，并返回读取的内容。
    def read_version_library_comparisons_txt(self):
        """
        获取版本比对默认的文件
        @return:
        """
        # 使用 with 语句来安全地打开指定路径下的文件 version_library_comparisons.txt 并读取其内容。open() 函数的第一个参数是文件路径，第二个参数是打开文件的模式，r 代表只读模式，第三个参数是文件编码方式，这里是 utf-8。
        with open(self.version_library_comparisons_path, 'r', encoding="utf-8") as file:
            # 返回打开文件后读取的内容，并使用 strip 函数去除字符串开头和结尾的空格。
            return file.read().strip(' ')

    @classmethod
    # 定义一个名为 check_charset 的类方法，它的第一个参数是 cls，指向当前类对象（而不是实例对象）。第二个参数是 file_path，表示要检查字符集的文件路径。
    def check_charset(cls, file_path):
        """获取文件的字符集"""
        # 使用 with 语句打开指定文件，并使用二进制模式(rb)打开文件。
        with open(file_path, "rb") as file:
            # 读取文件前四个字节的内容。这足以确定文件的编码方式，因为对于大多数文件来说，其编码方式信息包含在开头的几个字节中。
            data = file.read(4)
            # 使用 chardet 模块检测文件的编码方式，并将检测到的编码方式存储在 charset 变量中。
            charset = chardet.detect(data)['encoding']
        # 返回检测到的文件编码方式。
        return charset

    # 定义一个名为 read_requirements 的方法，它将读取指定文件的内容，并返回文件的内容。
    def read_requirements(self):
        """获取安装文件"""
        # 创建一个空字符串，用于存储文件内容。
        file_data = ""
        # 打开指定文件以读取其内容，并使用 with 语句确保安全关闭文件。 self.requirements_path 是文件的路径， r 表示以只读模式打开该文件， encoding 参数使用 check_charset 函数来确定文件的编码方式。
        with open(
                self.requirements_path,
                'r',
                encoding=self.check_charset(self.requirements_path)
        ) as file:
            # 读取打开文件的每一行，将其作为 line 变量的值。
            for line in file:
                # 检查读取的行是否包含某个字符串“[0m”，并用空字符串替换该字符串。于是获得的新字符串添加到 file_data 字符串中。
                if "[0m" in line:
                    line = line.replace("[0m", "")
                file_data += line

        # 重新打开指定文件以覆盖原始文件，然后将 file_data 中的内容写入文件，实现删除了 “[0m” 字符串的目的。
        with open(
                self.requirements_path,
                "w",
                encoding=self.check_charset(self.requirements_path)
        ) as file:
            file.write(file_data)

        # 返回读取的内容字符串。
        return file_data

    # 定义名为 text_comparison 的方法，其目的是检查库的依赖项是否有更新，并自动安装更新的依赖项。
    def text_comparison(self):
        """
        版本库比对
        @return:
        """
        # 使用 self.read_version_library_comparisons_txt() 方法读取存储了库依赖项版本信息的文件内容，并将其赋值给 read_version_library_comparisons_txt 变量（可能是一个字符串）。
        read_version_library_comparisons_txt = self.read_version_library_comparisons_txt()
        # 使用 self.read_requirements() 方法读取当前库依赖项的版本信息，并将其存储在 read_requirements 变量中。
        read_requirements = self.read_requirements()
        # 检查 read_version_library_comparisons_txt 变量和 read_requirements 变量是否相等。如果相等，则没有更新的库依赖项，并输出相关信息；否则，将进行安装更新。
        if read_version_library_comparisons_txt == read_requirements:
            INFO.logger.info("程序中未检查到更新版本库，已为您跳过自动安装库")
        # 程序中如出现不同的文件，则安装
        else:
            INFO.logger.info("程序中检测到您更新了依赖库，已为您自动安装")
            # 如果应用程序中存在版本差异，则使用 os.system 方法调用 pip3 安装库依赖项。
            os.system(f"pip3 install -r {self.requirements_path}")
            # 更新依赖项库版本信息文件，将当前库依赖项写入文件以供比较使用。
            with open(self.version_library_comparisons_path, "w",
                      encoding=self.check_charset(self.requirements_path)) as file:
                file.write(read_requirements)

