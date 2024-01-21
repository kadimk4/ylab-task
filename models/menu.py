import uuid

import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = 'menu'
    uuid = sq.Column(UUID(as_uuid=True), primary_key=True, name='uuid', default=uuid.uuid4)
    title = sq.Column(type_=sq.String, name='title', nullable=False)
    description = sq.Column(type_=sq.String, name='description', nullable=False)
    submenus = relationship('Submenu', back_populates='menu', cascade="all, delete-orphan", lazy='joined')


class Submenu(Base):
    __tablename__ = 'submenu'
    uuid = sq.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = sq.Column(sq.String, name='title', nullable=False)
    description = sq.Column(sq.String, name='description', nullable=False)
    menu_id = sq.Column(UUID(as_uuid=True), sq.ForeignKey('menu.uuid'))
    menu = relationship('Menu', back_populates='submenus', single_parent=True, lazy='joined')
    dishes = relationship('Dishes', back_populates='submenu', cascade="all, delete-orphan", lazy='joined')


class Dishes(Base):
    __tablename__ = 'dishes'
    uuid = sq.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = sq.Column(sq.String, name='title', nullable=False)
    description = sq.Column(sq.String, name='description', nullable=False)
    price = sq.Column(sq.String, nullable=False)
    submenu_id = sq.Column(UUID(as_uuid=True), sq.ForeignKey('submenu.uuid'))
    submenu = relationship('Submenu', back_populates='dishes', single_parent=True, lazy='joined')
