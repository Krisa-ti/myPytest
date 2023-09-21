import json

import xlrd
from xlutils.copy import copy
from common.setting import ensure_path_sep


# 函数名为get_excel_data，参数为sheet_name和case_name，返回值为列表类型list。
def get_excel_data(sheet_name: str, case_name: any) -> list:
    """
    读取 Excel 中的数据
    :param sheet_name: excel 中的 sheet 页的名称
    :param case_name: 测试用例名称
    :return:
    """
    # 创建一个空列表res_list，用于存储读取Excel中的数据。
    res_list = []

    # 用于将路径中的斜杠转换为对应系统的分隔符。这里将Excel文件所在的路径作为参数传入，并将结果赋值给excel_dire变量。
    excel_dire = ensure_path_sep("\\data\\TestLogin.xls")
    # 使用xlrd库打开Excel文件，并将结果赋值给work_book变量。formatting_info=True表示保留Excel中的格式信息。
    work_book = xlrd.open_workbook(excel_dire, formatting_info=True)

    # 获取指定名称的子表（sheet）并将结果赋值给work_sheet变量。
    work_sheet = work_book.sheet_by_name(sheet_name)
    # 初始化变量idx为0，用于记录行数。
    idx = 0
    # 使用col_values方法获取第一列的所有值，并遍历每一个值。
    for one in work_sheet.col_values(0):
        # 判断当前行是否包含指定的测试用例名称，如果是，则继续执行下一步。
        if case_name in one:
            # 获取当前行第10列（索引从0开始）的值，并将结果赋值给req_body_data变量，用于存储请求体数据。
            req_body_data = work_sheet.cell(idx, 9).value
            # 获取当前行第12列（索引从0开始）的值，并将结果赋值给resp_data变量，用于存储响应数据。
            resp_data = work_sheet.cell(idx, 11).value
            # 将请求体数据和响应数据组成一个元组，并添加到res_list列表中。
            res_list.append((req_body_data, json.loads(resp_data)))
        # 行数加1，继续读取下一行的数据。
        idx += 1
    # 返回读取到的Excel数据列表。
    return res_list


# 函数名为set_excel_data，参数为sheet_index，返回值为元组类型tuple。
def set_excel_data(sheet_index: int) -> tuple:
    """
    excel 写入
    :return:
    """
    # 用于指定Excel文件的路径。这里使用相对路径来指定文件所在的位置。
    excel_dire = '../data/TestLogin.xls'
    # 使用xlrd库打开Excel文件，并将结果赋值给work_book变量。formatting_info=True表示保留Excel中的格式信息。
    work_book = xlrd.open_workbook(excel_dire, formatting_info=True)
    # 使用xlutils.copy库的copy函数复制一份Excel文件，并将结果赋值给work_book_new变量。这里使用xlutils库是因为xlrd库只能读取Excel文件，不能进行写入操作。
    work_book_new = copy(work_book)

    # 获取指定索引的子表（sheet）并将结果赋值给work_sheet_new变量，用于写入数据
    work_sheet_new = work_book_new.get_sheet(sheet_index)
    # 返回复制后的Excel文件和要写入数据的子表（sheet）。
    return work_book_new, work_sheet_new


