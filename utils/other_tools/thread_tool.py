import time
import threading


class PyTimer:
    """定时器类"""

    # 定义了一个 __init__ 方法作为该类的构造函数，接收一个函数 func 和一些参数和关键字参数 *args、**kwargs。并且初始化了 4 个属性
    def __init__(self, func, *args, **kwargs):
        """构造函数"""

        self.func = func  # 表示需要定时执行的函数
        self.args = args  # 表示传递给需要定时执行的函数的位置参数或参数元组
        self.kwargs = kwargs  # 表示传递给需要定时执行的函数的关键字参数或参数字典
        self.running = False  # 表示定时器是否正在运行的标志，初始化为 False

    # 定义了一个 _run_func 实例方法。
    def _run_func(self):
        """运行定时事件函数"""

        # 使用 threading.Thread 方法创建一个新的线程对象 _thread，并将 self.func 函数作为该线程的目标函数，位置参数和关键字参数分别为 self.args 和 self.kwargs。
        _thread = threading.Thread(target=self.func, args=self.args, kwargs=self.kwargs)
        # 将 _thread 线程设置为守护线程，即子线程在主线程结束时会自动退出。
        _thread.setDaemon(True)
        # 启动 _thread 线程，开始执行定时事件函数。
        _thread.start()

    # 这个方法实现了在一个新线程中运行定时事件函数。使用多线程可以在程序启动后，让程序在后台运行不被阻塞，提高程序的响应能力。

    # 定义了一个名为 _start 的定时器线程函数，包含参数 interval 和 once。interval 是任务执行的时间间隔， once 是一个布尔值，表示任务在定时完成后是否仅执行一次。
    def _start(self, interval, once):
        """启动定时器的线程函数"""

        # 首先使用 max 函数将 interval 设定为 0.01 或更大的值。这是因为当 interval 的值太小可能会导致执行过程中的误差。
        interval = max(interval, 0.01)

        # 根据 interval 的大小， _dt 的值被设定为最小的执行时间。如果 interval 小于 0.05 秒，则 _dt 值为1/10倍的 interval。
        if interval < 0.050:
            _dt = interval / 10
        # 否则， _dt 值为0.005秒。
        else:
            _dt = 0.005

        # 如果任务只要单次执行，该代码块会先计算到达期限时间 deadline，等待直到时间到达 deadline（通过不断的 time.sleep(dt)），然后执行 self._run_func() 方法，以执行任务。
        if once:
            deadline = time.time() + interval
            while time.time() < deadline:
                time.sleep(_dt)

            # 定时时间到，调用定时事件函数
            self._run_func()
        # 如果任务需要重复执行，该代码块会设置 self.running = True，然后在一个循环中重复执行任务。在循环中，该代码块先计算下一个到期时间 deadline，然后等待时间直到到期（通过不断的time.sleep(dt)）。然后，为下一个定时执行更新 deadline 的值。最后，该代码块调用 _run_func() 方法来执行任务。
        else:
            # 当 self.running 被设置为 False 时，定时器将再次暂停，任务将不会被重复执行。
            self.running = True
            deadline = time.time() + interval
            while self.running:
                while time.time() < deadline:
                    time.sleep(_dt)

                # 更新下一次定时时间
                deadline += interval

                # 定时时间到，调用定时事件函数
                if self.running:
                    self._run_func()

    # 这是启动定时器的外部函数，在类中设定了 interval、once 其默认值为 False。
    def start(self, interval, once=False):
        """启动定时器
        interval    - 定时间隔，浮点型，以秒为单位，最高精度10毫秒
        once        - 是否仅启动一次，默认是连续的
        """

        # thread_ 是定义的一个线程对象，这里使用 threading.Thread 函数从 _start 中创建一个新线程。
        thread_ = threading.Thread(target=self._start, args=(interval, once))
        # 将线程设置为守护线程。在 Python 中，当一个线程为守护线程时，在主线程退出时，守护线程会自动退出。这可以确保定时器线程在主线程结束时自动结束。
        thread_.setDaemon(True)
        # 启动新线程，让定时器开始工作。线程开始执行 _start 方法，在该方法中，根据设定好的 interval 和 once参数，对定时器的执行进行相应设定和控制。
        thread_.start()

    def stop(self):
        """停止定时器"""

        # 是 running 属性的赋值操作，将类属性 self.running 设为 False，用于控制定时器的运行。
        self.running = False
    # 这个方法非常简单，它的作用就是让定时器主线程停止运行，因为在定时器的主线程中，使用了 while self.running: 循环，当 self.running 为 False 时，循环就会退出，从而实现停止定时器的目的。


# 定义了一个函数 do_something，函数接收两个参数，其中 name 是必须传递的参数，而 gender 是可选参数，如果不传递则默认为 'male'。
def do_something(name, gender='male'):
    """执行"""
    # 使用 time.time() 函数获取当前时间戳，并输出一个提示信息，表示在定时任务到达时，需要执行特定的任务。
    print(time.time(), '定时时间到，执行特定任务')
    # 使用字符串的 format 方法对字符串进行格式化输出，输出传入的 name 和 gender，其中 %s 是占位符。
    print('name:%s, gender:%s', name, gender)
    # 使用 time 模块的 sleep 函数使得程序暂停 5 秒，用于模拟执行一些需要耗费时间的操作。
    time.sleep(5)
    # 输出当前时间戳和一个提示信息，表示特定任务已经完成。
    print(time.time(), '完成特定任务')


# 定义了一个 PyTimer 对象，并传入了三个参数，分别是 do_something 函数、字符串 'Alice' 和字典 {'gender': 'female'}，其中 'Alice' 和 'female' 分别对应了 do_something 中的 name 和 gender 两个参数。
timer = PyTimer(do_something, 'Alice', gender='female')
# 调用了定时器对象 timer 的 start() 方法，开始了定时器操作。其中，第一个参数 0.5 表示每隔 0.5 秒执行一次任务，第二个参数 once=False 表示定时器会一直执行，而不是只执行一次。
timer.start(0.5, once=False)

# 使用 input 函数实现的阻塞操作，等待用户按下回车键，以便之后停止定时器操作。
input('按回车键结束\n')  # 此处阻塞住进程
# 调用了定时器对象 timer 的 stop() 方法，停止了定时器的操作。
timer.stop()