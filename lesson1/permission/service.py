# coding: utf-8
"""
PermissionService
"""

import logging
from sqlalchemy.exc import SQLAlchemyError
from ..models import Employee, DepartmentPermission, Permission, Department, LeaderPermission
from ..common.redis_helper import get_parent_department, get_child_department


class PermissionService(object):

    # FIXME: replace *args **kwargs with paramters
    def get_user_permissions(self, employee_id, resource_id) -> set:
        # raise NotImplementedError()

        logging.info("start function get_user_permissions")
        logging.debug('input employee_id: {} resource_id: {} '.format(employee_id, resource_id))

        try:
            # 查找该员工的实际部门ID
            employee_info = Employee.query.get(employee_id)

            if not employee_info:
                return set()

            logging.debug("department_id: %d", employee_info.department_id)

            # 获取所有上级部门
            all_department = get_parent_department(employee_info.department_id)

            logging.debug("all parent department: %s", repr(all_department))

            # 非leader，查找department_id及上级部门对resource_id拥有的非leader权限
            results = (Permission.query.
                       join(DepartmentPermission, DepartmentPermission.permission_id == Permission.id).
                       filter(Permission.resource_id == resource_id).
                       filter(DepartmentPermission.department_id.in_(all_department)).all())

            logging.debug("permission results: %s", repr(results))

            if not results:
                return set()

            ret = set()
            for row in results:
                ret.add(row.action)

            logging.debug("action results: %s", repr(ret))
            return ret

        except SQLAlchemyError as e:
            logging.error("Error: SQL Execute error: %s", e)
            return set()
        finally:
            logging.info("end function get_user_permissions")

    def get_user_permissions2(self, employee_id, resource_id) -> set:

        logging.info("start function get_user_permissions2")
        logging.debug("input employee_id: {}, resource_id: {}".format(employee_id, resource_id))

        try:
            # 查找该员工的所属部门ID
            employee_info = Employee.query.get(employee_id)

            if not employee_info:
                return set()

            # 查找员工权限
            ret = self.get_user_permissions(employee_id, resource_id)

            # 查找该员工是否为leader，及所在department_id
            leader_department = (Department.query.
                                 filter(Department.leader_id == employee_id).first())

            if leader_department:
                logging.debug("input employee_id: {} is a leader ".format(employee_id))

                # 获取所有下级部门
                all_department = get_child_department(employee_info.department_id)

                logging.debug("all child department: %s", repr(all_department))

                # 查找子department_id对resource_id拥有的权限
                results = (Permission.query.
                           join(LeaderPermission, LeaderPermission.permission_id == Permission.id).
                           filter(Permission.resource_id == resource_id).
                           filter(LeaderPermission.department_id.in_(all_department)).all())

                logging.debug("permission results: %s", repr(results))

                if results:
                    for row in results:
                        ret.add(row.action)

            logging.debug("action results: %s", repr(ret))
            return ret

        except SQLAlchemyError as e:
            logging.error("Error: SQL Execute error %s", e)
            return set()
        finally:
            logging.info("start function get_user_permissions2")
