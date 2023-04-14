from os import rename, listdir
from os.path import split, splitext, basename, exists, join, abspath
# 格式化器Formatter, 过滤器Filter, 处理器Handler,记录器Loggers
from logging import Formatter, Filter, FileHandler, StreamHandler
# 文件大小，文件时间，分开存储文件
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from logging import getLogger as logging_getLogger
from multiprocessing import Queue
from threading import Thread
from traceback import format_exc

# 创建日志文件输出目录
from utils import prepare_file_folder

"""
format日志格式
%(levelno)s: 打印日志级别的数值
%(levelname)s: 打印日志级别名称
%(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s: 打印当前执行程序名
%(funcName)s: 打印日志的当前函数
%(module)s 调用日志输出函数的模块名
%(name)s : 所使用的日志名称，默认是'root'，因为默认使用的是 rootLogger
%(msecs)d 日志事件发生事件的毫秒部分
%(lineno)d: 打印日志的当前行号
%(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
%(relativeCreated)d 日志事件发生的时间相对于logging模块加载时间的相对毫秒数（目前还不知道干嘛用的）
%(thread)d: 打印线程ID
%(threadName)s: 打印线程名称
%(process)d: 打印进程ID
%(message)s: 打印日志信息

"""

# 自定义日志输出格式【控制台】
CONSOLE_BASIC_FORMAT = '[%(asctime)s.%(alignmsecs)s %(alignlevelname)s] %(message)s'
CONSOLE_DATE_FORMAT = '%H:%M:%S'
CONSOLE_FORMAT = Formatter(CONSOLE_BASIC_FORMAT, CONSOLE_DATE_FORMAT)


# 自定义日志输出格式【文件】
# correct_module
#FILE_BASIC_FORMAT = "%(asctime)s.%(alignmsecs)s [%(alignlevelname)s %(module)s-%(lineno)d %(funcName)s] %(message)s"
FILE_BASIC_FORMAT = "%(asctime)s.%(alignmsecs)s [%(alignlevelname)s %(module)s] %(message)s"
FILE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
FILE_FORMAT = Formatter(FILE_BASIC_FORMAT, FILE_DATE_FORMAT)


"""
级别        级别数值        使用时机
'DEBUG'     10              详细信息
'INFO '     20              运行产生的信息
'WARN '     30              警告,可能出错(默认设置)
'ERROR'     40              程序不能执行部分功能
'CRITI'     50              程序不能运行
"""
# 自定义日志输出等级
ALIGN_LEVEL_NAME = {'D': 'DEBUG',
                    'I': 'INFO ',
                    'W': 'WARN ',
                    'E': 'ERROR',
                    'C': 'CRITI'
                   }

