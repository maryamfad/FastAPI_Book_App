from fastapi import FastAPI, Body

app = FastAPI()


BOOKS=[
  {
    'title': "To Kill a Mockingbird",
    'author': "Harper Lee",
    'category': "Fiction"
  },
  {
    'title': "1984",
    'author': "George Orwell",
    'category': "Dystopian"
  },
  {
    'title': "A Brief History of Time",
    'author': "Stephen Hawking",
    'category': "Science"
  },
  {
    'title': "The Great Gatsby",
    'author': "F. Scott Fitzgerald",
    'category': "Classic"
  },
  {
    'title': "Becoming",
    'author': "Michelle Obama",
    'category': "Biography"
  },
  {
    'title': "The Catcher in the Rye",
    'author': "J.D. Salinger",
    'category': "Fiction"
  }
];


@app.get("/books")
async def getAllBooks():
    return BOOKS


@app.get("/books/byAuthor/")
async def getBooksByAuthor(author: str):
    booksRoReturn = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            booksRoReturn.append(book)
    return booksRoReturn


@app.get("/books/{book_title}")
async def getABookByTitle(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        

@app.get("/books/{book_title}/")
async def getBookByCategoryAndAutor(author: str, category:str):
    booksRoReturn = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold() and book.get('category').casefold() == category.casefold():
            booksRoReturn.append(book)
    return booksRoReturn


@app.get("/books/")
async def getBooksByCategory(category: str):
    booksRoReturn = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            booksRoReturn.append(book)
    return booksRoReturn


@app.post("/books/addBook")
async def addBook(newBook=Body()):
    BOOKS.append(newBook)
    return newBook


@app.put("/books/updateBook")
async def updateBook(updatedBook=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updatedBook.get('title').casefold():
            BOOKS[i] = updatedBook
            return updatedBook
        

@app.delete("/books/deleteBook/{book_title}")
async def deleteBook(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            return {"message": f"Book {book_title} deleted successfully"}
