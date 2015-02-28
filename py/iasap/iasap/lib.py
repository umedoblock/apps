import sys, os
import datetime

import logging as _logger

global logger
logger = _logger

CHARACTORS_PRINTED_PER_LINE = 79
CPPL = CHARACTORS_PRINTED_PER_LINE

def start_logger(script_name, log_dir=os.path.curdir, log_level=logger.INFO):
    # 通常使用時は、log_dir=os.path.curdir を想定している。
    # log_dir が空文字であれば、log の出力先を sys.stderr に変更する。

    basename = os.path.basename(script_name)
    if log_dir:
        log_base = ".".join((basename, "log"))
        log_path = os.path.join(log_dir, log_base)

        # http://docs.python.jp/3.4/library/logging.html#logging.basicConfig
        # stream: 指定されたストリームを StreamHandler の初期化に使います。
        # この引数は 'filename' と同時には使えないことに注意してください。
        # 両方が指定されたときには ValueError が送出されます。
        # logger.basicConfig(filename='/dev/null', level=logger.INFO)
        # logger.basicConfig(stream=sys.stderr, level=logger.DEBUG)
        logger.basicConfig(filename=log_path, level=log_level)
    else:
        logger.basicConfig(stream=sys.stderr, level=log_level)

    log_prefix = "INFO:root:"
    horizontal = "=" * (CPPL - len(log_prefix))
    _now = datetime.datetime.now()
    body = "{} start! at {} ".format(basename, _now)
    tail = "=" * (CPPL - (len(log_prefix) + len(body)))

    logger.info(horizontal)
    logger.info(body + tail)
    logger.info(horizontal)


