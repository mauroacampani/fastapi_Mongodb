from config.db import collection
from schemas.user import userEntity, usersEntity
from fastapi import APIRouter, status,Response
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()


@user.get('/users')
def find_all_users():
    return usersEntity(collection.find())
    

@user.post('/users')
def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]
    id = collection.insert_one(new_user).inserted_id
    user = collection.find_one({"_id": id})
    return userEntity(user)


@user.get('/users/{id}')
def find_user(id: str):
    return userEntity(collection.find_one({"_id": ObjectId(id)}))


@user.put("/users/{id}")
def update_user(id: str, user: User):
    collection.find_one_and_update({'_id': ObjectId(id)}, {'$set': dict(user)})


@user.delete("/users/{id}")
def delete_user(id: str):
    collection.find_one_and_delete({
        "_id": ObjectId(id)
    })
    return Response(status_code=HTTP_204_NO_CONTENT)