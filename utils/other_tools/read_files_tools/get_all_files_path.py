import os


# 函数名为get_all_files，参数为file_path和yaml_data_switch，返回值为列表类型list。
def get_all_files(file_path, yaml_data_switch=False) -> list:
    """
    获取文件路径
    :param file_path: 目录路径
    :param yaml_data_switch: 是否过滤文件为 yaml格式， True则过滤
    :return:
    """
    # 创建一个空列表filename，用于存储文件路径。
    filename = []
    # 使用os.walk函数遍历指定路径下的所有文件和文件夹，并获取每一个子目录的路径、子目录列表和文件列表。
    for root, dirs, files in os.walk(file_path):
        # 遍历文件列表中的每一个文件路径。
        for _file_path in files:
            # 使用os.path.join函数将当前文件所在目录的路径和文件名拼接成完整的文件路径，并赋值给path变量。
            path = os.path.join(root, _file_path)
            # 判断yaml_data_switch参数是否为True，如果是，则继续执行下一步。
            if yaml_data_switch:
                # 判断文件路径中是否包含yaml或.yml，如果是，则将文件路径添加到filename列表中。
                if 'yaml' in path or '.yml' in path:
                    filename.append(path)
            # 如果yaml_data_switch参数为False，则将文件路径添加到filename列表中。
            else:
                filename.append(path)
    # 返回所有文件的路径列表。
    return filename