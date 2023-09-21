from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run()