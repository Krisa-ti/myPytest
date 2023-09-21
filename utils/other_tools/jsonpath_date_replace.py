# 定义一个名为 jsonpath_replace 的函数，该函数接受三个参数，分别是 change_data、 key_name 和 data_switch，用于处理 JSONPath 数据。
def jsonpath_replace(change_data, key_name, data_switch=None):
    """处理jsonpath数据"""
    # 定义 _new_data 变量，初始值为 key_name 与一个空字符串拼接。
    _new_data = key_name + ''
    # 使用 for 循环遍历 change_data 变量中的每一个元素，i 是遍历时用于找到元素的迭代变量。
    for i in change_data:
        # 如果检测到 JSONPath 路径中存在 $，则什么都不做，直接跳过。
        if i == '$':
            pass
        # 如果 data_switch 为 None 并且元素为 "data"，则在 _new_data 的后面追加一个字符串 '.data' 。
        elif data_switch is None and i == "data":
            _new_data += '.data'
        # 如果检测到元素是索引（即 i 表示一个列表元素），则在 _new_data 的后面追加一对方括号和 /i[1:-1]/。
        elif i[0] == '[' and i[-1] == ']':
            _new_data += "[" + i[1:-1] + "]"
        # 如果是「非索引形式」的元素，则在 _new_data 的后面追加一对方括号和引号组成的字符串 /"/i/"/（即元素 i 用引号括起来）。
        else:
            _new_data += '[' + '"' + i + '"' + "]"
    # 返回最终的 _new_data 变量，其中包含了处理后的字符串形式的 JSONPath。
    return _new_data

