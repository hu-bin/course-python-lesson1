# coding: utf-8

import logging
import redis
from ..models import DepartmentClosure
from ..config.common import REDIS_URL


def get_parent_department(department_id) -> set:
    """根据部门ID获取其父级部门结构"""

    # 尝试从redis读取
    # r = redis.StrictRedis(host='172.18.0.2', port=6379, db=0)  # , decode_responses=True
    r = redis.StrictRedis.from_url(REDIS_URL)
    key_name = '{}p'.format(department_id)
    parent_department = r.smembers(key_name)

    logging.debug("key name: %s", key_name)
    logging.debug("get_parent_department.get from redis %s", repr(parent_department))

    # 如果取不到从数据库读取
    if not parent_department:

        parent_department = DepartmentClosure.get_parent_department(department_id)

        logging.debug("get_parent_department.get from db %s", repr(parent_department))

        # 添加到redis中
        if parent_department is not None:
            for i in parent_department:
                r.sadd(key_name, i)
    else:
        # parent_department = [int.from_bytes(e) for e in parent_department]
        parent_department = set([int(e.decode('utf8')) for e in parent_department])

    return parent_department


def get_child_department(department_id) -> set:
    """根据部门ID获取其子级部门结构"""

    # 尝试从redis读取
    # r = redis.StrictRedis(host='172.18.0.2', port=6379, db=0)  # , decode_responses=True
    r = redis.StrictRedis.from_url(REDIS_URL)
    key_name = '{}c'.format(department_id)
    child_department = r.smembers(key_name)

    logging.debug("key name: %s", key_name)
    logging.debug("get_child_department.get from redis %s", repr(child_department))

    # 如果取不到从数据库读取
    if not child_department:

        child_department = DepartmentClosure.get_child_department(department_id)

        logging.debug("get_child_department.get from db %s", repr(child_department))

        # 添加到redis中
        if child_department is not None:
            for i in child_department:
                r.sadd(key_name, i)
    else:
        child_department = set([int(e.decode('utf8')) for e in child_department])

    return child_department
