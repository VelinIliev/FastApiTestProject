from typing import Optional

from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1800, lt=2030)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Enter the author',
                'description': 'Enter a description',
                'rating': 'integer 1-5',
                'published_date': 'Publish year'
            }
        }


BOOKS = [
    Book(1, 'Title1', 'Author1', 'Good Book1', 5, 2020),
    Book(2, 'Title2', 'Author2', 'Good Book2', 4, 2021),
    Book(3, 'Title3', 'Author1', 'Good Book3', 2, 2022),
    Book(4, 'Title4', 'Author3', 'Good Book4', 5, 2023),
    Book(5, 'Title5', 'Author4', 'Good Book5', 4, 2024),
    Book(6, 'Title6', 'Author5', 'Good Book6', 2, 2025),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def view_books():
    return BOOKS


def find_book_id(book: Book):
    book.id = BOOKS[-1].id + 1 if len(BOOKS) > 1 else 1
    return book


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def view_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(gt=0, lt=6)):
    books = []
    for book in BOOKS:
        if book.rating == rating:
            books.append(book)
    return books


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def get_books_by_year(year: int = Query(gt=1800, lt=2030)):
    books = []
    for book in BOOKS:
        if book.published_date == year:
            books.append(book)
    return books


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookRequest):
    new_book = Book(**book_data.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found.')


@app.delete("/books/{book_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found.')
