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
    """A repository that has either a package.json or a requirements.txt"""
    __tablename__ = 'gs_repo'

    id = Column(postgresql.UUID, default=generate_uuid, primary_key=True, unique=True)
    repo_name = Column(String(255), index=True)
    sha = Column(String(255), index=True)
    user = Column(String(255), index=True)
    target_file_url = Column(String(255), index=True, unique=True)
    repo_type = Column(String(32), index=True)
    check_state = Column(String(32))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Dependency(BASE):
    """A dependency that a repository has."""
    __tablename__ = 'gs_deps'
    id = Column(postgresql.UUID, default=generate_uuid, primary_key=True, unique=True)
    dep_name = Column(String(255), index=True)
    major_ver = Column(Integer, nullable=False)
    minor_ver = Column(Integer, nullable=False)
    patch_ver = Column(Integer, nullable=False)
    exact_version = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.now)
    repository_moment = Column(postgresql.UUID, ForeignKey('gs_repo.id'))
    is_dev_dep = Column(Boolean, default=False)
    lang = Column(String(32), index=True)


"""
Migrations
"""
# alter table gs_deps add column patch_ver integer not null default 0;
