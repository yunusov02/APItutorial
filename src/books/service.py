from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.models import Book
from src.books.schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc


class BookService:
    async def get_all_books(self, session: AsyncSession):
        """
        Get a list of all books

        Returns:
            list: list of books
        """
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)

        return result.all()

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        
        book_dict_data = book_data.model_dump()

        if "published_date" in book_dict_data.keys():
            book_dict_data["published_date"] = datetime.strptime(
                book_dict_data["published_date"], "%Y-%m-%d"
            ).date()

        new_book = Book(**book_dict_data)
        
        session.add(new_book)
        await session.commit()

        return new_book
    
    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)

        result = await session.exec(statement)

        book = result.first()

        return book if book is not None else None
    

    async def update_book(self, book_uid: str, update_date: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is not None:
            update_dict_data = update_date.model_dump()

            for k, v in update_dict_data:
                setattr(book_to_update, k, v)

            await session.commit()

            return book_to_update
        return None
    

    async def delete_book(self, book_uid:str , session:AsyncSession):
        book_to_delete = await self.get_book(book_uid,session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)

            await session.commit()

            return {}

        return None


        