# First, install: pip install Flask SQLAlchemy


# In this example, we first import the necessary modules, including Flask and SQLAlchemy. We then set up the Flask app and connect to a local SQLite database using SQLAlchemy.
# We define a model for the data we'll be working with using the Book class, which inherits from db.Model. We then define API routes for handling HTTP requests using app.route().
# For example, the GET /books route retrieves all books from the database and returns them as a JSON response. The POST /books route creates a new book by parsing the request body and saving it to the database. The PUT /books/<int:book_id> route updates an existing book by finding it based on the book_id parameter and replacing it with the new data in the request body. The DELETE /books/<int:book_id> route deletes a book based on the book_id parameter.


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Set up Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect to SQLite database
db = SQLAlchemy(app)

# Define model for data
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.String(10))
    pages = db.Column(db.Integer)

    def __init__(self, title, author, published_date, pages):
        self.title = title
        self.author = author
        self.published_date = published_date
        self.pages = pages

# Define API routes
@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/books')
def get_all_books():
    books = Book.query.all()
    return jsonify([book.serialize() for book in books])

@app.route('/books', methods=['POST'])
def create_book():
    book_data = request.get_json()
    book = Book(title=book_data['title'], author=book_data['author'], 
                published_date=book_data['published_date'], pages=book_data['pages'])
    db.session.add(book)
    db.session.commit()
    return jsonify(book.serialize())

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    book_data = request.get_json()
    book.title = book_data['title']
    book.author = book_data['author']
    book.published_date = book_data['published_date']
    book.pages = book_data['pages']
    db.session.commit()
    return jsonify(book.serialize())

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

# Run the app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
