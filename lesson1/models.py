# coding: utf-8
"""
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy import Index

from .flask import app

db = SQLAlchemy(app)


class CommonTableArgs(object):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False)
    leader_id = db.Column(BIGINT, nullable=False)
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)

    __table_args__ = (
        CommonTableArgs.__table_args__,
    )


class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False)
    leader_id = db.Column(BIGINT, nullable=False)

    __table_args__ = (
        CommonTableArgs.__table_args__,
    )


class Resource(db.Model):
    __tablename__ = 'resource'

    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False)

    __table_args__ = (
        CommonTableArgs.__table_args__,
    )


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    resource_id = db.Column(BIGINT, nullable=False)
    action = db.Column(VARCHAR(64), nullable=False)

    __table_args__ = (
        CommonTableArgs.__table_args__,
    )


class DepartmentClosure(db.Model):
    """部门层级结构，parent_id保存各级上级部门ID，depth表示级别差距"""
    __tablename__ = 'department_closure'
    # mysql_character_set = 'utf8mb4'  -- 使用该语句可以建立字符集为utf8mb4的表

    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    parent_id = db.Column(BIGINT(unsigned=True), nullable=False)
    depth = db.Column(BIGINT(unsigned=True), nullable=False)

    __table_args__ = (
        Index('idx_department_tree_d', department_id),
        Index('idx_department_tree_p', parent_id),
        CommonTableArgs.__table_args__,
    )

    @staticmethod
    def get_parent_department(department_id) -> set:
        tmp = (DepartmentClosure.query.with_entities(DepartmentClosure.parent_id).
               filter(DepartmentClosure.department_id == department_id).all())
        ret = set()
        if tmp:
            for i in tmp:
                ret.add(i[0])
        return ret

    @staticmethod
    def get_child_department(department_id) ->set:
        tmp = (DepartmentClosure.query.with_entities(DepartmentClosure.department_id).
               filter(DepartmentClosure.parent_id == department_id).all())
        ret = set()
        if tmp:
            for i in tmp:
                ret.add(i[0])
        return ret


class DepartmentPermission(db.Model):
    """部门员工具有的权限"""
    __tablename__ = 'department_permission'

    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    permission_id = db.Column(BIGINT(unsigned=True), nullable=False)

    __table_args__ = (
        Index('idx_department_permission_d', department_id),
        CommonTableArgs.__table_args__,
    )


class LeaderPermission(db.Model):
    """部门Leader具有的权限"""
    __tablename__ = 'leader_permission'

    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    permission_id = db.Column(BIGINT(unsigned=True), nullable=False)

    __table_args__ = (
        Index('idx_leader_permission_d', department_id),
        CommonTableArgs.__table_args__,
    )

