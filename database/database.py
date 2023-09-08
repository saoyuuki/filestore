import pymongo, os
from config import DB_URI, DB_NAME
import random
import string


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']
col = database['shorten']


async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

async def get_short(short):
    return col.find_one({short: {'$exists': True}})

async def generate_random_string():
    characters = string.ascii_letters + string.digits
    st=''.join(random.choice(characters) for _ in range(15))
    return st

async def set_short(short):
    rndm=await generate_random_string()
    col.insert_one({rndm:short})
    return rndm