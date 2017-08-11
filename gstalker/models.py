# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, DateTime, Boolean, Integer
import uuid

BASE = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class RepositoryMoment(BASE):
    __tablename__ = 'repo'

    id = Column(postgresql.UUID, default=generate_uuid, primary_key=True, unique=True)
    repo_name = Column(String(255), index=True, unique=True)
    sha1 = Column(String(255), index=True, unique=True)
    user = Column(String(255), index=True, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Dependency(BASE):
    __tablename__ = 'deps'
    id = Column(postgresql.UUID, default=generate_uuid, primary_key=True, unique=True)
    dep_name = Column(String(255), index=True, unique=True)
    major_ver = Column(Integer, nullable=False)
    minor_ver = Column(Integer, nullable=False)
    exact_version = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    repository_moment = Column(postgresql.UUID, ForeignKey('repository_moment.id'))
    is_dev_dep = Column(Boolean, default=False)
    lang = Column(String(32), index=True, unique=False)
