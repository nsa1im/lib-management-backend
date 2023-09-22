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
            cursor.execute(GET_BOOK_AUTHOR_TITLE, (book_author, book_title))
            books.append(cursor.fetchall())
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
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MEMBERS_TABLE)
            cursor.execute(GET_MEMBER, (member_id, ))
            if(cursor.fetchall()==[]):
                cursor.execute(INSERT_MEMBER, (member_id, first_name, last_name))
                return jsonify({'message': 'Member has been added successfully!'})
    return jsonify({'message': 'Member already exists!'})

# view all members
@app.route('/allmembers', methods=['GET'])
def get_members():
     with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ALL_MEMBERS)
            members = cursor.fetchall()
            return jsonify(members)

# view a member based on name
@app.route('/getmember', methods=['GET'])
def get_member():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    members = []
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_NAME, (first_name, last_name))
            members.append(cursor.fetchall())
            if(members==[[]]):
                return jsonify({'message': 'No such member exists!'})
            return jsonify(members)

# update member
@app.route('/updatemember', methods=['PUT'])
def update_member():
    member_id = request.form['member_id']
    first_name =request.form['first_name']
    last_name =request.form['last_name']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_MEMBER, (member_id, ))
            if(cursor.fetchall()==[]):
                return jsonify({'message': 'No such member exists!'})
            cursor.execute(UPDATE_MEMBER, (first_name, last_name, member_id))
            return jsonify({'message': 'Member has been updated successfully!'})

# delete member 
@app.route('/deletemember', methods=['DELETE'])
def delete_member():
    member_id = request.form['member_id']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_MEMBER, (member_id, ))
            if(cursor.fetchall()==[]):
                return jsonify({'message': 'No such member exists!'})
            else:
                cursor.execute(DELETE_MEMBER, (member_id, ))
                return jsonify({'message': 'Member has been deleted successfully!'})

# issue book
@app.route('/issue', methods=['POST'])
def issue():
    member_id = request.form['member_id']
    isbn = request.form['isbn']
    date = request.form['date']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_MEMBER, (member_id, ))
            if(cursor.fetchall()==[]):
                return jsonify({'message': 'No such member was found!'})
            else:
                cursor.execute(GET_BOOK, (isbn, ))
                if(cursor.fetchall()==[]):
                    return jsonify({'message': 'No such book was found!'})
                else:
                    cursor.execute(GET_ASSIGN, (isbn, member_id))
                    if(cursor.fetchall()==[]):
                        cursor.execute(INSERT_ASSIGN, (isbn, member_id, date))
                        cursor.execute(DELETE_RETURN, (isbn, member_id))
                        return jsonify({'message': 'Book issued successfully!'})
                    else:
                        return jsonify({'message': 'Book has already been issued!'})
                    
# issue book return
@app.route('/returnbook', methods=['POST'])
def returnbook():
    isbn = request.form['isbn']
    member_id = request.form['member_id']
    date = request.form['date']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ASSIGN, (isbn, member_id))
            if(cursor.fetchall()==[]):
                return jsonify({'message': 'No such issue was found!'})
            else:
                prev_date = cursor.fetchall()[0][2]
                days, fee = get_days(date, prev_date)
                cursor.execute(INSERT_RETURN, (isbn, member_id, date, days, fee))
                cursor.execute(DELETE_ASSIGN, (isbn, member_id))
                return jsonify({'message': 'Book return was issued!'})

if __name__ == '__main__':
    app.run()