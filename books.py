from typing import Optional
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

BOOKS = {
    "book_1": {"title": "Star Wars", "author": "Lucas"},
    "book_2": {"title": "title2", "author": "author2"},
    "book_3": {"title": "title3", "author": "author3"},
    "book_4": {"title": "title4", "author": "author4"},
    "book_5": {"title": "title5", "author": "author5"}
}

class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get("/") # decorater - path of the API variable
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS
# terminal command: uvicorn books:app --reload


# order matters, cant put this function below read_book cause of params
@app.get("/books/mybook")
async def read_favorite_book():
    return {"book_title": "My favorite book"}


@app.get("/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]


@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up"}
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down"}
    if direction_name == DirectionName.west:
        return {"Direction": direction_name, "sub": "Left"}
    if direction_name == DirectionName.east:
        return {"Direction": direction_name, "sub": "Right"}


@app.post("/")
async def create_book(book_title, book_author):
    curr_id = 0
    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split("_")[-1])
            if x > curr_id:
                curr_id = x

    BOOKS[f'book_{curr_id + 1}'] = {"title": book_title, "author": book_author}
    return BOOKS[f'book_{curr_id + 1}']