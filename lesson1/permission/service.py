# coding: utf-8
"""
PermissionService
"""

# from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ..config.common import SQLALCHEMY_DATABASE_URI
from ..models import EmployeeDepartment, DepartmentTree, DepartmentPermission, Permission, Department


class PermissionService(object):

    # FIXME: replace *args **kwargs with paramters
    def get_user_permissions(self, employee_id, resource_id) -> set:
        # raise NotImplementedError()

        print("start function get_user_permissions")
        print("input employee_id:", employee_id, ", resource_id: ", resource_id)

        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        # 通过绑定数据库引擎获取数据库会话类
        db_session = sessionmaker(bind=engine)
        # 获取数据库会话
        session = db_session()

        try:
            # 查找该员工的所属部门ID
            department_id, parent_path = self.get_user_department(employee_id)
            print("department_id: ", department_id, ", parent_path: ", parent_path)

            if department_id is None:
                return set([])

            # 上级部门分开成list的项，同时变为int类型
            all_department = set([])
            if parent_path is not None:
                all_department = set(parent_path.split('-'))
                all_department = set([int(i) for i in all_department])

            all_department.add(department_id)

            print("all_department:", all_department)

            # 非leader，查找department_id及上级部门对resource_id拥有的非leader权限
            results = (session.query(Permission.action).
                       join(DepartmentPermission, DepartmentPermission.permission_id == Permission.id).
                       filter(DepartmentPermission.leader_only.is_(False)).
                       filter(Permission.resource_id == resource_id).
                       filter(DepartmentPermission.department_id.in_(all_department)).all())

            print("results", results)
            ret = set([])
            for row in results:
                ret.add(row[0])
                # print("every action", row[0])

            print(ret)
            return ret

        except SQLAlchemyError as e:
            print("Error: SQL Execute error", e)
            return set([])
        finally:
            session.close()
            print("end function get_user_permissions")

    def get_user_permissions2(self, employee_id, resource_id) -> set:

        print("start function get_user_permissions2")
        print("input employee_id:", employee_id, ", resource_id: ", resource_id)

        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        # 通过绑定数据库引擎获取数据库会话类
        db_session = sessionmaker(bind=engine)
        # 获取数据库会话
        session = db_session()

        try:
            # 查找该员工的所属部门ID
            department_id, parent_path = self.get_user_department(employee_id)
            print("department_id: ", department_id, ", parent_path: ", parent_path)

            if department_id is None:
                return set([])

            # 查找员工权限
            ret = self.get_user_permissions(employee_id, resource_id)

            # 查找该员工是否为leader，及所在department_id
            leader_department = (session.query(Department.id).
                                 filter(Department.leader_id == employee_id).first())

            if leader_department is not None:
                # 查找子department_id对resource_id拥有的权限
                results = (session.query(Permission.action).
                           join(DepartmentPermission, DepartmentPermission.permission_id == Permission.id).
                           join(DepartmentTree, DepartmentTree.id == DepartmentPermission.department_id).
                           filter(DepartmentPermission.leader_only.is_(True)).
                           filter(Permission.resource_id == resource_id).
                           filter(DepartmentTree.parent_path.like(parent_path + '%')).all())

                print("results", results)

                for row in results:
                    ret.add(row[0])
                    # print("every action", row[0])

            print(ret)
            return ret

        except SQLAlchemyError as e:
            print("Error: SQL Execute error", e)
            return set([])
        finally:
            session.close()
            print("start function get_user_permissions2")

    def get_user_department(self, employee_id) -> tuple:
        # 获取用户所在部门(包括上级部门)

        # print("start function get_user_department")
        # print("input employee_id:", employee_id)

        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        # 通过绑定数据库引擎获取数据库会话类
        db_session = sessionmaker(bind=engine)
        # 获取数据库会话
        session = db_session()

        try:
            # 查找该员工的实际部门ID
            department_id = (session.query(EmployeeDepartment.department_id).
                             filter(EmployeeDepartment.employee_id == employee_id).one_or_none())

            # print("department_id:", department_id)

            # 若查不到该员工，返回空集
            if department_id is None:
                return None, None

            department_id = department_id[0]

            # 查找该部门的所有上级部门
            parent_path = (session.query(DepartmentTree.parent_path).
                           filter(DepartmentTree.id == department_id).one_or_none())

            # print("parent_path: ", parent_path)

            if parent_path is not None:
                parent_path = parent_path[0]

            return department_id, parent_path

        except SQLAlchemyError as e:
            print("Error: SQL Execute error", e)
            return None, None
        finally:
            session.close()
            # print("end function get_user_department")
