import os


# 函数定义，输入参数为要删除的路径名。
def del_file(path):
    """删除目录下的文件"""
    # 获取指定路径下的所有子文件和子目录，并存储到 list_path 变量中。
    list_path = os.listdir(path)
    # 依次遍历 list_path 中的每个目录和文件，将它们的绝对路径存储到 c_path 变量中。
    for i in list_path:
        c_path = os.path.join(path, i)
        # 如果当前路径 c_path 是一个目录，则递归调用 del_file 函数，继续删除目录中的文件和子目录。
        if os.path.isdir(c_path):
            del_file(c_path)
        # 如果当前路径 c_path 是一个文件，则直接删除它。
        else:
            os.remove(c_path)
# 这个函数会递归地删除指定的路径下所有的文件和子目录，直到删除完毕并返回。