from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://maei86957:b.Susan1997@cluster0.ckmph.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)
db = client.book

def insert_cats():
    result_many = db.cats.insert_many(
        [
            {
                "name": "Barsik",
                "age": 3,
                "features": ["ходить в капці", "дає себе гладити", "рудий"]
            },

            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
        ]
    )
    print("Вставлено котів:", result_many.inserted_ids)


def one_cat(name):
    try:
        result = db.cats.find_one({"name": name})
        if result:
            print(result)
        else:
            print("Кота не знайдено.")
    except Exception as e:
        print(f"Виникла помилка при виконанні запиту: {e}")


def update_age(name, new_age):
    try:
        db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
        result = db.cats.find_one({"name": name})
        if result:
            print(result)
        else:
            print("Кота не знайдено.")
    except Exception as e:
        print(f"Виникла помилка при виконанні запиту: {e}")


def update_features(name, new_features):
    try:
        result = db.cats.update_one({"name": name}, {"$set": {"features": new_features}})
        if result.matched_count:
            print(f"Оновлені характеристики кота {name}: {new_features}.")
        else:
            print("Кота не знайдено.")
    except Exception as e:
        print(f"Виникла помилка при виконанні запиту: {e}")

def delete_one(name):
    try:
        result = db.cats.delete_one({"name": name})
        if result.deleted_count:
            print(f"Кота {name} успішно видалено.")
        else:
            print("Кота не знайдено.")
    except Exception as e:
        print(f"Виникла помилка при виконанні запиту: {e}")

def delete_all():
    try:
        result = db.cats.delete_many({})
        print(f"Видалено всіх котів: {result.deleted_count}.")
    except Exception as e:
        print(f"Виникла помилка при виконанні запиту: {e}")



insert_cats()
one_cat("Lama")
update_age("Barsik",5)
update_features("Barsik", ["ходить в капці", "ласкавий", "чорний"])
delete_one("Liza")
delete_all()