# coding: utf-8
"""
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, BOOLEAN

from .flask import app

db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False)
    leader_id = db.Column(BIGINT, nullable=False)


class Department(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False)
    leader_id = db.Column(BIGINT, nullable=False)


class Resource(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False)


class Permission(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    resource_id = db.Column(BIGINT, nullable=False)
    action = db.Column(VARCHAR(64), nullable=False)


class DepartmentTree(db.Model):
    """部门层级结构，parent_path保存所有父级部门，以 - 分隔"""
    __name__ = 'department_tree'
    # mysql_character_set = 'utf8mb4' -- 使用该语句可以建立字符集为utf8mb4的表
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    parent_path = db.Column(VARCHAR(128), nullable=False)


class EmployeeDepartment(db.Model):
    """员工所属直接部门"""
    __name__ = 'employee_department'
    # mysql_character_set = 'utf8mb4'
    employee_id = db.Column(BIGINT(unsigned=True), primary_key=True)
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)


class DepartmentPermission(db.Model):
    """部门具有的权限"""
    __name__ = 'department_permission'
    # mysql_character_set = 'utf8mb4'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    permission_id = db.Column(BIGINT(unsigned=True), nullable=False)
    leader_only = db.Column(BOOLEAN, nullable=False, default=False)
    # leader_only列在第三题中有效

