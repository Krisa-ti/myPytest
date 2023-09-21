"""
mysql 封装，支持 增、删、改、查
"""
import ast
import datetime
import decimal
from warnings import filterwarnings
import pymysql
from typing import List, Union, Text, Dict
from utils import config
from utils.logging_tool.log_control import ERROR
from utils.other_tools.read_files_tools.regular_control import sql_regular
from utils.other_tools.read_files_tools.regular_control.regular_control import cache_regular
from utils.other_tools.exceptions import DataAcquisitionFailed, ValueTypeError

# 用于设置在连接 MySQL 服务器时忽略掉一些 MySQL 数据库发出的警告信息。
filterwarnings("ignore", category=pymysql.Warning)


# 定义一个MysqlDB类，在此类中，我们封装了一些操作MySQL数据库的方法。
class MysqlDB:
    """ mysql 封装 """
    # 当config.mysql_db.switch为True时，才会执行类定义的代码。这里的意思是如果配置文件中开启了MySQL开关，才会继续连接MySQL。
    if config.mysql_db.switch:

        # 定义类的初始化方法。
        def __init__(self):
            # try语句块用来捕获抛出的异常。
            try:
                # 使用pymysql库建立数据库连接。
                self.conn = pymysql.connect(
                    # 连接数据库的主机地址。
                    host=config.mysql_db.host,
                    # 连接数据库的用户名。
                    user=config.mysql_db.user,
                    # 连接数据库的密码。
                    password=config.mysql_db.password,
                    # 连接数据库的端口号。
                    port=config.mysql_db.port
                )

                # 通过连接对象self.conn的cursor()方法来获取游标self.cur，并指定返回结果为字典格式。
                self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            # 捕捉到异常时执行的语句，这里是打印连接失败的日志信息。
            except AttributeError as error:
                # 将错误信息输出到日志文件中，以便后续查找错误原因。
                ERROR.logger.error("数据库连接失败，失败原因 %s", error)

        # 定义了一个特殊方法__del__，在对象销毁时自动调用，用于释放该类所有的资源，如关闭数据库连接等。
        def __del__(self):
            # try语句用于异常处理，尝试关闭游标和连接。
            try:
                # 关闭游标
                self.cur.close()
                # 关闭连接
                self.conn.close()
            # 捕捉到异常时执行的语句，这里是打印连接失败的日志信息。
            except AttributeError as error:
                # 记录日志信息，记录连接失败的原因。
                ERROR.logger.error("数据库连接失败，失败原因 %s", error)

        # 总之，该方法是一个析构函数，用于在对象销毁时释放数据库连接和游标。为了避免未释放资源的错误，像在这里这样释放资源是一个好的编程习惯。

        # 定义了一个名为query的方法，用于执行查询语句。sql表示要执行的查询语句。tate="all"表示查询的类型，默认为all，即查询所有数据。
        def query(self, sql, state="all"):
            """
                查询
                :param sql:
                :param state:  all 是默认查询全部
                :return:
                """
            # try语句用于异常处理，尝试执行查询语句。
            try:
                # 执行传入的SQL查询语句。
                self.cur.execute(sql)

                # 如果查询的类型是all，即查询所有数据。
                if state == "all":
                    # 使用fetchall方法获取全部查询结果。
                    data = self.cur.fetchall()
                # 否则即查询单条。
                else:
                    # 使用fetchone方法获取单条查询结果。
                    data = self.cur.fetchone()
                # 返回查询结果。
                return data
            # 捕捉到异常时执行的语句，这里是打印连接失败的日志信息。
            except AttributeError as error_data:
                # 记录日志信息，记录连接失败的原因。
                ERROR.logger.error("数据库连接失败，失败原因 %s", error_data)
                # 将异常继续向上抛出，让函数调用者来处理异常。
                raise

        # 总之，这个方法是一个查询类的方法，用于执行SQL查询语句，并且返回查询结果。在查询语句中，使用了fetchall和fetchone方法获取查询结果。

        # 定义了一个名为execute的方法，用于执行更新、删除和新增操作。sql表示要执行的SQL语句。
        def execute(self, sql: Text):
            """
                更新 、 删除、 新增
                :param sql:
                :return:
                """
            try:
                # 执行传入的SQL更新、删除和新增语句，并返回受影响行数。
                rows = self.cur.execute(sql)
                # 执行提交事务，将更改提交到数据库中。
                self.conn.commit()
                # 返回受影响的行数。
                return rows
            # 捕捉到异常时执行的语句，这里是打印连接失败的日志信息。
            except AttributeError as error:
                # 记录日志信息，记录连接失败的原因。
                ERROR.logger.error("数据库连接失败，失败原因 %s", error)
                # 执行回滚操作，撤销刚才执行的更改。
                self.conn.rollback()
                # 将异常继续向上抛出，让函数调用者来处理异常。
                raise

        # 总之，这个方法是一个更新、删除和新增类的方法，用于执行SQL更新、删除和新增语句，并返回受影响的行数。在执行SQL语句后，使用commit方法提交更改，并使用rollback方法回滚事务。

        # 这个装饰器用于将方法声明为类方法，而不是实例方法，即使没有实例仍然可以调用
        @classmethod
        # 定义了一个名为sql_data_handler的类方法，用于处理部分类型的SQL查询返回的数据。query_data：表示查询出来的数据。data：表示要处理的数据类型。
        def sql_data_handler(cls, query_data, data):
            """
            处理部分类型sql查询出来的数据格式
            @param query_data: 查询出来的sql数据
            @param data: 数据池
            @return:
            """
            # 遍历查询出来的数据。
            for key, value in query_data.items():
                # 判断查询出来的数据类型是否为decimal.Decimal类型。
                if isinstance(value, decimal.Decimal):
                    # 如果是，则将它转换为浮点型。
                    data[key] = float(value)
                # 判断查询出来的数据类型是否为datetime.datetime类型。
                elif isinstance(value, datetime.datetime):
                    # 如果是，则将它转换为字符串。
                    data[key] = str(value)
                # 否则即是其他数据类型。
                else:
                    # 直接将查询出来的数据放入返回值数据池中。
                    data[key] = value
            # 返回处理后的数据结果。
            return data
        # 总之，这个方法是一个用于处理部分类型SQL查询返回的数据的类方法，用于保证返回值数据格式的正确性。方法内部使用了for循环遍历查询出来的数据，并根据数据类型进行相应的转换或赋值操作，最后将结果放入返回值数据池中。


