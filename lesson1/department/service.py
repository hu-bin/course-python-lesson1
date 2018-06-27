# coding: utf-8
"""
DepartmentService
"""
import logging
from sqlalchemy.exc import SQLAlchemyError
from ..models import Employee
from ..common.redis_helper import get_parent_department


class DepartmentService(object):

    # FIXME: replace *args **kwargs with paramters
    def is_user_in_department(self, employee_id, department_id) -> bool:
        # raise NotImplementedError()

        logging.info("start function is_user_in_department ")
        logging.debug("input employee_id: {}, department_id: {}".format(employee_id, department_id))

        try:
            # 查找该员工的实际部门ID
            employee_info = Employee.query.get(employee_id)

            # 若查不到该员工，返回False
            if not employee_info:
                return False

            department_id_real = employee_info.department_id
            logging.debug("department_id_real: %d", department_id_real)

            # 若输入为实际部门，直接返回True
            if department_id_real == department_id:
                return True

            # 查找该部门的所有上级部门
            parent_department = get_parent_department(department_id_real)

            # 若查不到上级部门，返回False
            if not parent_department:
                return False

            logging.debug("parent_department: %s", repr(parent_department))

            # 判断是否与父级部门匹配
            if department_id in parent_department:
                return True
            else:
                return False

        except SQLAlchemyError as e:
            logging.error("SQL Execute error: %s", e)
            return False
        finally:
            logging.info("end function is_user_in_department")


