from typing import Optional
from flask import Flask, render_template
from flask_pymongo import PyMongo
from fastapi import Body, FastAPI, Path
from pydantic import BaseModel, ValidationError, validator
import pymongo
from bson.son import SON
import pprint
import asyncio
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from motor.motor_asyncio import AsyncIOMotorClient

myclient = AsyncIOMotorClient("mongodb://localhost:27017/")
mydb = myclient["book_database"]
mycol = mydb["books"]
app = FastAPI()

# Creating the database
async def create():
    # Deleting existing database for easier testing
    await mycol.delete_many({})
    await mydb.books.drop()

    x = await mydb.books.insert_many([
        {
            "_id": 1,
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "description": "The Catcher in the Rye is an American novel by J. D. Salinger that was partially published in serial form 1945–46 before being novelized in 1951. Originally intended for adults, it is often read by adolescents for its themes of angst and alienation, and as a critique of superficiality in society.",
            "price": 8.93,
            "stock": 7
        },

        {
            "_id": 2,
            "title": "Animal Farm",
            "author": "George Orwell",
            "description": "Animal Farm is a beast fable, in the form of a satirical allegorical novella, by George Orwell, first published in England on 17 August 1945. It tells the story of a group of farm animals who rebel against their human farmer, hoping to create a society where the animals can be equal, free, and happy.",
            "price": 10.76,
            "stock": 1
        },

        {
            "_id": 3,
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "description": "To Kill a Mockingbird is a novel by the American author Harper Lee. It was published in 1960 and was instantly successful. In the United States, it is widely read in high schools and middle schools",
            "price": 8.89,
            "stock": 2
        },

        {
            "_id": 4,
            "title": "The Story",
            "author": "A'Ziah King",
            "description": "about house",
            "price": 28.00,
            "stock": 40
        },

        {
            "_id": 5,
            "title": "Gump and Co.",
            "author": "Winston Groom",
            "description": "Gump & Co. is a 1995 novel by Winston Groom. It is the sequel to his 1986 novel Forrest Gump and the Academy Award-winning 1994 film of the same name starring Tom Hanks. It was written to chronicle Forrest's life throughout the 1980s.",
            "price": 16.89,
            "stock": 15
        },

        {
            "_id": 6,
            "title": "The Metamorphosis",
            "author": "Franz Kafka",
            "description": "Metamorphosis is a novella written by Franz Kafka which was first published in 1915. One of Kafka's best-known works, Metamorphosis tells the story of salesman Gregor Samsa, who wakes one morning to find himself inexplicably transformed into a huge insect and subsequently struggles to adjust to this new condition.",
            "price": 10.79,
            "stock": 2
        },

        {
            "_id": 7,
            "title": "White Nights",
            "author": "Fyodor Dostoevsky",
            "description": "When his plane makes an emergency landing in Siberia, ballet dancer Nikolai Rodchenko (Mikhail Baryshnikov) is recognized as a defector and brought into custody. Returned to Leningrad and reunited with his former love, aging prima ballerina Galina Ivanova (Helen Mirren), Nikolai meets American dancer Raymond Greenwood (Gregory Hines), who defected to the Soviet Union during the Vietnam War but has secretly grown disenchanted. Together, they plot an escape to the American consulate and freedom.",
            "price": 7.19,
            "stock": 6
        },

        {
            "_id": 8,
            "title": "Fahrenheit 451",
            "author": "Ray Bradbury",
            "description": "Fahrenheit 451 is a 1953 dystopian novel by American writer Ray Bradbury. Fahrenheit 451 presents an American society where books have been personified and outlawed and 'firemen' burn any that are found.",
            "price": 8.89,
            "stock": 9
        },

        {
            "_id": 9,
            "title": "A Clockwork Orange",
            "author": "Anthony Burgess",
            "description": "A Clockwork Orange is a dystopian satirical black comedy novel by English writer Anthony Burgess, published in 1962. It is set in a near-future society that has a youth subculture of extreme violence.",
            "price": 17.89,
            "stock": 21
        },

        {
            "_id": 10,
            "title": "A Moveable Feast",
            "author": "Ernest Hemingway",
            "description": "A Moveable Feast is a 1964 memoir and belles-lettres by American author Ernest Hemingway about his years as a struggling expat journalist and writer in Paris during the 1920s. It was published posthumously.",
            "price": 10.99,
            "stock": 13
        },

        {
            "_id": 11,
            "title": "The Old Man and the Sea",
            "author": "Ernest Hemingway",
            "description": "The Old Man and the Sea is a novella written by the American author Ernest Hemingway in 1951 in Cayo Blanco, and published in 1952. It was the last major work of fiction written by Hemingway that was published during his lifetime.",
            "price": 12.99,
            "stock": 12
        }
    ])

    await mydb.books.create_index(
        [
            ("author", 1),
            ("title", -1)
        ]
    )

    await mydb.books.create_index(
        [
            ("title", 1),
            ("stock", -1)
        ]
    )

    await mydb.books.create_index(
        [
            ("title", 1),
            ("price", -1)
        ]
    )
    return


