# coding: utf-8
"""
DepartmentService
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ..models import EmployeeDepartment, DepartmentTree
from ..config.common import SQLALCHEMY_DATABASE_URI


class DepartmentService(object):

    # FIXME: replace *args **kwargs with paramters
    def is_user_in_department(self, employee_id, department_id) -> bool:
        # raise NotImplementedError()

        print("start function is_user_in_department ")
        print("input employee_id:", employee_id, ", department_id:", department_id)

        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        # 通过绑定数据库引擎获取数据库会话类
        db_session = sessionmaker(bind=engine)
        # 获取数据库会话
        session = db_session()

        try:

            # 查找该员工的实际部门ID
            department_id_real = (session.query(EmployeeDepartment.department_id).
                                  filter(EmployeeDepartment.employee_id == employee_id).one_or_none())

            # 若查不到该员工，返回False
            if department_id_real is None:
                return False

            department_id_real = department_id_real[0]
            print("department_id_real: ", department_id_real)

            # 若输入为实际部门，直接返回True
            if department_id_real == department_id:
                return True

            # 查找该部门的所有上级部门
            parent_path = (session.query(DepartmentTree.parent_path).
                           filter(DepartmentTree.id == department_id_real).one_or_none())

            # 若查不到上级部门，返回False
            if parent_path is None:
                return False

            parent_path = parent_path[0]
            print("parent_path: ", parent_path)

            # 上级部门分开成list的项，并添加到list
            parent_department = parent_path.split('-')

            # 判断是否与父级部门匹配
            if str(department_id) in parent_department:
                return True
            else:
                return False

        except SQLAlchemyError as e:
            print("Error: SQL Execute error", e)
            return False
        finally:
            session.close()
            print("end function is_user_in_department")
