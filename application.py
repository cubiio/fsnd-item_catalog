"""
Application docstrings here
"""

# [START Imports]
# Flask
from flask import Flask, render_template, request, redirect, url_for
# from flask_wtf.csrf import CSRFProtect

# SQLAlchemy
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

# Db
from database_setup import Base, Category, Book
# [END Imports]


# [START Database set-up]
engine = create_engine('sqlite:///cataloguebooks.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# [END Database set-up]


# Flask
# csrf = CSRFProtect()


# def create_app():
#     app = Flask(__name__)
#     csrf.init_app(app)

app = Flask(__name__)


# [START Routes]
# Home /index
@app.route('/')
@app.route('/catalogue')
def index():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('index.html', categories=categories)


# show books in one category
@app.route('/category/<int:category_id>/')
def showBooks(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(category_id=category_id).all()
    return render_template('/categorybooks.html',
                           category_id=category_id, category=category,
                           books=books)


# display one book
@app.route('/book/<int:book_id>')
def theBook(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return render_template('/book.html', book=book)


# login
@app.route('/login')
def login():
    return render_template('/login.html')


# new category
@app.route('/category/new')
def newCategory():
    return render_template('/newcategory.html')


# edit category
@app.route('/category/<int:category_id>/edit')
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    return render_template('/editcategory.html', category=editedCategory)


# delete category
@app.route('/category/<int:category_id>/delete')
def deleteCategory(category_id):
    deletedCategory = session.query(Category).filter_by(id=category_id).one()
    return render_template('/deletecategory.html', category=deletedCategory)


# new book
@app.route('/book/new', methods=['GET', 'POST'])
def newBook():
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST':
        c = request.form['category']
        c_submitted = session.query(Category).filter(
            Category.name == c).first()
        newBook = Book(name=request.form['name'],
                       description=request.form['description'],
                       price=request.form['price'],
                       author=request.form['author'],
                       category=c_submitted)
        session.add(newBook)
        session.commit()
        # add flash message; also to redirect page to display msg

        # amend redirect
        return redirect(url_for('index'))
    return render_template('/newbook.html', categories=categories)


# edit book
@app.route('/category/<int:category_id>/book/<int:book_id>/edit')
def editBook(category_id, book_id):
    editedBook = session.query(Book).filter_by(id=book_id).one()
    # category = session.query(Category).filter_by(id=category_id).one()
    return render_template('/editbook.html', category_id=category_id,
                           book_id=book_id, book=editedBook)


# delete book
@app.route('/category/<int:category_id>/book/<int:book_id>/delete')
def deleteBook(category_id, book_id):
    deletedBook = session.query(Book).filter_by(id=book_id).one()
    # category = session.query(Category).filter_by(id=category_id).one()
    return render_template('/deletebook.html', category_id=category_id,
                           book_id=book_id, book=deletedBook)
# [END Routes]


# Flask
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
