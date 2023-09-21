"""
Assert 断言类型
"""

from typing import Any, Union, Text
from collections import *


# 定义了名为 equals 的函数，使用 Any 类型注解表示该函数的参数类型可以是任意类型。具体来说，check_value 和 expect_value 参数表示要比较的两个值，message 参数为可选参数，用于在断言失败时输出自定义的错误信息。
def equals(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """判断是否相等"""

    # 使用 Python 自带的 assert 语句进行比较，如果 check_value 等于 expect_value，则不做处理；如果不等，则抛出 AssertionError 异常，其中的错误消息为 message。
    assert check_value == expect_value, message


# 定义了一个名为 less_than 的函数，该函数有三个参数：check_value 表示要检查的实际值，必须为 int 或 float 类型；expect_value 表示预期结果，也必须为 int 或 float 类型。这两个参数都使用了类型注解，用于指定参数的类型，从而提高代码的可读性和可理解性。第三个参数 message 是可选参数，可以用来在断言失败时输出自定义的错误信息。这个函数的功能是判断实际结果是否小于预期结果。
def less_than(
        check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""
):
    """判断实际结果小于预期结果"""
    # 使用 assert 语句对实际值和预期值进行比较。如果实际结果小于预期结果，则 assert 语句不做任何事情，程序会继续执行；否则，assert 语句抛出一个 AssertionError 异常，其中的错误消息是参数 message。在测试代码中，如果出现了异常，测试框架会记录该测试用例失败。这种方式可以方便地验证代码是否按照预期执行。
    assert check_value < expect_value, message


def less_than_or_equals(
        check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""):
    """判断实际结果小于等于预期结果"""
    assert check_value <= expect_value, message


def greater_than(
        check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""
):
    """判断实际结果大于预期结果"""
    assert check_value > expect_value, message


def greater_than_or_equals(
        check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""
):
    """判断实际结果大于等于预期结果"""
    assert check_value >= expect_value, message


def not_equals(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """判断实际结果不等于预期结果"""
    assert check_value != expect_value, message


def string_equals(
        check_value: Text, expect_value: Any, message: Text = ""
):
    """判断字符串是否相等"""
    assert check_value == expect_value, message


# 定义了一个名为 length_equals 的函数，该函数有三个参数：check_value 表示要检查的值，必须为字符串类型；expect_value 表示期望长度，必须是整数类型。第三个参数 message 是可选参数，用于在断言失败时输出自定义的错误信息。该函数的功能是判断输入字符串的长度是否等于期望长度。
def length_equals(
        check_value: Text, expect_value: int, message: Text = ""
):
    """判断长度是否相等"""
    # 用于检查传入的 expect_value 是否是 int 类型。如果不是，则抛出一个异常，告诉我该值需要是整数类型。
    assert isinstance(
        expect_value, int
    ), "expect_value 需要为 int 类型"
    # 用于比较输入字符串的长度是否等于期望长度。如果两个长度相等，则这个 assert 语句不会做任何事情，程序会继续执行。否则，assert 语句会抛出一个 AssertionError 异常，并且错误信息为参数 message。在测试代码中，如果出现异常，测试框架将记录该测试用例失败。
    assert len(check_value) == expect_value, message


def length_greater_than(
        check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断长度大于"""
    assert isinstance(
        expect_value, (float, int)
    ), "expect_value 需要为 float/int 类型"
    assert len(str(check_value)) > expect_value, message


def length_greater_than_or_equals(
        check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断长度大于等于"""
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value 需要为 float/int 类型"
    assert len(check_value) >= expect_value, message


def length_less_than(
        check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断长度小于"""
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value 需要为 float/int 类型"
    assert len(check_value) < expect_value, message


def length_less_than_or_equals(
        check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断长度小于等于"""
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value 需要为 float/int 类型"
    assert len(check_value) <= expect_value, message


def contains(check_value: Any, expect_value: Any, message: Text = ""):
    """判断期望结果内容包含在实际结果中"""
    assert isinstance(
        check_value, (list, tuple, dict, str, bytes)
    ), "expect_value 需要为  list/tuple/dict/str/bytes  类型"
    assert expect_value in check_value, message


def contained_by(check_value: Any, expect_value: Any, message: Text = ""):
    """判断实际结果包含在期望结果中"""
    assert isinstance(
        expect_value, (list, tuple, dict, str, bytes)
    ), "expect_value 需要为  list/tuple/dict/str/bytes  类型"

    assert check_value in expect_value, message


def startswith(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """检查响应内容的开头是否和预期结果内容的开头相等"""
    assert str(check_value).startswith(str(expect_value)), message


def endswith(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """检查响应内容的结尾是否和预期结果内容相等"""
    assert str(check_value).endswith(str(expect_value)), message


def setlist(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """检查去重后的响应内容是否和预期结果内容相等"""
    assert check_value == expect_value, message


def str_set(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """list转换str 去重无序判断是否相等"""
    list_check_value = str(check_value)
    list_expect_value = str(expect_value)
    assert set(list_check_value) == set(list_expect_value), message


def counter(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """O(n)：Counter()方法是最好的（如果你的对象是可散列的）"""
    list_check_value = str(check_value)
    list_expect_value = str(expect_value)
    assert Counter(list_check_value) == Counter(list_expect_value), message

'''

这段代码定义了多个断言类型的实现函数，比如
`equals`
函数用于判断两个值是否相等，`less_than`
函数用于判断实际结果是否小于预期结果，等等。这些函数将会在
`AssertUtil`
类的
`_assert`
方法中进行调用，用于完成对应的断言操作。

这些函数的参数和返回值分别如下：

- 参数
`check_value`：需要进行断言检查的值；
- 参数
`expect_value`：期望的值；
- 参数
`message`（可选）：当断言检查失败时，返回的自定义错误信息；
- 返回值：当断言检查失败时，会抛出
`AssertionError`
异常。

这些函数的实现方式非常简单，只需要调用
Python
中的
`
assert ` 语句即可。例如
`equals`
函数的实现如下：
'''



def equals(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """判断是否相等"""

    assert check_value == expect_value, message


'''
这个函数的作用是判断
`check_value`
是否等于
`expect_value`，如果不相等，抛出断言错误，并输出自定义错误信息
`message`（如果提供了的话）。
'''

