"""
Database set-up script for item catalogue
"""

# [START Imports]
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
# [END Imports]

Base = declarative_base()


# class User(Base):
#     """
#     Table to store User information
#     """
#     __tablename__ = 'user'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#     email = Column(String(250), nullable=False)
#     picture = Column(String(250))


class Category(Base):
    """
    Table to store categories used to classify the books
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    # user_id = Column(Integer, ForeignKey('user.id'))
    # user = relationship(User)


class Book(Base):
    """
    Table to store books
    """
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    author = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    # user_id = Column(Integer, ForeignKey('user.id'))
    # user = relationship(User)


engine = create_engine('sqlite:///cataloguebooks.db')

Base.metadata.create_all(engine)
