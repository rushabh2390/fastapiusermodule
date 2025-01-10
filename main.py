from sqladmin import Admin, ModelView
from database.database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response
from users.routers.users import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from users.models.users import User
import logging
logging.basicConfig(level=logging.DEBUG)


# App Object
app = FastAPI()
admin = Admin(app, engine)
app.include_router(user_router, tags=["users"])
origins = ["*"]


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.fullname]


admin.add_view(UserAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=200)
async def read_root():
    return Response("server is up and running")
