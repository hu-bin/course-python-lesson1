# coding: utf-8
"""

"""
from unittest import TestCase
import logging
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ..department.service import DepartmentService
from ..models import DepartmentClosure, Employee, Department
# from ..config.common import SQLALCHEMY_DATABASE_URI
from ..models import db


class TestDepartment(TestCase):

    def setUp(self):
        self.add_all_employee_info()

    def tearDown(self):
        self.clear_all_employee_info()

    def test_is_user_in_department(self):
        # raise NotImplementedError()
        dpt_srv = DepartmentService()
        # 各级leader与对应部门
        self.assertEqual(dpt_srv.is_user_in_department(1, 1), True)
        self.assertEqual(dpt_srv.is_user_in_department(4, 4), True)
        self.assertEqual(dpt_srv.is_user_in_department(6, 6), True)
        self.assertEqual(dpt_srv.is_user_in_department(10, 10), True)

        # 员工与对应部门
        self.assertEqual(dpt_srv.is_user_in_department(13, 5), True)
        self.assertEqual(dpt_srv.is_user_in_department(17, 4), True)
        self.assertEqual(dpt_srv.is_user_in_department(17, 4), True)
        self.assertEqual(dpt_srv.is_user_in_department(24, 12), True)

        # 越级判断
        self.assertEqual(dpt_srv.is_user_in_department(23, 8), True)
        self.assertEqual(dpt_srv.is_user_in_department(18, 2), True)
        self.assertEqual(dpt_srv.is_user_in_department(22, 1), True)

        # 部门错误
        self.assertEqual(dpt_srv.is_user_in_department(14, 6), False)
        self.assertEqual(dpt_srv.is_user_in_department(3, 5), False)

        # employee不存在
        self.assertEqual(dpt_srv.is_user_in_department(25, 1), False)
        self.assertEqual(dpt_srv.is_user_in_department(0, 1), False)
        self.assertEqual(dpt_srv.is_user_in_department(-1, 1), False)

        # department不存在
        self.assertEqual(dpt_srv.is_user_in_department(1, 0), False)
        self.assertEqual(dpt_srv.is_user_in_department(1, 13), False)
        self.assertEqual(dpt_srv.is_user_in_department(1, -1), False)

    @staticmethod
    def add_employee():
        try:
            # 添加员工数据
            employee_list = list([])
            employee_list.append(Employee(id=1, name='公司总裁', leader_id=1, department_id=1))
            employee_list.append(Employee(id=2, name='研发部经理', leader_id=1, department_id=2))
            employee_list.append(Employee(id=3, name='营销部经理', leader_id=1, department_id=3))
            employee_list.append(Employee(id=4, name='行政部经理', leader_id=1, department_id=4))
            employee_list.append(Employee(id=5, name='市场部部长', leader_id=3, department_id=5))
            employee_list.append(Employee(id=6, name='销售部部长', leader_id=3, department_id=6))
            employee_list.append(Employee(id=7, name='客户端研发部部长', leader_id=2, department_id=7))
            employee_list.append(Employee(id=8, name='服务端研发部部长', leader_id=2, department_id=8))
            employee_list.append(Employee(id=9, name='Android研发部Leader', leader_id=7, department_id=9))
            employee_list.append(Employee(id=10, name='iOS研发部Leader', leader_id=7, department_id=10))
            employee_list.append(Employee(id=11, name='API研发部Leader', leader_id=8, department_id=11))
            employee_list.append(Employee(id=12, name='Infrastructure研发部Leader', leader_id=8, department_id=12))
            employee_list.append(Employee(id=13, name='市场部员工1', leader_id=5, department_id=5))
            employee_list.append(Employee(id=14, name='市场部员工2', leader_id=5, department_id=5))
            employee_list.append(Employee(id=15, name='销售部员工1', leader_id=6, department_id=6))
            employee_list.append(Employee(id=16, name='销售部员工2', leader_id=6, department_id=6))
            employee_list.append(Employee(id=17, name='行政部员工1', leader_id=4, department_id=4))
            employee_list.append(Employee(id=18, name='Android研发部员工1', leader_id=9, department_id=9))
            employee_list.append(Employee(id=19, name='Android研发部员工2', leader_id=9, department_id=9))
            employee_list.append(Employee(id=20, name='Android研发部员工3', leader_id=9, department_id=9))
            employee_list.append(Employee(id=21, name='iOS研发部员工1', leader_id=10, department_id=10))
            employee_list.append(Employee(id=22, name='iOS研发部员工2', leader_id=10, department_id=10))
            employee_list.append(Employee(id=23, name='API研发部员工1', leader_id=11, department_id=11))
            employee_list.append(Employee(id=24, name='Infrastructure研发部员工1', leader_id=12, department_id=12))

            db.session.add_all(employee_list)
            db.session.commit()

            # print("add employee info")

        except SQLAlchemyError as e:
            logging.error("SQL Execute error: %s", e)

    @staticmethod
    def add_department():

        try:
            # 添加部门数据
            department_list = list([])
            department_list.append(Department(id=1, name='公司', leader_id=1))
            department_list.append(Department(id=2, name='研发部', leader_id=2))
            department_list.append(Department(id=3, name='营销部', leader_id=3))
            department_list.append(Department(id=4, name='行政部', leader_id=4))
            department_list.append(Department(id=5, name='市场部', leader_id=5))
            department_list.append(Department(id=6, name='销售部', leader_id=6))
            department_list.append(Department(id=7, name='客户端研发部', leader_id=7))
            department_list.append(Department(id=8, name='服务端研发部', leader_id=8))
            department_list.append(Department(id=9, name='Android研发部', leader_id=9))
            department_list.append(Department(id=10, name='iOS研发部', leader_id=10))
            department_list.append(Department(id=11, name='API研发部', leader_id=11))
            department_list.append(Department(id=12, name='Infrastructure研发部', leader_id=12))

            db.session.add_all(department_list)
            db.session.commit()

            # print("add department info")

        except SQLAlchemyError as e:
            logging.error("SQL Execute error: %s", e)

    @staticmethod
    def add_department_closure():
        try:
            # 添加部门结构数据
            department_closure_list = list([])
            department_closure_list.append(DepartmentClosure(id=1, department_id=1, parent_id=1, depth=0))

            department_closure_list.append(DepartmentClosure(id=2, department_id=2, parent_id=1, depth=1))
            department_closure_list.append(DepartmentClosure(id=3, department_id=2, parent_id=2, depth=0))

            department_closure_list.append(DepartmentClosure(id=4, department_id=3, parent_id=1, depth=1))
            department_closure_list.append(DepartmentClosure(id=5, department_id=3, parent_id=3, depth=0))

            department_closure_list.append(DepartmentClosure(id=6, department_id=4, parent_id=1, depth=1))
            department_closure_list.append(DepartmentClosure(id=7, department_id=4, parent_id=4, depth=0))

            department_closure_list.append(DepartmentClosure(id=8, department_id=5, parent_id=1, depth=2))
            department_closure_list.append(DepartmentClosure(id=9, department_id=5, parent_id=3, depth=1))
            department_closure_list.append(DepartmentClosure(id=10, department_id=5, parent_id=5, depth=0))

            department_closure_list.append(DepartmentClosure(id=11, department_id=6, parent_id=1, depth=2))
            department_closure_list.append(DepartmentClosure(id=12, department_id=6, parent_id=3, depth=1))
            department_closure_list.append(DepartmentClosure(id=13, department_id=6, parent_id=6, depth=0))

            department_closure_list.append(DepartmentClosure(id=14, department_id=7, parent_id=1, depth=2))
            department_closure_list.append(DepartmentClosure(id=15, department_id=7, parent_id=2, depth=1))
            department_closure_list.append(DepartmentClosure(id=16, department_id=7, parent_id=7, depth=0))

            department_closure_list.append(DepartmentClosure(id=17, department_id=8, parent_id=1, depth=2))
            department_closure_list.append(DepartmentClosure(id=18, department_id=8, parent_id=2, depth=1))
            department_closure_list.append(DepartmentClosure(id=19, department_id=8, parent_id=8, depth=0))

            department_closure_list.append(DepartmentClosure(id=20, department_id=9, parent_id=1, depth=3))
            department_closure_list.append(DepartmentClosure(id=21, department_id=9, parent_id=2, depth=2))
            department_closure_list.append(DepartmentClosure(id=22, department_id=9, parent_id=7, depth=1))
            department_closure_list.append(DepartmentClosure(id=23, department_id=9, parent_id=9, depth=0))

            department_closure_list.append(DepartmentClosure(id=24, department_id=10, parent_id=1, depth=3))
            department_closure_list.append(DepartmentClosure(id=25, department_id=10, parent_id=2, depth=2))
            department_closure_list.append(DepartmentClosure(id=26, department_id=10, parent_id=7, depth=1))
            department_closure_list.append(DepartmentClosure(id=27, department_id=10, parent_id=10, depth=0))

            department_closure_list.append(DepartmentClosure(id=28, department_id=11, parent_id=1, depth=3))
            department_closure_list.append(DepartmentClosure(id=29, department_id=11, parent_id=2, depth=2))
            department_closure_list.append(DepartmentClosure(id=30, department_id=11, parent_id=8, depth=1))
            department_closure_list.append(DepartmentClosure(id=31, department_id=11, parent_id=11, depth=0))

            department_closure_list.append(DepartmentClosure(id=32, department_id=12, parent_id=1, depth=3))
            department_closure_list.append(DepartmentClosure(id=33, department_id=12, parent_id=2, depth=2))
            department_closure_list.append(DepartmentClosure(id=34, department_id=12, parent_id=8, depth=1))
            department_closure_list.append(DepartmentClosure(id=35, department_id=12, parent_id=12, depth=0))

            db.session.add_all(department_closure_list)
            db.session.commit()

            # print("add department_tree info")

        except SQLAlchemyError as e:
            logging.error("SQL Execute error: %s", e)

    """
    @staticmethod
    def add_employee_department():
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        # 通过绑定数据库引擎获取数据库会话类
        db_session = sessionmaker(bind=engine)
        # 获取数据库会话
        session = db_session()
        try:
            # 添加员工数据
            employee_department_list = list([])
            employee_department_list.append(EmployeeDepartment(employee_id=1, department_id=1))
            employee_department_list.append(EmployeeDepartment(employee_id=2, department_id=2))
            employee_department_list.append(EmployeeDepartment(employee_id=3, department_id=3))
            employee_department_list.append(EmployeeDepartment(employee_id=4, department_id=4))
            employee_department_list.append(EmployeeDepartment(employee_id=5, department_id=5))
            employee_department_list.append(EmployeeDepartment(employee_id=6, department_id=6))
            employee_department_list.append(EmployeeDepartment(employee_id=7, department_id=7))
            employee_department_list.append(EmployeeDepartment(employee_id=8, department_id=8))
            employee_department_list.append(EmployeeDepartment(employee_id=9, department_id=9))
            employee_department_list.append(EmployeeDepartment(employee_id=10, department_id=10))
            employee_department_list.append(EmployeeDepartment(employee_id=11, department_id=11))
            employee_department_list.append(EmployeeDepartment(employee_id=12, department_id=12))
            employee_department_list.append(EmployeeDepartment(employee_id=13, department_id=5))
            employee_department_list.append(EmployeeDepartment(employee_id=14, department_id=5))
            employee_department_list.append(EmployeeDepartment(employee_id=15, department_id=6))
            employee_department_list.append(EmployeeDepartment(employee_id=16, department_id=6))
            employee_department_list.append(EmployeeDepartment(employee_id=17, department_id=4))
            employee_department_list.append(EmployeeDepartment(employee_id=18, department_id=9))
            employee_department_list.append(EmployeeDepartment(employee_id=19, department_id=9))
            employee_department_list.append(EmployeeDepartment(employee_id=20, department_id=9))
            employee_department_list.append(EmployeeDepartment(employee_id=21, department_id=10))
            employee_department_list.append(EmployeeDepartment(employee_id=22, department_id=10))
            employee_department_list.append(EmployeeDepartment(employee_id=23, department_id=11))
            employee_department_list.append(EmployeeDepartment(employee_id=24, department_id=12))

            session.add_all(employee_department_list)
            session.commit()

            # print("add employee department info")

        except SQLAlchemyError as e:
            print("Error: SQL Execute error", e)

        finally:
            session.close()
    """

    @staticmethod
    def add_all_employee_info():
        TestDepartment.add_employee()
        TestDepartment.add_department()
        TestDepartment.add_department_closure()
        # print("add all employee info")

    @staticmethod
    def clear_all_employee_info():
        try:
            Employee.query.delete()
            Department.query.delete()
            DepartmentClosure.query.delete()
            db.session.commit()
            # print("clear all employee info")

        except SQLAlchemyError as e:
            logging.error("SQL Execute error: %s", e)

