import os
from typing import Text


# 定义一个函数`root_path()`，用于获取根路径。
def root_path():
    """ 获取 根路径 """
    # 使用`os`模块的三个函数，分别获取当前文件所在目录的上两级目录的绝对路径，并将其赋值给变量`path`，也就是获取根路径。
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 将获得的根路径返回。
    return path


# 定义一个名为`ensure_path_sep()`的函数，接收一个字符串类型的参数`path`，并指定该函数返回一个字符串类型的值。
def ensure_path_sep(path: Text) -> Text:
    """兼容 windows 和 linux 不同环境的操作系统路径 """
    # 如果`path`中含有`/`这个字符。
    if "/" in path:
        # # 将`path`按照`/`拆分成一个列表，并使用`os.sep`将其拼接成一个路径，将拼接好的路径赋给变量`path`。`os.sep`用来获取当前操作系统的路径分隔符，以便在不同操作系统中正确地处理路径。
        path = os.sep.join(path.split("/"))
        # 如果`path`中含有`\\`这个字符。
    if "\\" in path:
        # 将`path`按照`\\`拆分成一个列表，并使用`os.sep`将其拼接成一个路径，将拼接好的路径赋给变量`path`。
        path = os.sep.join(path.split("\\"))

    # 返回根路径和拼接好的路径，组成完整的路径。可以看出，该函数的作用是将路径中的所有`/`和`\\`都替换成当前操作系统的路径分隔符，以免在不同操作系统中出现路径错误。
    return root_path() + path
'''
以上代码主要是关于路径处理的相关函数。
总的来说，以上代码是一个比较通用的路径处理函数集合，可以在不同的操作系统中兼容地处理路径问题。
'''
