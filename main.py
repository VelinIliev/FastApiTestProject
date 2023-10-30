from fastapi import FastAPI, Body

app = FastAPI()


BOOKS = [
    {'title': 'title1', 'author': 'author1', 'category': 'science'},
    {'title': 'title2', 'author': 'author2', 'category': 'science'},
    {'title': 'title3', 'author': 'author3', 'category': 'history'},
    {'title': 'title4', 'author': 'author4', 'category': 'math'},
    {'title': 'title5', 'author': 'author5', 'category': 'math'},
    {'title': 'title6', 'author': 'author2', 'category': 'math'},
]


@app.get("/")
async def root():
    print('test')
    return {'message': 'Hello Velko'}


@app.get("/books")
async def view_all_books():
    return BOOKS


@app.get("/books/")
async def view_all_books_by_category(category: str):
    # http://127.0.0.1:8000/books/?category=history
    books = []
    for book in BOOKS:
        if book.get('category').lower() == category.lower():
            books.append(book)
    return books


@app.get("/books/{title}/")
async def view_single_book_by_title(title: str):
    # http://127.0.0.1:8000/books/title4/
    for book in BOOKS:
        if book.get('title').lower() == title.lower():
            return book


@app.get("/books/author/{author}/")
async def view_books_by_author_and_category(author: str, category: str):
    # http://127.0.0.1:8000/books/author/author2/?category=math
    books = []
    for book in BOOKS:
        if book.get('author').lower() == author.lower():
            if category == 'all':
                books.append(book)
            elif book.get('category').lower() == category.lower():
                books.append(book)
    return books


@app.get("/books/")
async def view_books_by_category_with_query(category: str):
    #   http://127.0.0.1:8000/books/?category=science
    books = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books.append(book)
    return books


@app.post("/books/create/")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete/{title}")
async def delete_book(title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').lower() == title.lower():
            del BOOKS[i]
            break