# 定义了一个名为SetUpMySQL的类，继承自MysqlDB类。
class SetUpMySQL(MysqlDB):
    """ 处理前置sql """

    # 定义了一个名为setup_sql_data的实例方法，它接收一个sql参数，可以是一个字符串列表或空值，并返回一个含有处理后数据的字典对象。
    def setup_sql_data(self, sql: Union[List, None]) -> Dict:
        """
            处理前置请求sql
            :param sql:
            :return:
            """
        # 将sql转换成字符串类型，并移除前面所有的空白字符，并将其作为参数传递给ast.literal_eval函数，用于转换sql成Python语法的对象。
        sql = ast.literal_eval(cache_regular(str(sql)))
        # try语句用于异常处理。
        try:
            # 声明一个空字典，用于存储SQL查询返回结果。
            data = {}
            # 当传入的SQL请求不是空值时执行。
            if sql is not None:
                # 遍历sql列表，将每一组SQL请求语句执行。
                for i in sql:
                    # 如果查询是select类型。
                    if i[0:6].upper() == 'SELECT':
                        # 使用query方法执行SQL查询，并将返回数据的第一项赋值给变量sql_date。
                        sql_date = self.query(sql=i)[0]
                        # 遍历sql_date的键值对。
                        for key, value in sql_date.items():
                            # 将查询到的value值赋给data的key键。
                            data[key] = value
                    # 如果查询不是select类型。
                    else:
                        # 使用execute方法直接执行SQL请求。
                        self.execute(sql=i)
            # 返回处理好的数据结果。
            return data
        # 捕捉到异常时执行的语句，这里是抛出一个DataAcquisitionFailed异常。
        except IndexError as exc:
            # 抛出一个DataAcquisitionFailed异常，提示SQL数据查询失败，请检查是否正确，将捕获到的异常作为其原因。
            raise DataAcquisitionFailed("sql 数据查询失败，请检查setup_sql语句是否正确") from exc


