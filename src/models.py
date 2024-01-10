import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

#Tabla muchos a muchos
followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('following_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    bio = Column(String(250))
    profile_image = Column(String(250))

    #Relaciones
    posts = relationship('Post', back_populates='user')
    followers = relationship('User', secondary=followers, 
                             primaryjoin=(followers.c.follower_id == id),
                             secondaryjoin=(followers.c.following_id == id),
                             backref="following"
                            )

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image = Column(String(250))
    caption = Column(String(250))

    #Relaciones
    likes = relationship('User', secondary='post_likes')
    comments = relationship('Comment', back_populates='post')

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    text = Column(String(250))
    created_at = Column(DateTime)

# Many-to-Many table for Post likes
post_likes = Table(
    'post_likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('post.id'), primary_key=True)
)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
