# coding=utf-8
# @File  : test.py
# @Author: PuJi
# @Date  : 2018/4/26 0026
# Maybe it's not necessary
from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float, rea
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()# create sqlorm base class


blogs_tags = Table('blogs_tags',
                   Column('blog_id', String(45), ForeignKey('blogs.id')),
                   Column('tag_id', Integer, ForeignKey('tags.id')))


users_blogs = Table('users_blogs',
                    Column('user_id', Integer, ForeignKey('users.id')),
                    Column('blog_id', Integer, ForeignKey('blogs.id')))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(128))
    email = Column(String(32))
    cellphone = Column(String(12))
    token = Column(String(128), index=True)
    timestamp = Column(String(10))
    balance = Column(Float)
    wallet = Column(String(34))
    pay_password = Column(String(128))
    reads = relationship(
        'Blog',
        secondary=users_blogs,
        backref=backref('blogs', lazy='dynamic')
    )
    # reads = db.Column(db.String(128))
    # Reserved field
    pre1 = Column(String())
    pre2 = Column(String())

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)