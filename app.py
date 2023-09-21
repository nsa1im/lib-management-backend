from flask import Flask, jsonify, request
from flask_cors import CORS

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sample data
books = [
    {'book_title': 'A Historical Geography of China', 'book_author': 'Yi-Fu Tuan', 'isbn': 9780202366395, 'quantity': 200},
    {'book_title': 'A Guide to High-performance Powder Coating', 'book_author': 'Bob Utech', 'isbn': 9780872635470, 'quantity': 20},
    {'book_title': 'Mobile Multimedia in Action', 'book_author': 'Ilpo Koskinen', 'isbn': 9781412809429, 'quantity': 100}
]
members = [
    {'member_id': 19834, 'first_name': 'Ahmed', 'last_name': 'Ali'},
    {'member_id': 19221, 'first_name': 'Muhammad', 'last_name': 'Yusuf'},
    {'member_id': 20385, 'first_name': 'Kamau', 'last_name': 'Peter'}
]
bookAssign = [
    {'isbn': 9780202366395, 'member_id': 19834, 'date': '2023-06-02'}
]
bookReturn = [
    {'isbn': 9780202366395, 'member_id': 19834, 'date': '2023-08-01', 'days': 60, 'fee': 300}
]

# create book
@app.route('/addbook', methods=['POST'])
def add_book():
    book_title = request.form['title']
    book_author = request.form['author']
    book_isbn = request.form['isbn']
    book_quantity = request.form['quantity']
    for book in books:
        if book['isbn']==book_isbn:
            return jsonify({'message': 'Book exists!'})
    book = {
        'book_title': book_title,
        'book_author': book_author,
        'isbn': book_isbn,
        'quantity': book_quantity
    }
    return jsonify({'message': 'Book has been added successfully!'})
# BOOKS
# view all books
@app.route('/allbooks', methods=['GET'])
def get_books():
    return jsonify(books)

# view a book based on author or title
@app.route('/getbook/<string:author_title>', methods=['GET'])
def get_book(author_title):
    for book in books:
        if(book['book_title']==author_title or book['book_author']==author_title):
            return jsonify(book)
    return jsonify({'message': 'No such book exists!'})

# update book
@app.route('/updatebook', methods=['PUT'])
def update_book():
    for book in books:
        if(book['isbn']==request.form['isbn']):
            book['quantity']=request.form['quantity']
            return jsonify({'message': 'Book has been updated successfully!'})
    return jsonify({'message': 'No such book exists!'})

# delete book 
@app.route('/deletebook', methods=['DELETE'])
def delete_book():
    for book in books:
        if(book['isbn']==request.form['isbn']):
            books.remove(book)
            return jsonify({'message': 'Book has been deleted successfully!'})
    return jsonify({'message': 'No such book exists!'})

# MEMBERS
# view all members
@app.route('/allmembers', methods=['GET'])
def get_members():
    return jsonify(members)

# view a member based on name
@app.route('/getmember/<string:name>', methods=['GET'])
def get_member(name):
    for member in members:
        if(member['first_name']==name or member['last_name']==name):
            return jsonify(member)
    return jsonify({'message': 'No such member exists!'})

# update member
@app.route('/updatemember', methods=['PUT'])
def update_member():
    for member in members:
        if(member['id']==request.form['id']):
            member['first_name']=request.form['first_name']
            member['last_name']=request.form['last_name']
            return jsonify({'message': 'Member has been updated successfully!'})
    return jsonify({'message': 'No such member exists!'})

# delete member 
@app.route('/deletemember', methods=['DELETE'])
def delete_member():
    for member in members:
        if(member['id']==request.form['id']):
            members.remove(member)
            return jsonify({'message': 'Member has been deleted successfully!'})
    return jsonify({'message': 'No such member exists!'})

if __name__ == '__main__':
    app.run()