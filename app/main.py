# docker run --name postgresql -e POSTGRES_USER=test_user -e POSTGRES_PASSWORD=test_password -p 15432:5432 -d postgres
# uvicorn app.main:app --reload
from random import randint

from fastapi import FastAPI, HTTPException, Response, status
from loguru import logger
from psycopg2 import connect
from psycopg2.errors import Error
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from app.helpers import utils

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


def db_connection():
    return connect(
        host='localhost', port=15432, dbname='fastapi_course', user='test_user', password='test_password',
        cursor_factory=RealDictCursor
    ).cursor()


cursor = utils.wait(
    db_connection, timeout=2, interval=1, err_msg="Failed to connect to DB", ignored_exceptions=Error
)
logger.info("Database connection was successful!")

my_posts = [
    {"title": "title of post 1", "content": "123", "id": 1},
    {"title": "favourite food", "content": "pizza", "id": 2}
]


@app.get("/posts")
def get_posts():
    return my_posts


def find_post(post_id: int):
    for post in my_posts:
        if post['id'] == post_id:
            return post


def find_post_id(post_id: int):
    for i, post in enumerate(my_posts):
        if post['id'] == post_id:
            return i


@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    data = find_post(post_id)

    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f'post with id {post_id} not found'}

    return {"data": data}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randint(1, 1000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    index = find_post_id(post_id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} not found")

    del my_posts[index]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def create_posts(post_id: int, post: Post):
    index = find_post_id(post_id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} not found")

    post_dict = post.dict()
    post_dict['id'] = post_id
    my_posts[index] = post_dict
    return {"data": post_dict}