# Aggregation Pipelines
stockPipeline = [
    {"$unwind": "$stock"},
    {"$group": {'_id': None, "inStock":{"$sum": "$stock"}}}
]

booksPipeline = [
    {"$unwind": "$title"},
    {"$group": {"_id": "$title", "inStock": {"$sum": "$stock"}}},
    {"$sort": SON([("inStock", 1), ("id", -1)])},
    {"$limit": 5}
]

authorPipeline = [
    {"$unwind": "$author"},
    {"$group": {"_id": "$author", "numOfBooksInStore": {"$sum": "$stock"}}},
    {"$sort": SON([("numOfBooksInStore", -1), ("id", -1)])},
    {"$limit": 5}
]

# Aggregation
async def aggregation():
    await create()
    totalnumofbooks = await mydb.books.aggregate(stockPipeline).to_list(None)
    top5sellerslist = await mydb.books.aggregate(booksPipeline).to_list(None)
    top5authorslist = await mydb.books.aggregate(authorPipeline).to_list(None)
    print("")
    print("Total number of books in the store: ", totalnumofbooks)
    print("")

    print("The top 5 bestselling books: ")
    for books in top5sellerslist:
        print(books)

    print("")
    print("The top 5 authors with the most books in the store: ")
    for authors in top5authorslist:
        print(authors)
    return

# Running aggregation
asyncio.create_task(aggregation()) # Run this line only when running "uvicorn bookstore:app --reload"
# asyncio.run(aggregation()) # Run this line only When running python file itself


# Pydantic models and data validation
class Book(BaseModel):
    title: str
    author: str
    description: str
    price: float
    stock: int

    @validator('title')
    def title_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError('must be a string')
        return v

    @validator('author')
    def author_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError('must be a string')
        return v

    @validator('description')
    def description_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError('must be a string')
        return v

    @validator('price')
    def price_must_be_float(cls, v):
        if not isinstance(v, float):
            raise ValueError('must be a float')
        return v

    @validator('stock')
    def stock_must_be_int(cls, v):
        if not isinstance(v, int):
            raise ValueError('must be a int')
        return v


class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


# API Endpoints
@app.get('/')
async def index():
    book_collection = []
    async for y in mycol.find():
        book_collection.append(y)
    return book_collection


@app.get('/books/{book_id}')
async def get_book(book_id: int = Path(description="The ID of the book you want to view", gt=0)):
    if await mycol.find_one({"_id": book_id}) is None:
        return {"Error": "Book does not exists"}
    x = await mycol.find_one({"_id": book_id})
    return x


@app.get('/books')
async def get_books():
    book_collection = []
    async for y in mycol.find():
        book_collection.append(y)
    return book_collection


@app.get('/search')
async def search_book(title: Optional[str] = None, author: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    main_q = {}
    if title != None:
        main_q["title"] = {"$regex": title.title()}
    if author != None:
        main_q["author"] = {"$regex": author.title()}
    if min_price != None and max_price != None:
        main_q["price"] = {"$gt": min_price, "$lt": max_price}
    elif min_price != None:
        main_q["price"] = {"$gt": min_price}
    elif max_price != None:
        main_q["price"] = {"$lt": max_price}

    book_collection = []
    async for y in mycol.find(main_q):
        book_collection.append(y)
    return book_collection


@app.post("/books")
async def create_book(book: Book):
    num = 0
    while True:
        num += 1
        if await mycol.find_one({"_id": num}) is None:
            book_title = book.title
            book_author = book.author
            book_description = book.description
            book_price = book.price
            book_stock = book.stock

            x = await mydb.books.insert_one({"_id": num,
                                        "title": book_title,
                                        "author": book_author,
                                        "description":  book_description,
                                        "price": book_price,
                                        "stock": book_stock})
            return {"Message": "Book added successfully"}


@app.put("/books/{book_id}")
async def update_book(book_id: int, book: UpdateBook):
    if await mycol.find_one({"_id": book_id}) is None:
        return {"Error": "book does not exists"}
    if book.title != None:
        book_title = book.title
        q = {"_id" : book_id}
        update = {"$set": {"title": book_title}}
        mycol.update_one(q, update)
    if book.author != None:
        book_author = book.author
        q = {"_id" : book_id}
        update = {"$set": {"author": book_author}}
        mycol.update_one(q, update)
    if book.description:
        book_description = book.description
        q = {"_id" : book_id}
        update = {"$set": {"description": book_description}}
        mycol.update_one(q, update)
    if book.price != None:
        book_price = book.price
        q = {"_id" : book_id}
        update = {"$set": {"price": book_price}}
        mycol.update_one(q, update)
    if book.stock != None:
        book_stock = book.stock
        q = {"_id" : book_id}
        update = {"$set": {"stock": book_stock}}
        mycol.update_one(q, update)
    return {"Message": "Book updated successfully"}
    

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    if await mycol.find_one({"_id": book_id}) is None:
        return {"Error": "Book does not exists"}
    
    q = {"_id": book_id}
    mycol.delete_one(q)
    
    return {"Message": "Book deleted successfully"}
