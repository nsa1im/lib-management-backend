import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from CalculateDays.dayCalculator import get_days
from dbHelper.dbHelper import *

load_dotenv()

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# BOOKS
# create book
@app.route('/addbook', methods=['POST'])
def add_book():
    book_title = request.form['title']
    book_author = request.form['author'] 
    book_isbn = request.form['isbn']
    book_quantity = request.form['quantity']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_BOOKS_TABLE)
            cursor.execute(GET_BOOK, (book_isbn, ))
            if(cursor.fetchall()==[]):
                cursor.execute(INSERT_BOOK, (book_title, book_author, book_isbn, book_quantity))
                return jsonify({'message': 'Book has been added successfully!'})
    return jsonify({'message': 'Book already exists!'})

# view all books
@app.route('/allbooks', methods=['GET'])
def get_books():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ALL_BOOKS)
            books = cursor.fetchall()
            return jsonify(books)

# view a book based on author or title
@app.route('/getbook', methods=['GET'])
def get_book():
    book_author = request.form['author']
    book_title = request.form['title']
    books = []
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_BOOK_TITLE, (book_title, ))
            books1 = cursor.fetchall()
            cursor.execute(GET_BOOK_AUTHOR, (book_author, ))
            books2 = cursor.fetchall()
            if(books1 == books2):
                books.append(books1)
            else:
                books.append(books1)
                books.append(books2)
            if(books==[[]]):
                return jsonify({'message': 'No such book exists!'})
            return jsonify(books)
    

# update book
@app.route('/updatebook', methods=['PUT'])
def update_book():
    quantity = request.form['quantity']
    isbn = request.form['isbn']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_BOOK, (isbn, ))
            if(cursor.fetchall()==[]):
                return jsonify({'message': 'No such book exists!'})
            cursor.execute(UPDATE_BOOK, (quantity, isbn))
            return jsonify({'message': 'Book has been updated successfully!'})
    
# delete book 
@app.route('/deletebook', methods=['DELETE'])
def delete_book():
    isbn = request.form['isbn']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_BOOK, (isbn, ))
            if(cursor.fetchall()==[]):
                return jsonify({'message': 'No such book exists!'})
            else:
                cursor.execute(DELETE_BOOK, (isbn, ))
                return jsonify({'message': 'Book has been deleted successfully!'})

# MEMBERS
# create member
@app.route('/addmember', methods=['POST'])
def add_member():
    member_id = request.form['member_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    for member in members:
        if member['member_id']==member_id:
            return jsonify({'message': 'Member already exists!'})
    member = {
        'member_id': member_id,
        'first_name': first_name,
        'last_name': last_name
        }
    return jsonify({'message': 'Member has been added successfully!'})

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
        if(member['member_id']==request.form['member_id']):
            member['first_name']=request.form['first_name']
            member['last_name']=request.form['last_name']
            return jsonify({'message': 'Member has been updated successfully!'})
    return jsonify({'message': 'No such member exists!'})

# delete member 
@app.route('/deletemember', methods=['DELETE'])
def delete_member():
    for member in members:
        if(member['member_id']==request.form['member_id']):
            members.remove(member)
            return jsonify({'message': 'Member has been deleted successfully!'})
    return jsonify({'message': 'No such member exists!'})

# issue book
@app.route('/issue', methods=['POST'])
def issue():
    for member in members:
        if(member['member_id']==request.form['member_id']):
            for book in books:
                if(book['isbn']==request.form['isbn']):
                    bookAssign.append({
                        'isbn': request.form['isbn'], 
                        'member_id': request.form['member_id'], 
                        'date': request.form['date']
                    })
                    for bookreturn in bookReturn:
                        if(bookreturn['isbn']==request.form['isbn'] and 
                           bookreturn['member_id']==request.form['member_id']):
                            bookReturn.remove(bookreturn)
                    return jsonify({'message': 'Book assigned successfully!'})
    return jsonify({'message': 'No such details were found!'})

# issue book return
@app.route('/returnbook', methods=['POST'])
def returnbook():
    for bookassign in bookAssign:
        if(bookassign['isbn']==request.form['isbn'] and bookassign['member_id']==request.form['member_id']):
            days, fee = get_days(request.form['date'], bookassign['date'])
            bookReturn.append({
                'isbn': bookassign['isbn'],
                'member_id': bookassign['member_id'],
                'date': bookassign['date'],
                'days': days,
                'fee': fee
            })
            bookAssign.remove(bookassign)
            return jsonify({'message': 'Book return was issued!'})
    return jsonify({'message': 'No such details were found!'})

if __name__ == '__main__':
    app.run()