# !/usr/bin/python3
# coding=utf-8
import logging.config
import yaml
import os

# log日志生成位置
# if getattr(sys, 'frozen', False):
#     path = os.path.dirname(os.path.realpath(sys.argv[0]))
# else:
#     path = os.path.dirname(os.path.realpath(__file__)).replace("log", "")

logging_config_file = os.path.dirname(os.path.realpath(__file__)).replace("log", "") + '/config/logging_config.yaml'
# 设置日志打印配置
with open(file=logging_config_file, encoding='utf-8') as f:
    config = yaml.safe_load(f.read())
    # 固定日志文件生成位置
    # config['handlers']['file']['filename'] = path + '/' + config['handlers']['file']['filename']
    logging.config.dictConfig(config)

log = logging.getLogger(__name__)
