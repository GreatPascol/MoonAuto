# -*- coding: utf-8 -*-
import logging
import os
import time
from logging.handlers import RotatingFileHandler

default_date_fmt = '%Y-%m-%d %H:%M:%S'
default_msg_fmt = '%(asctime)s [%(levelname)s - %(name)s] %(filename)s-%(lineno)d:  %(message)s'

default_formatter = logging.Formatter(default_msg_fmt, default_date_fmt)
no_prefix_formatter = logging.Formatter('%(message)s')  # 不带时间级别文件等前缀信息的Formatter


def init_basic(level=logging.INFO, format_str=default_msg_fmt, datefmt=default_date_fmt):
    """
    python的logging需要handler来处理日志如何输出，默认是没有handler的；
    logging模块提供一个便利方法basicConfig()来为root logger配置handler

    此方法进一步便利，可以不传参数为root配置输出到控制台的handler
    :param level:
    :param format_str:
    :param datefmt:
    :return:
    """
    logging.basicConfig(level=level, format=format_str, datefmt=datefmt)


def disable_logger_propagate(logger_name):
    """
    设置logger信息不向上传递给祖先logger，通常用来设置信息只输出到单独logger的日志文件
    :param logger_name: logger名
    :return:
    """
    logger = logging.getLogger(logger_name)
    logger.propagate = False


def new_formatter(format_str, datefmt=default_date_fmt):
    """
    实例化Formatter, 参数参见logging.Formatter()文档
    需要自定义信息格式时，用来传递给add_rotating_handler()或add_file_current_date_handler()
    :param format_str:
    :param datefmt:
    :return:
    """
    return logging.Formatter(format_str, datefmt)


def add_rotating_handler(logger_name, log_path, filename='debug.log', max_mb=5, backup=2, level=logging.DEBUG, formatter=default_formatter):
    """
    给logger添加设置输出到日志文件，文件为滚动文件，
    即文件大小超过max_mb时，末尾每添加一个字符，开头相应会删除一个字符
    :param logger_name: logger名
    :param log_path: 日志文件所在的目录
    :param filename: 文件的文件名，默认'debug.log'
    :param max_mb: 文件最大容量
    :param backup: 备份数
    :param level:
    :param formatter:
    :return:
    """
    logger = logging.getLogger(logger_name)
    os.makedirs(log_path, exist_ok=True)
    rotating_handler = RotatingFileHandler(log_path + "/" + filename, encoding="utf-8",
                                           maxBytes=max_mb * 1024 * 1024, backupCount=backup)
    rotating_handler.setLevel(level)
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)


def add_file_current_date_handler(logger_name, log_path, filename_prefix="unnamed", level=logging.DEBUG, formatter=default_formatter):
    """
    给logger添加设置输出到日志文件，文件没有大小限制，文件名自动带日期时间后缀。
    :param logger_name: logger名
    :param log_path: 日志文件所在的目录
    :param filename_prefix: 文件前缀名
    :param level:
    :param formatter:
    :return:
    """
    logger = logging.getLogger(logger_name)
    os.makedirs(log_path, exist_ok=True)
    log_filename = '%s%s.log' % (filename_prefix, time.strftime("%Y-%m-%d-%H-%M", time.localtime(time.time())))
    log_path = "%s/%s" % (log_path, log_filename)
    file_handler = logging.FileHandler(filename=log_path, mode="w", encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
