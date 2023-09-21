"""
缓存文件处理
"""

import os
from typing import Any, Text, Union
from common.setting import ensure_path_sep
from utils.other_tools.exceptions import ValueNotFoundError


# 定义了 Cache 类，用于读写缓存文件。
class Cache:
    """ 设置、读取缓存 """

    # 类的初始化函数 __init__(self, filename: Union[Text, None]) -> None。__init__ 函数在类实例化时被调用，self 参数指向实例化的对象。filename 是一个可选参数，用于指定缓存文件的名称。函数定义中，Union[Text, None] 表示 filename 可以为字符串或者 None。
    def __init__(self, filename: Union[Text, None]) -> None:
        # 如果filename不为空，则操作指定文件内容
        if filename:
            self.path = ensure_path_sep("\\cache" + filename)
        # 如果filename为None，则操作所有文件内容
        else:
            self.path = ensure_path_sep("\\cache")

    # 定义了一个名为 set_cache 的函数，它是一个类的方法，所以第一个参数 self 代表类的实例。该函数有两个参数：key 和 value，分别表示键和值，它们将被存在缓存中。指定的数据类型和值是用于提供多个键值对的支持，给缓存系统添加更多的值。这些键值对可以被序列化，即转换成字符串形式，并被写入到缓存文件系统中。函数的返回类型是 None，这意味着该函数不返回任何值。这是因为该函数的作用是设置缓存并将其写入到文件中，而不是返回数据。
    def set_cache(self, key: Text, value: Any) -> None:
        # 使用open()函数打开指定路径的缓存文件，并以“写入”模式('w')打开文件。接着，将要写入的键值对转换成一个字典类型，并使用str()函数将其转换成一个字符串。最后，使用write()函数将转换后的字符串写入打开的文件中。这个方法仅适用于设置单个键值对的字典类型缓存数据。如果缓存文件之前已经存在，则会被新缓存内容替换。
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(str({key: value}))

    # 定义了一个名为set_caches()的方法，它接受一个任意类型的参数value，并且没有返回值。该方法的作用是将参数value保存到缓存文件中。
    def set_caches(self, value: Any) -> None:
        """
        设置多组缓存数据
        :param value: 缓存内容
        :return:
        """
        # 这行代码使用with语句以写入模式('w')打开指定路径的缓存文件，并将文件对象赋值给变量file。这将会清空文件并写入新的数据。
        with open(self.path, 'w', encoding='utf-8') as file:
            # 这行代码将参数value转换成字符串并写入到缓存文件中。注意，这个方法并没有做任何格式化或序列化数据的操作，因此需要在调用该方法的地方确保传入的数据是可以被转换成字符串的。
            file.write(str(value))

    # 定义了一个名为get_cache()的方法，它没有任何参数，且返回一个任意类型的对象。
    def get_cache(self) -> Any:
        """
        获取缓存数据
        :return:
        """
        # 这行代码使用with语句以只读模式('r')打开指定路径的缓存文件，并将文件对象赋值给变量file。with语句会自动关闭文件，并确保在文件操作出现异常时做出正确的清理操作。
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                # 这行代码读取打开的文件中的所有内容，并将其作为一个字符串返回。如果文件为空，则会返回一个空字符串。
                return file.read()
        # 这行代码表示当try块中的代码抛出FileNotFoundError异常时，跳过这个异常，并继续执行下去。这样做是为了确保程序不会因为缓存文件不存在而崩溃。
        except FileNotFoundError:
            pass

    # 定义了一个名为clean_cache()的方法，它没有接受参数，也没有返回值。该方法的作用是删除指定的缓存文件。
    def clean_cache(self) -> None:

        """删除所有缓存文件"""

        # 这行代码使用os.path模块中的exists()函数检查指定路径的文件或目录是否存在。如果文件不存在，就会抛出FileNotFoundError异常，提示用户该文件不存在。
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"您要删除的缓存文件不存在 {self.path}")
        # 这行代码使用os模块中的remove()函数删除指定文件。在这里，我们使用self.path属性指定要删除的缓存文件路径。
        os.remove(self.path)

    # @classmethod是一个装饰器，它用于定义一个类方法。类方法属于类本身而非类的实例，因此可以在不创建类实例的情况下调用它们。类方法的第一个参数始终是类本身，通常被命名为cls。通过cls参数，我们可以访问和修改类属性，或者调用其他类方法。如果没有@classmethod装饰器，那么定义的方法将是实例方法，只能由实例调用。
    @classmethod
    # 定义了一个名为clean_all_cache()的方法，该方法没有接收参数，也没有返回值。该方法的作用是清除目标目录下所有的缓存文件。
    def clean_all_cache(cls) -> None:

        """
        清除所有缓存文件
        :return:
        """
        # 这行代码调用了之前定义的辅助函数ensure_path_sep()，用于确保缓存目录路径以目录分隔符结尾，避免后续拼接路径时出现错误。
        cache_path = ensure_path_sep("\\cache")
        # 这行代码使用os模块中的listdir()函数获取指定目录下的文件列表，并将其存储在list_dir变量中。
        list_dir = os.listdir(cache_path)
        # 这个循环遍历所有文件，并使用os模块中的remove()函数将每个文件从磁盘上删除。在这里，我们使用cache_path指定缓存文件的路径。每个文件的名称由listdir()函数返回的列表中的元素提供。
        for i in list_dir:
            os.remove(cache_path + i)


# 定义了一个空字典_cache_config，用于存储缓存数据。在该变量中，缓存数据以键值对的形式存储，其中键是缓存名称，值是任何Python对象，表示缓存数据。
_cache_config = {}


# 定义了一个名为CacheHandler的类。
class CacheHandler:

    @staticmethod
    # 这个get_cache()静态方法接收一个参数cache_data，该参数是缓存名称。该方法从_cache_config中获取指定缓存数据，并返回它。如果缓存数据不存在，则会引发ValueNotFoundError异常，提示缓存数据未找到。
    def get_cache(cache_data):
        try:
            return _cache_config[cache_data]
        except KeyError:
            raise ValueNotFoundError(f"{cache_data}的缓存数据未找到，请检查是否将该数据存入缓存中")

    @staticmethod
    # 这个update_cache()静态方法接收两个参数，cache_name和value。它将value添加或更新到_cache_config字典中指定cache_name的键。
    def update_cache(*, cache_name, value):
        _cache_config[cache_name] = value