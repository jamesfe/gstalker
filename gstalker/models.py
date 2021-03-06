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
    min_major_ver = Column(Integer, nullable=False)
    min_minor_ver = Column(Integer, nullable=False)
    min_patch_ver = Column(Integer, nullable=False)
    exact_version = Column(String(255), index=True)
    max_major_ver = Column(Integer, nullable=True)
    max_minor_ver = Column(Integer, nullable=True)
    max_patch_ver = Column(Integer, nullable=True)
    max_inclusive = Column(Boolean, default=False)
    no_max = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    repository_moment = Column(postgresql.UUID, ForeignKey('gs_repo.id'))
    is_dev_dep = Column(Boolean, default=False)
    lang = Column(String(32), index=True)

    def serialize(self):
        ret_val = {
            'dep_name': self.dep_name,
            'exact_version': self.exact_version,
            'language': self.lang
        }
        return ret_val


"""
Migrations
"""
# alter table gs_deps add column patch_ver integer not null default 0;

# We need to add a max qualifier, so here are some new columns
"""
alter table gs_deps rename column minor_ver to min_minor_ver;
alter table gs_deps rename column major_ver to min_major_ver;
alter table gs_deps rename patch_ver to min_patch_ver;

alter table gs_deps add column max_patch_ver integer not null default 0;
alter table gs_deps add column max_minor_ver integer not null default 0;
alter table gs_deps add column max_major_ver integer not null default 0;

alter table gs_deps add column no_max boolean not null default false;
alter table gs_deps add column max_inclusive boolean not null default false;

"""
