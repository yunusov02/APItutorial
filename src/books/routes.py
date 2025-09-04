from fastapi import HTTPException, status, APIRouter
from .schemas import Book, BookUpdateModel
from typing import List

from .data import books

book_router = APIRouter()

raise_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book Not Found"
    )


@book_router.get('/books', response_model=List[Book])
async def get_all_books():
    return books


@book_router.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book) -> dict:
    new_book = book.model_dump()
    books.append(new_book)
    return new_book



@book_router.get('/books/{book_id}')
async def get_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    
    raise raise_exception

@book_router.patch("/books/{book_id}")
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book
    
    raise raise_exception


@book_router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)

            return{}
        
    raise raise_exception
