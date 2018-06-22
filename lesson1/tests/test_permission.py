# coding: utf-8
"""

"""
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ..permission.service import PermissionService
from .test_department import TestDepartment
from ..models import Permission, Resource, DepartmentPermission
from ..config.common import SQLALCHEMY_DATABASE_URI


class TestPermission(TestCase):

    def setUp(self):
        self.add_all_permission_info()

    def tearDown(self):
        self.clear_all_permission_info()

    def test_get_user_department(self):
        dpt_srv = PermissionService()
        self.assertEqual(dpt_srv.get_user_department(1), (1, '1'))
        self.assertEqual(dpt_srv.get_user_department(4), (4, '1'))
        self.assertEqual(dpt_srv.get_user_department(6), (6, '1-3'))
        self.assertEqual(dpt_srv.get_user_department(9), (9, '1-2-7'))
        self.assertEqual(dpt_srv.get_user_department(13), (5, '1-3'))
        self.assertEqual(dpt_srv.get_user_department(17), (4, '1'))
        self.assertEqual(dpt_srv.get_user_department(18), (9, '1-2-7'))
        self.assertEqual(dpt_srv.get_user_department(23), (11, '1-2-8'))
        self.assertEqual(dpt_srv.get_user_department(0), (None, None))
        self.assertEqual(dpt_srv.get_user_department(-1), (None, None))
        self.assertEqual(dpt_srv.get_user_department(25), (None, None))

    def test_get_user_permissions(self):
        # raise NotImplementedError()
        dpt_srv = PermissionService()
        # 部门权限向下扩散
        self.assertEqual(dpt_srv.get_user_permissions(1, 1), {'查看', '修改'})
        self.assertEqual(dpt_srv.get_user_permissions(13, 1), {'查看', '修改'})
        self.assertEqual(dpt_srv.get_user_permissions(2, 2), set())
        self.assertEqual(dpt_srv.get_user_permissions(10, 2), {'查看'})
        self.assertEqual(dpt_srv.get_user_permissions(1, 3), set())
        self.assertEqual(dpt_srv.get_user_permissions(18, 3), {'查看'})
        self.assertEqual(dpt_srv.get_user_permissions(18, 4), {'查看'})
        self.assertEqual(dpt_srv.get_user_permissions(16, 4), set())
        self.assertEqual(dpt_srv.get_user_permissions(2, 4), {'查看'})
        # 输入有误
        self.assertEqual(dpt_srv.get_user_permissions(0, 4), set())
        self.assertEqual(dpt_srv.get_user_permissions(1, 10), set())

    def test_get_user_permissions2(self):
        # raise NotImplementedError()
        dpt_srv = PermissionService()
        # leader权限向上扩散
        self.assertEqual(dpt_srv.get_user_permissions2(1, 3), {'修改'})
        self.assertEqual(dpt_srv.get_user_permissions2(2, 2), {'修改'})
        self.assertEqual(dpt_srv.get_user_permissions2(2, 3), {'修改'})
        self.assertEqual(dpt_srv.get_user_permissions2(2, 4), {'查看', '修改'})
        self.assertEqual(dpt_srv.get_user_permissions2(7, 2), {'修改'})
        self.assertEqual(dpt_srv.get_user_permissions2(7, 4), {'查看'})
        self.assertEqual(dpt_srv.get_user_permissions2(10, 2), {'查看', '修改'})
        self.assertEqual(dpt_srv.get_user_permissions2(10, 3), {'查看'})
        self.assertEqual(dpt_srv.get_user_permissions2(21, 3), {'查看'})
        self.assertEqual(dpt_srv.get_user_permissions2(13, 3), set())
        # 输入有误
        self.assertEqual(dpt_srv.get_user_permissions(0, 4), set())
        self.assertEqual(dpt_srv.get_user_permissions(1, 10), set())

    @staticmethod
    def add_resource():
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        # 通过绑定数据库引擎获取数据库会话类
        db_session = sessionmaker(bind=engine)
        # 获取数据库会话
        session = db_session()
        try:
            # 添加员工数据
            resource_list = list([])
            resource_list.append(Resource(id=1, name='个人资源'))
            resource_list.append(Resource(id=2, name='iOS研发部资源'))
            resource_list.append(Resource(id=3, name='客户端研发部资源'))
            resource_list.append(Resource(id=4, name='研发部资源'))

            session.add_all(resource_list)
            session.commit()

            # print("add resource info")

        except SQLAlchemyError as e:
            print("Error: SQL Execute error", e)

        finally:
            session.close()

    @staticmethod
    def add_permission():
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        # 通过绑定数据库引擎获取数据库会话类
        db_session = sessionmaker(bind=engine)
        # 获取数据库会话
        session = db_session()
        try:
            # 添加员工数据
            permission_list = list([])
            permission_list.append(Permission(id=1, resource_id=1, action='增加'))
            permission_list.append(Permission(id=2, resource_id=1, action='修改'))
            permission_list.append(Permission(id=3, resource_id=1, action='删除'))
            permission_list.append(Permission(id=4, resource_id=1, action='查看'))
            permission_list.append(Permission(id=5, resource_id=2, action='增加'))
            permission_list.append(Permission(id=6, resource_id=2, action='修改'))
            permission_list.append(Permission(id=7, resource_id=2, action='删除'))
            permission_list.append(Permission(id=8, resource_id=2, action='查看'))
            permission_list.append(Permission(id=9, resource_id=3, action='增加'))
            permission_list.append(Permission(id=10, resource_id=3, action='修改'))
            permission_list.append(Permission(id=11, resource_id=3, action='删除'))
            permission_list.append(Permission(id=12, resource_id=3, action='查看'))
            permission_list.append(Permission(id=13, resource_id=4, action='增加'))
            permission_list.append(Permission(id=14, resource_id=4, action='修改'))
            permission_list.append(Permission(id=15, resource_id=4, action='删除'))
            permission_list.append(Permission(id=16, resource_id=4, action='查看'))

            session.add_all(permission_list)
            session.commit()

            # print("add permission info")

        except SQLAlchemyError as e:
            print("Error: SQL Execute error", e)

        finally:
            session.close()

    @staticmethod
    def add_department_permission():
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        # 通过绑定数据库引擎获取数据库会话类
        db_session = sessionmaker(bind=engine)
        # 获取数据库会话
        session = db_session()
        try:
            # 添加员工数据
            department_permission_list = list([])
            department_permission_list.\
                append(DepartmentPermission(id=1, department_id=1, permission_id=4, leader_only=False))
            department_permission_list.\
                append(DepartmentPermission(id=2, department_id=1, permission_id=2, leader_only=False))
            department_permission_list.\
                append(DepartmentPermission(id=3, department_id=2, permission_id=16, leader_only=False))
            department_permission_list.\
                append(DepartmentPermission(id=4, department_id=7, permission_id=12, leader_only=False))
            department_permission_list.\
                append(DepartmentPermission(id=5, department_id=10, permission_id=8, leader_only=False))
            department_permission_list.\
                append(DepartmentPermission(id=6, department_id=10, permission_id=6, leader_only=True))
            department_permission_list.\
                append(DepartmentPermission(id=7, department_id=7, permission_id=10, leader_only=True))
            department_permission_list.\
                append(DepartmentPermission(id=8, department_id=2, permission_id=14, leader_only=True))

            session.add_all(department_permission_list)
            session.commit()

            # print("add department permission info")

        except SQLAlchemyError as e:
            print("Error: SQL Execute error", e)

        finally:
            session.close()

    @staticmethod
    def add_all_permission_info():
        TestDepartment.add_all_employee_info()
        TestPermission.add_resource()
        TestPermission.add_permission()
        TestPermission.add_department_permission()
        # print("add all permission info")

    @staticmethod
    def clear_all_permission_info():
        TestDepartment.clear_all_employee_info()

        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        # 通过绑定数据库引擎获取数据库会话类
        db_session = sessionmaker(bind=engine)
        # 获取数据库会话
        session = db_session()
        try:
            session.query(Resource).delete()
            session.query(Permission).delete()
            session.query(DepartmentPermission).delete()

            session.commit()
            # print("clear all permission info")

        except SQLAlchemyError as e:
            print("Error: SQL Execute error", e)

        finally:
            session.close()