class Filter(Filter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def filter(self, record):
        record.alignlevelname = ALIGN_LEVEL_NAME[record.levelname[0]]
        record.alignmsecs = '{:<3}'.format(int(record.msecs))
        return True


def getLogger(name = None, file = None, level = 'DEBUG', file_level = 'DEBUG', console_level = 'INFO', multiprocess = False):
    if multiprocess:
        from multiprocessing import get_logger
        logger = get_logger()
        logger.setLevel(level)
    else:
        logger = logging_getLogger(name)
        logger.propagate = False
        logger.setLevel(level)

    if file is not None:
        if not isinstance(file, (list, tuple)):
            file = [file]
        if not isinstance(file_level, (list, tuple)):
            file_level = [file_level]
        for file_, file_level_ in zip(file, file_level):
            prepare_file_folder(file_)
            fhlr = FileHandler(file_)
            fhlr.setFormatter(FILE_FORMAT)
            fhlr.setLevel(file_level_)
            fhlr.addFilter(Filter())
            logger.addHandler(fhlr)
            
    for h in logger.handlers:
        if isinstance(h, StreamHandler):
            return logger

    chlr = StreamHandler()
    chlr.setFormatter(CONSOLE_FORMAT)
    chlr.setLevel(console_level)
    chlr.addFilter(Filter())
    logger.addHandler(chlr)

    return logger


class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, *args, **kwds):
        baseName = split(filename)[1]
        assert baseName.count('.') <= 1
        ext = splitext(baseName)[1]
        suffix = filename[:len(filename)-len(ext)]
        self.real_filename = abspath(filename)  # super().__init__ 里面用到_open，用到self.real_filename
        super().__init__(suffix, *args, **kwds)
        self.len_ext = len(ext)
        self.file_s = f'%s{ext}'
        self.real_filename = self.file_s % self.baseFilename  # 重设


    def rotation_filename(self, default_name):
        return self.file_s % default_name

    def getFilesToDelete(self):
        dirName, baseName = split(self.baseFilename)
        fileNames = listdir(dirName)
        result = []
        prefix = splitext(baseName)[0] + "."
        plen = len(prefix)
        for fileName in fileNames:
            _fileName = fileName[:len(fileName)-self.len_ext]
            if _fileName[:plen] == prefix:
                suffix = _fileName[plen:]
                if self.extMatch.match(suffix):
                    result.append(join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        return result

    def rotate(self, source, dest):
        if exists(self.file_s % source):
            rename(self.file_s % source, dest)

    def _open(self):
        return open(self.real_filename, self.mode, encoding=self.encoding,
                    errors=self.errors)



class MultiprocessingLogger():
    def __init__(self, name, filename,
                 q_size = 1000,
                 backupCount = 30,
                 level = 'INFO',
                 error_filename = None,
                 maxBytes = 512*1024*1024,
                 error_backupCount = 7,
                 console_level = None):
        self.log_queue = Queue(q_size)
        self.logger = logging_getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        prepare_file_folder(filename)
        #fhlr = MyTimedRotatingFileHandler(filename, when='S', interval = 5, backupCount = backupCount)
        fhlr = MyTimedRotatingFileHandler(filename, when='midnight', backupCount = backupCount)
        fhlr.setFormatter(FILE_FORMAT)
        #fhlr.setLevel(level)
        fhlr.addFilter(Filter())
        self.logger.addHandler(fhlr)

        if error_filename is not None:
            prepare_file_folder(error_filename)
            fhlr = RotatingFileHandler(error_filename, maxBytes=maxBytes, backupCount=error_backupCount)
            fhlr.setFormatter(FILE_FORMAT)
            fhlr.setLevel('ERROR')
            fhlr.addFilter(Filter())
            self.logger.addHandler(fhlr)

        if console_level is not None:
            chlr = StreamHandler()
            chlr.setFormatter(CONSOLE_FORMAT)
            chlr.setLevel(console_level)
            chlr.addFilter(Filter())
            self.logger.addHandler(chlr)

        self.funcs = [
            self.logger.debug,
            self.logger.info, 
            self.logger.warning, 
            self.logger.error, 
            self.logger.critical
        ]

        self._client_logger = None

        self.thread = None
        self.start()

    @property
    def client_logger(self):
        if self._client_logger is None:
            self._client_logger = self.create_client()
        return self._client_logger

    def run(self):
        while True:
            level, msg = self.log_queue.get()
            self.funcs[level](msg)

    def start(self):
        if self.thread is None:
            self.thread = Thread(target=self.run, daemon=True)
            self.thread.start()

    def join(self):
        self.thread.join()
        self.thread = None


    def create_client(self):
        client = ClientLogger(self.log_queue)
        return client



class ClientLogger():
    def __init__(self, log_queue):
        self.log_queue = log_queue

    def debug(self, msg):
        self.log_queue.put((0, msg))

    def info(self, msg):
        self.log_queue.put((1, msg))

    def warning(self, msg):
        self.log_queue.put((2, msg))

    def error(self, msg):
        self.log_queue.put((3, msg))

    def critical(self, msg):
        self.log_queue.put((4, msg))

    def exception(self, msg):
        self.log_queue.put((3, f'{msg}\n{format_exc()}'))





    