# create tables
CREATE_BOOKS_TABLE = (
    "CREATE TABLE IF NOT EXISTS books (book_title TEXT, book_author TEXT, isbn BIGINT PRIMARY KEY, quantity INTEGER);"
)
CREATE_MEMBERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS members (member_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT);"
)
CREATE_BOOK_ASSIGN = (
    "CREATE TABLE IF NOT EXISTS bookassign (isbn BIGINT, member_id INTEGER, date TEXT);"
)
CREATE_BOOK_RETURN = (
    "CREATE TABLE IF NOT EXISTS bookreturn (isbn BIGINT, member_id INTEGER, date TEXT, days INTEGER, fee INTEGER);"
)

# insert into tables
INSERT_BOOK = "INSERT INTO books (book_title, book_author, isbn, quantity) VALUES (%s, %s, %s, %s);"
INSERT_MEMBER = "INSERT INTO members (member_id, first_name, last_name) VALUES (%s, %s, %s);"
INSERT_ASSIGN = "INSERT INTO bookassign (isbn, member_id, date) VALUES (%s, %s, %s);"
INSERT_RETURN = "INSERT INTO bookreturn (isbn, member_id, date, days, fee) VALUES (%s, %s, %s, %s, %s);"

# view from tables
GET_ALL_BOOKS = "SELECT * FROM books;"
GET_BOOK = "SELECT * FROM books WHERE isbn = (%s);"
GET_BOOK_AUTHOR_TITLE = "SELECT * FROM books WHERE book_author=(%s) OR book_title=(%s)"

GET_ALL_MEMBERS = "SELECT * FROM members;"
GET_MEMBER = "SELECT * FROM members WHERE member_id=(%s);"
GET_NAME = "SELECT * FROM members WHERE first_name=(%s) OR last_name=(%s);"

GET_ASSIGN = "SELECT * FROM bookassign WHERE isbn=(%s) AND member_id=(%s);"

GET_ALL_ISSUES = "SELECT * FROM bookassign;"
GET_ALL_RETURNS = "SELECT * FROM bookreturn;"

# update tables
UPDATE_BOOK = "UPDATE books SET quantity=(%s) WHERE isbn=(%s);"
UPDATE_MEMBER = "UPDATE members SET first_name=(%s), last_name=(%s) WHERE member_id=(%s);"

# delete from tables
DELETE_BOOK = "DELETE FROM books WHERE isbn=(%s);"
DELETE_MEMBER = "DELETE FROM members WHERE member_id=(%s);"
DELETE_RETURN = "DELETE FROM bookreturn WHERE isbn=(%s) AND member_id=(%s);"
DELETE_ASSIGN = "DELETE FROM bookassign WHERE isbn=(%s) AND member_id=(%s);"
