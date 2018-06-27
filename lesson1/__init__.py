# coding: utf-8
"""

@create: 2017/1/18
"""
import logging

logging.basicConfig(filename='my.log',
                    level=logging.DEBUG,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S')
