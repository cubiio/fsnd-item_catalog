"""
Database set-up script for item catalogue
"""

# [START Imports]
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy import create_engine
# [END Imports]


base = declarative_base()

# no users; dev 1
# engine = create_engine(
#     'sqlite:////vagrant/fsnd-item_catalog/catalog/cataloguebooksv1.db')

# with users; dev >2
engine = create_engine(
    'sqlite:////vagrant/fsnd-item_catalog/catalog/cataloguebooksv3.db')


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
# [END Db engine and session]


class User(base):
    """
    Table to store User information
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(base):
    """
    Table to store categories used to classify the books
    Inputs required category_name
    Category_id is autogenerated
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """
        Return Category object data in serialized JSON format
        """
        return {
            'name': self.name,
            'id': self.id,
        }


class Book(base):
    """
    Table to store books
    Inputs required book_name; and foreign key = category_name
    Inputs optional book_description, book_author, book_price
    Book_id is autogenerated
    """
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(750))
    author = Column(String(250))
    price = Column(String(8))
    created_at = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """
        Return Book object data in serialized JSON format
        """
        return {
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'price': self.price,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


base.metadata.create_all(engine)
