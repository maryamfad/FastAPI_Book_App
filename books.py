from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.exceptions import HTTPException
from starlette import status

app = FastAPI()

class Book:
  id: int
  title: str
  author: str
  description : str
  rating: int
  publishedDate: int

  def __init__(self, id: int, title: str, author: str, description: str, rating: int, publishedDate: int):
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating
    self.publishedDate = publishedDate

class BookRequest(BaseModel):
  id: Optional[int] = Field(description='ID is not needed on create request', default=None)
  title: str =Field(min_length=3)
  author: str = Field(min_length=1)
  description: str = Field(min_length=1, max_length=100)
  rating: int = Field(gt=0, lt=6)
  publishedDate: int = Field(gt=1900)

  model_config = {
    "json_schema_extra":{
      "example": {
        "title": "Sample Book",
        "author": "Sample Author",
        "description": "Sample Description",
        "rating": 5,
        "publishedDate":2012
      }
    }
  }
  
Books = [
    Book(1, "Book 1", "Author 1", "Description 1", 5, 2012),
    Book(2, "Book 2", "Author 2", "Description 2", 4, 2013),
    Book(3, "Book 3", "Author 3", "Description 3", 3, 2014),
    Book(4, "Book 4", "Author 4", "Description 4", 2, 2015),
    Book(5, "Book 5", "Author 5", "Description 5", 1, 2012)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def getAllbooks():
  return Books

@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def getBookByPublishDate( publishedDate: int = Query(gt=1999, lt=2031)):
  booksToReturn = []
  for book in Books:
    if book.publishedDate == publishedDate:
      booksToReturn.append(book)
  return booksToReturn

@app.get("/books/{bookId}", status_code=status.HTTP_200_OK)
async def getBookById(bookId: int = Path(gt=0)):
  for book in Books:
    if book.id == bookId:
      return book
  raise HTTPException(status_code=404, detail='Item not found')

@app.get("/books/", status_code=status.HTTP_200_OK)
async def getBookByRating( rating: int = Query(gt=0,lt=6)):
  booksToReturn = []
  for book in Books:
    if book.rating == rating:
      booksToReturn.append(book)
  return booksToReturn



@app.post("/createBook", status_code=status.HTTP_201_CREATED)
async def createBook(bookRequest : BookRequest):
  newBook = Book(**bookRequest.model_dump())
  Books.append(addIdToBook(newBook))
  return bookRequest


def addIdToBook(book: Book):
    book.id = 1 if len(Books) == 0 else Books[-1].id + 1
    return book


@app.put("/books/updateBook", status_code=status.HTTP_204_NO_CONTENT)
async def updateBook(book: BookRequest):
    bookChanged = False
    for i in range(len(Books)) :
        if Books[i].id == book.id:
            Books[i] = book
            bookChanged = True
    if not bookChanged:
        raise HTTPException(status_code=404, detail='Item not found')
  
  
@app.delete("/books/{bookId}")
async def deleteBook(bookId: int = Path(gt=0)):
    bookChanged = False
    for i in range(len(Books)):
        if Books[i].id == bookId:
            Books.pop(i)
            bookChanged = True
    if not bookChanged:
        raise HTTPException(status_code=404, detail='Item not found')