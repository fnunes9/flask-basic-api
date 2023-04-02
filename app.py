from flask import Flask, request, jsonify

app = Flask(__name__)

# data
books = [
    {'id': 0,
     'title': 'Flask Web Development: Developing Web Applications with Python',
     'author': 'Miguel Grinberg ',
     'year_published': '2018'},
    {'id': 1,
     'title': 'Docker: Up & Running: Shipping Reliable Containers in Production',
     'author': 'Sean P Kane, Karl Matthias',
     'published': '2018'},
    {'id': 2,
     'title': 'Learning SQL: Generate, Manipulate, and Retrieve Data',
     'author': 'Alan Beaulieu',
     'published': '2020'}
]

# helpers
def get_book_by_id(id):
    for book in books:
        if book['id'] == id:
            return book
    return None

# rotas
@app.route('/')
def home():
    return 'This is my book store API'

@app.route('/books')
def get_books():
    return jsonify(books)

@app.route('/book/<int:id>')
def book(id):
    book_ = get_book_by_id(id)
    if book_ is not None:
        return jsonify(book_)
    else:
        return "Error. Resource not found", 404
    
@app.route('/add', methods=["POST"])
def add_book():
    book = request.get_json(force=True) 
    dict_to_return = {'OK:': {'book':book}}
    books.append(book)
    return jsonify(dict_to_return), 200

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_book_by_id(id)

    if book is None:
        return "Error. Resource not found", 404

    if request.method == 'POST':
        book_ = request.get_json(force=True)

        for book in books:
            if book['id'] == id:
                book['id'] =  book_['id']
                book['author'] = book_['author']
                book['title'] = book_['title']
                book['published'] = book_['published']

    return "Update successfully!", 200

@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    book = get_book_by_id(id)

    if book is None:
        return "Error. Resource not found", 404

    idx = books.index(book)
    books.pop(idx)

    return "Item removed successfully!", 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)