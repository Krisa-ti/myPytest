import json
import allure
from utils.other_tools.models import AllureAttachmentType


# 定义了一个名为allure_step的函数，它接受两个字符串参数step和var，并不返回任何内容（返回值为None）。
def allure_step(step: str, var: str) -> None:
    """
    :param step: 步骤及附件名称
    :param var: 附件内容
    """
    # 定义一个名为step的allure步骤，包含了需要记录的步骤信息。
    with allure.step(step):
        # 把一个JSON字符串作为附件附加到allure报告的当前步骤中。其中，json.dumps()函数将var对象转换为JSON字符串，然后使用allure.attach()函数将它作为JSON附件附加到报告中。该函数还指定了所附加的附件类型（JSON）。
        allure.attach(
            json.dumps(
                str(var),
                ensure_ascii=False,
                indent=4),
            step,
            allure.attachment_type.JSON)


# 定义了一个名为allure_attach的函数，它接受三个参数source、name和extension，不返回任何内容（返回值为None）。
def allure_attach(source: str, name: str, extension: str):
    """
    allure报告上传附件、图片、excel等
    :param source: 文件路径，相当于传一个文件
    :param name: 附件名称
    :param extension: 附件的拓展名称
    :return:
    """
    # 获取name参数的拓展名，并转换为大写字母。
    _name = name.split('.')[-1].upper()
    # 从AllureAttachmentType枚举中获取与拓展名匹配的枚举值，如果找到了，则将它存储在变量_attachment_type中，否则将_attachment_type设置为None。
    _attachment_type = getattr(AllureAttachmentType, _name, None)

    # 附加一个文件到allure报告中。使用source参数指定文件路径，使用name参数指定文件名，使用attachment_type参数指定文件类型，使用extension参数指定文件的扩展名。
    allure.attach.file(
        source=source,
        name=name,
        attachment_type=_attachment_type if _attachment_type is None else _attachment_type.value,
        extension=extension
    )


# 定义了一个名为allure_step_no的函数，它接受一个字符串参数step，不返回任何内容（返回值为None）。
def allure_step_no(step: str):
    """
    无附件的操作步骤
    :param step: 步骤名称
    :return:
    """
    # 定义一个名为step的allure步骤，包含了需要记录的步骤信息。
    with allure.step(step):
        # 这个代码块为空，因此不执行任何操作。
        pass