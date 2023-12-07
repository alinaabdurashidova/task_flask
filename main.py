from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from datetime import date

DATABASE_URL = "postgresql://alina:1@localhost/book"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    created_at = Column(Date, nullable=True)

Base.metadata.create_all(bind=engine)

BookPydantic = sqlalchemy_to_pydantic(Book, exclude=['id'])

def create_book(db_book: BookPydantic):
    new_book = Book(**db_book.dict())
    with SessionLocal() as session:
        session.add(new_book)
        session.commit()
    return new_book

def get_all_books():
    book_list = []
    with SessionLocal() as db:
        books = db.query(Book).all()
        book_list = [{'id': book.id, 'title': book.title, 'author': book.author,
                      'genre': book.genre, 'created_at': book.created_at.strftime("%Y-%m-%d") if book.created_at else None} for book in books]
    return book_list

new_book_data = {
    'title': 'Kapitanskaia dochka',
    'author': 'Pushkin',
    'genre': 'roman',
    'created_at': date(1823, 1, 1)
}

new_book = BookPydantic(**new_book_data)
created_book = create_book(new_book)
print(get_all_books())


def update_book(book_id: int, updated_data: BookPydantic):
    with SessionLocal() as session:
        existing_book = session.query(Book).filter(Book.id == book_id).first()
        if existing_book is None:
            return None
            
        for key, value in update_data.items():
            setattr(existing_book, key, value)
        session.commit()
        session.refresh(existing_book)
        return existing_book

update_data = {'title': 'First teacher', 'author': 'Aitmatov', 'genre': 'rasskaz', 'created_at': date(1956, 5, 2)}
update_result = update_book(5, update_data)
print(update_result)
print(get_all_books())

def delete_book_by_id(book_id: int):
    with SessionLocal() as session:
        book = session.query(Book).filter(Book.id == book_id).first()
        if book:
            session.delete(book)
            session.commit()
            return True
        return False


delete_result = delete_book_by_id(3)
print(delete_result)
print(get_all_books())