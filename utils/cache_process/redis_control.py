"""
redis 缓存操作封装
"""
from typing import Text, Any
import redis


# 定义了一个名为 RedisHandler 的类。这个类用于封装redis缓存的读取，方便其他地方进行调用。__init__ 方法是一个特殊的方法，在创建类的实例时被调用。
class RedisHandler:
    """ redis 缓存读取封装 """

    def __init__(self):
        # 初始化了五个属性，分别是 host、port、database、password、charset。在本例中，这些属性存储了 Redis 的连接信息，包括主机名或 IP 地址、端口号、数据库编号、密码和字符集等。
        self.host = '127.0.0.0'
        self.port = 6000
        self.database = 0
        self.password = 123456
        self.charset = 'UTF-8'
        # 创建了与 Redis 服务器的连接。这里使用了 redis.Redis 类，它是 Redis 的官方 Python 客户端之一，提供了与 Redis 进行通信的接口。在这里，我们把 Redis 的连接信息作为参数传给 redis.Redis()，然后创建一个 Redis 连接实例，保存在 RedisHandler 对象的 redis 属性中。其中，decode_responses=True 的作用是将 Redis 匹配的值自动转换为 Python 字符串，避免了手动编码/解码的繁琐过程。
        self.redis = redis.Redis(
            self.host,
            port=self.port,
            password=self.password,
            decode_responses=True,
            db=self.database
        )

    # 函数set_string，用来将一个字符串存储到 Redis 缓存中。它有 6 个参数，其中第一个参数 name 是必需的，表示要写入缓存的名称。第二个参数 value 是必需的，表示要写入缓存的值。第三个参数 exp_time 是可选的，表示设置缓存的过期时间（以秒为单位）。第四个参数 exp_milliseconds 是可选的，表示设置缓存的过期时间（以毫秒为单位）。第五个参数 name_not_exist 是可选的，如果设置为 True，则仅在缓存中没有该名称时才执行写入操作。第六个参数 name_exit 是可选的，如果设置为 True，则仅在缓存中存在该名称时才执行写入操作。
    def set_string(
            self, name: Text,
            value, exp_time=None,
            exp_milliseconds=None,
            name_not_exist=False,
            name_exit=False) -> None:
        """
        缓存中写入 str（单个）
        :param name: 缓存名称
        :param value: 缓存值
        :param exp_time: 过期时间（秒）
        :param exp_milliseconds: 过期时间（毫秒）
        :param name_not_exist: 如果设置为True，则只有name不存在时，当前set操作才执行（新增）
        :param name_exit: 如果设置为True，则只有name存在时，当前set操作才执行(修改）
        :return:
        """
        # 使用 redis.set() 方法来写入字符串到 Redis 缓存中。redis 是 RedisHandler 类的一个属性，它保存了连接到 Redis 的客户端实例。在这里，我们为 redis.set() 方法传递了 name 和 value 参数。ex 参数表示设置缓存的过期时间（以秒为单位），px 参数表示设置缓存的过期时间（以毫秒为单位），nx 参数表示只有在缓存中没有该名称时才执行写入操作，xx 参数表示仅在缓存中存在该名称时才执行写入操作。
        self.redis.set(
            name,
            value,
            ex=exp_time,
            px=exp_milliseconds,
            nx=name_not_exist,
            xx=name_exit
        )

    # 函数key_exit，用于判断 Redis 缓存中的一个键是否存在。它只有一个参数 key，表示要检查的键名称。
    def key_exit(self, key: Text):
        """
        判断redis中的key是否存在
        :param key:
        :return:
        """
        # 返回布尔值（True 或 False），表示指定的键是否存在于 Redis 缓存中。在这里，我们使用了 self.redis.exists() 方法，它是 Redis 提供的一个方法，用于检查指定的 key 是否存在于 Redis 缓存中。
        return self.redis.exists(key)

    # 函数incr，用于递增 Redis 缓存中的一个键的值。它只有一个参数 key，表示要递增值的键名称。
    def incr(self, key: Text):
        """
        使用 incr 方法，处理并发问题
        当 key 不存在时，则会先初始为 0, 每次调用，则会 +1
        :return:
        """
        # 使用 incr() 方法来增加一个 Redis 缓存中的键的值。在这里，我们使用 self.redis.incr() 方法，它是 Redis 提供的一个方法，自动增加指定 key 中的值，如果该 key 不存在，则会先创建并初始化为 0，然后再递增。
        self.redis.incr(key)

    # 这是一个返回类型注解，以内联注释代码的形式表示返回值类型为 Text。


'''
函数get_key，用于获取
Redis
缓存中指定键名的值。它只有一个参数
name，表示要获取值的键名称。
'''

def get_key(self, name: Any) -> Text:
    """
    读取缓存
    :param name:
    :return:
    """
    # 使用 get() 函数来获取 Redis 缓存中指定 name 的值。在这里，我们使用了 self.redis.get() 方法，它是 Redis 提供的一个函数，用于获取指定键名称 name 的值。
    return self.redis.get(name)


# 函数set_many，用于批量设置 Redis 缓存中的多个键值对。它支持两种方式来设置缓存，即列表方式和关键字参数方式。使用 *args 和 **kwargs 可以接收这两种方式传入的值。
def set_many(self, *args, **kwargs):
    """
    批量设置
    支持如下方式批量设置缓存
    eg: set_many({'k1': 'v1', 'k2': 'v2'})
        set_many(k1="v1", k2="v2")
    :return:
    """
    # 使用 mset() 方法来批量设置 Redis 缓存中的多个键值对。在这里，我们使用了 self.redis.mset() 方法，它是 Redis 提供的一个方法，用于设置多个键值对。
    self.redis.mset(*args, **kwargs)


# 函数get_many，用于获取 Redis 缓存中多个键的值。它只有一个参数 *args，表示要获取值的键名称列表或元组，支持传入多个键。使用 *args 可以接收任意数量的参数。
def get_many(self, *args):
    """获取多个值"""
    # 使用 mget() 方法来获取 Redis 缓存中多个键的值，然后返回获取的结果。在这里，我们使用了 self.redis.mget() 方法，它是 Redis 提供的一个方法，用于获取多个键的值。
    results = self.redis.mget(*args)
    return results


# 函数del_all_cache，用于清除 Redis 缓存中所有的数据。
def del_all_cache(self):
    """清理所有现在的数据"""
    # 使用 keys() 方法获取 Redis 缓存中所有的键的列表，然后使用 del_cache() 方法来依次清除每一个键对应的数据。self.redis.keys() 方法返回一个列表，包含了 Redis 缓存中所有的键。
    for key in self.redis.keys():
        self.del_cache(key)


# 函数del_cache，用于删除 Redis 缓存中指定键的数据。
def del_cache(self, name):
    """
    删除缓存
    :param name:
    :return:
    """
    # 使用 delete() 方法来删除 Redis 缓存中指定 name 键的数据。self.redis.delete() 方法是 Redis 提供的一个方法，用于删除指定的键。
    self.redis.delete(name)