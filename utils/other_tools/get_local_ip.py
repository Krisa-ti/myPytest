import socket


# 定义一个名为 get_host_ip 的函数。
def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    # 初始化一个变量 '_s' ，并将其值置为 None。
    _s = None
    try:
        # # 使用 Python 标准库中的 socket 模块创建一个 socket 对象 _s。其中 socket.AF_INET 表示建立面向 IPv4 的网络套接字， socket.SOCK_DGRAM 表示该套接字是数据报类型。接着，使用 connect 方法将 socket 对象 _s 连接到 ('8.8.8.8', 80) 这个公共 DNS 服务器。然后，使用 getsockname() 方法获取本机的 IP 地址，用变量 l_host 保存。
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.connect(('8.8.8.8', 80))
        l_host = _s.getsockname()[0]
    # finally 语句块中关闭 socket 连接，确保资源释放。
    finally:
        _s.close()

    # 返回 l_host，本机 IP 地址。
    return l_host