'''
总之，这个SetUpMySQL类继承了MysqlDB类，并覆盖了父类中的setup_sql_data方法，该方法用于处理前置的SQL请求。在该方法内部，先将传入的SQL请求转换成Python语法对象，并进行遍历执行。如果是select类型的查询，在遍历结果的同时将查询到的数据存放在字典对象中并返回。如果是其他类型的请求，则直接调用方法执行，并将返回值赋值给data字典。如果执行失败，则会抛出异常提示查询失败。
'''
# 定义了一个名为AssertExecution的类，继承自MysqlDB类。
class AssertExecution(MysqlDB):
    """ 处理断言sql数据 """

    # 定义了一个名为assert_execution的实例方法，它接收两个参数，一个是sql，一个是resp，并返回一个字典。
    def assert_execution(self, sql: list, resp) -> dict:
        """
         执行 sql, 负责处理 yaml 文件中的断言需要执行多条 sql 的场景，最终会将所有数据以对象形式返回
        :param resp: 接口响应数据
        :param sql: sql
        :return:
        """
        try:
            # 判断传入的sql参数是否为列表类型。
            if isinstance(sql, list):

                # 声明一个空字典，用于存储SQL查询返回结果。
                data = {}
                # 声明变量_sql_type，这里存放SQL执行语句的关键字。
                _sql_type = ['UPDATE', 'update', 'DELETE', 'delete', 'INSERT', 'insert']
                # 如果查询的SQL语句不包含_sql_type中的关键字语句就执行。
                if any(i in sql for i in _sql_type) is False:
                    for i in sql:
                        # 对每个i关键字SQL执行正则匹配操作。并将resp作为参数传递给sql_regular方法。
                        sql = sql_regular(i, resp)
                        # 如果sql不为空。
                        if sql is not None:
                            # 使用query方法执行SQL查询，并将返回结果的第一项赋值给query_data。
                            query_data = self.query(sql)[0]
                            # 使用sql_data_handler方法，处理查询出来的数据，并将其存入data字典。
                            data = self.sql_data_handler(query_data, data)
                        # 如果sql为空，就抛出异常。
                        else:
                            # 抛出DataAcquisitionFailed异常，提示未查询到数据。
                            raise DataAcquisitionFailed(f"该条sql未查询出任何数据, {sql}")
                else:
                    # 如果对sql中_sql_type中的关键字类型中的语句进行断言，即不符合处理条件时抛出异常。
                    raise DataAcquisitionFailed("断言的 sql 必须是查询的 sql")
            # 如果sql不属于列表类型，就抛出异常
            else:
                # 抛出ValueTypeError异常，提示sql数据类型不正确，接收的参数类型为列表类型。
                raise ValueTypeError("sql数据类型不正确，接受的是list")
            # 返回处理好的数据结果。
            return data
        # 捕捉可能出现的任何异常。
        except Exception as error_data:
            # 输出相关异常错误日志信息。
            ERROR.logger.error("数据库连接失败，失败原因 %s", error_data)
            # 抛出捕捉到的异常。
            raise error_data

'''
总之，这个AssertExecution类继承了MysqlDB类，并覆盖了父类中的assert_execution方法，该方法用于处理SQL断言。在该方法内部，首先判断sql是否为列表类型，然后遍历并处理每个SQL语句。如果是查询语句，就使用query方法执行，并使用sql_data_handler方法将处理后的结果存储到data字典中。如果有其他情况，则抛出相关异常信息。

'''
