from __future__ import annotations

import os
from pathlib import Path
import re
import sys
import getpass
import logging
import argparse
from types import ModuleType
from typing import Dict

from javspn.core.lib import re_escape

__all__ = ['cfg', 'args']

built_in_cfg_file = os.path.join(os.path.dirname(__file__), 'cfg.py')

def log_filter(record):
    """只接受JavSP自身的日志，排除所依赖的库的日志"""
    rname = record.name
    return rname in ('main', '__main__') or rname.startswith(('javspn.core.', 'javspn.web.'))


class ColoredFormatter(logging.Formatter):
    """为不同level的日志着色"""
    NO_STYLE = '\033[0m'
    COLOR_MAP = {
        logging.DEBUG:    '\033[1;30m',  # grey
        logging.WARNING:  '\033[1;33m',  # light yellow
        logging.ERROR:    '\033[1;31m',  # light red
        logging.CRITICAL: '\033[0;31m',  # red
    }

    def __init__(self, fmt='%(levelname)-8s:%(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S', style='%', validate=True) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate)

    def format(self, record):
        # 清除exc_info异常信息，保持终端输出的整洁
        record.exc_info = None
        record.exc_text = None
        raw = super().format(record)
        color = self.COLOR_MAP.get(record.levelno, self.NO_STYLE)
        return color + raw + self.NO_STYLE


class DetailedFormatter(logging.Formatter):
    """如果日志记录包含异常信息，则将传递给异常的参数一起记录下来"""
    def __init__(self, fmt='%(asctime)s %(name)s:%(lineno)d %(levelname)s: %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S', *args) -> None:
        super().__init__(fmt, datefmt, *args)
        username = getpass.getuser()
        self.anonymize = re.compile(r'([\\/]*)' + re_escape(username) + '([\\/]*)', flags=re.I)

    def format(self, record):
        raw = super().format(record)
        s = self.anonymize.sub(r'\1javsp\2', raw)
        return s

    def formatException(self, ei):
        s = super().formatException(ei)
        # ei[1] 是异常的实例，从中提取除了异常的message外的其他参数
        if len(ei[1].args) > 1:
            args = ei[1].args[1:]
            s += "\nArguments: \n  " + str(args).strip('(),')
        return s


# 添加到root的filter无法对root的子logger生效（真是反直觉的设计），因此将filter添加到每一个handler
# https://docs.python.org/3/library/logging.html#filter-objects
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    filename=rel_path_from_exe('JavSP.log'), mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.addFilter(filter=log_filter)
file_handler.setFormatter(DetailedFormatter())
root_logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.addFilter(filter=log_filter)
stream_handler.setFormatter(ColoredFormatter(fmt='%(message)s'))
root_logger.addHandler(stream_handler)

filemove_logger = logging.getLogger('filemove')
file_handler2 = logging.FileHandler(filename=rel_path_from_exe('FileMove.log'),
                                    mode='a', encoding='utf-8')
file_handler2.addFilter(filter=lambda r: r.name == 'filemove')
file_handler2.setFormatter(logging.Formatter(
    fmt='%(asctime)s\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
filemove_logger.addHandler(file_handler2)

logger = logging.getLogger(__name__)

class CfgObj(object):                                 
    def __init__(self) -> None:                       
        self.__backed: Dict[str, CfgObj] = {}         
    def __getattr__(self, name: str, /) -> CfgObj:    
                                                      
        if name == '__backed':                        
            print('lol')                              
            return object.__getattribute__(self, name)
        if name in self.__backed:                     
            return self.__backed[name]                
        else:                                         
            ret = CfgObj()                            
            self.__backed[name] = ret                 
            return ret                                

# class CfgObj(object):
#     def __init__(self) -> None:
#         self.__backed = {}
#     def __getattribute__(self, name: str, /) -> CfgObj:
#         if name == '__backed':
#             object.__getattribute__(self, name)
#         elif name in self.__backed:
#             return self.__backed[name]
#         else:
#             ret = CfgObj()
#             self.__backed[name] = ret
#             return ret

def dict_from_module(module):
    context = {}
    for setting in dir(module):
        # you can write your filter here
        if setting.islower() and setting.isalpha():
            context[setting] = getattr(module, setting)

    return context

#TODO: fix read config
def read_config(cfg_file) -> ModuleType:
    if getattr(sys, 'frozen', False):
        sys.path.append('.')
    else:
        sys.path.append(str(Path(__file__).parent.parent.parent.parent / 'config'))
    return __import__('cfg')

def parse_args():
    """解析从命令行传入的参数并进行有效性验证"""
    parser = argparse.ArgumentParser(prog='JavSP', description='汇总多站点数据的AV元数据刮削器',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', help='使用指定的配置文件')
    parser.add_argument('-i', '--input', help='要扫描的文件夹')
    parser.add_argument('-o', '--output', help='保存整理结果的文件夹')
    parser.add_argument('-x', '--proxy', help='代理服务器地址')
    parser.add_argument('-e', '--auto-exit', action='store_true', help='运行结束后自动退出')
    parser.add_argument('-s', '--shutdown', action='store_true', help='整理完成后关机')
    parser.add_argument('--data-cache-file', help='存储数据的缓存文件，临时文件，供进程间通信使用')
    parser.add_argument('--only-scan', action='store_true', help='仅识别，不刮削')
    parser.add_argument('--only-fetch', action='store_true', help='仅刮削data-cache-file缓存文件中的数据')
    parser.add_argument('--no-update', action='store_true', help='不检查更新')
    # 忽略无法识别的参数，避免传入供pytest使用的参数时报错
    args, unknown = parser.parse_known_args()

    # 验证相关参数的有效性
    if args.config:
        cfg_file = os.path.abspath(args.config)
        if not os.path.exists(cfg_file):
            logger.error(f"找不到指定的配置文件: '{cfg_file}'")
            raise SystemExit()
        else:
            logger.debug(f"读取指定的配置文件: '{cfg_file}'")
    else:
        cfg_file = built_in_cfg_file
    # manual: 未传入选项时值为-1，仅传入选项时值为None，传入选项且有对应值时为对应值
    # 为了方便使用，仅传入选项时的默认值修改为'failed'，未传入选项时修改为None
    # raise argparse.ArgumentError('a', "invalid choice: 'aa' (choose from 1, 23)")
    if args.manual == None:
        args.manual = 'failed'
    elif args.manual == -1:
        args.manual = None
    elif args.manual.lower() in ('all', 'failed'):
        args.manual = args.manual.lower()
    else:
        # 生成与argparser类似格式的异常消息
        msg = f"{parser.prog}: error: argument -m/--manual: invalid choice: '{args.manual}' (choose from 'all', 'failed' or leave it empty)"
        # 使用SystemExit异常以避免显示traceback信息
        raise SystemExit(msg)
    if (args.only_scan == True or args.only_fetch == True) and args.data_cache_file == None:
        raise SystemExit("当仅刮削或者仅识别时，必须传入缓存文件路径")
    args.config = cfg_file
    return args

args = parse_args()
cfg = dict_from_module(read_config(args.config))
cfg.update(parse_args())
