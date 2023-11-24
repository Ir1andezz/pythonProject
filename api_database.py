from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def connect_to_database():
    return sqlite3.connect('TelephoneBook.db')


def create_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Friends (
        id INTEGER PRIMARY KEY,
        FIOFriends TEXT NOT NULL,
        email TEXT NULL,
        telephone TEXT NULL
    )
    ''')
    connection.commit()
    connection.close()


def insert_friend(name, email, telephone):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Friends (FIOFriends, email, telephone) VALUES (?, ?, ?)',
                   (name, email, telephone))

    connection.commit()
    connection.close()


def select_all_friends():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Friends')
    users = cursor.fetchall()

    for user in users:
        print(user)

    connection.close()


def select_friend_by_name(name):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT FIOFriends, email, telephone FROM Friends WHERE FIOFriends = ?', (name,))
    results = cursor.fetchall()

    for row in results:
        print(row)

    connection.close()


def update_email_by_name(name, new_email):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('UPDATE Friends SET email = ? WHERE FIOFriends = ?', (new_email, name))
    connection.commit()
    connection.close()


def delete_friend_by_name(name):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Friends WHERE FIOFriends = ?', (name,))
    connection.commit()
    connection.close()


def main():
    create_table()

    while True:
        print("\nВыберите действие:")
        print("1. Добавить нового друга")
        print("2. Просмотреть всех друзей")
        print("3. Поиск друга по имени")
        print("4. Обновить email друга")
        print("5. Удалить друга")
        print("0. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            name = input("Введите имя друга: ")
            email = input("Введите email друга: ")
            telephone = input("Введите телефон друга: ")
            insert_friend(name, email, telephone)
            print("Друг успешно добавлен!")

        elif choice == "2":
            print("\nСписок всех друзей:")
            select_all_friends()

        elif choice == "3":
            name = input("Введите имя друга для поиска: ")
            select_friend_by_name(name)

        elif choice == "4":
            name = input("Введите имя друга, чей email нужно обновить: ")
            new_email = input("Введите новый email: ")
            update_email_by_name(name, new_email)
            print("Email успешно обновлен!")

        elif choice == "5":
            name = input("Введите имя друга для удаления: ")
            delete_friend_by_name(name)
            print("Друг успешно удален!")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте еще раз.")



class FriendCreate(BaseModel):
    FIOFriends: str
    email: str = None
    telephone: str = None


@app.post("/friends/", response_model=FriendCreate)
async def create_friend(friend: FriendCreate):
    insert_friend(friend.FIOFriends, friend.email, friend.telephone)
    return friend


@app.get("/friends/")
async def read_friends():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT FIOFriends, email, telephone FROM Friends')
    friends = cursor.fetchall()

    connection.close()

    return {"friends": friends}


@app.get("/friends/{name}")
async def read_friend(name: str):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT FIOFriends, email, telephone FROM Friends WHERE FIOFriends = ?', (name,))
    results = cursor.fetchall()

    connection.close()

    if not results:
        raise HTTPException(status_code=404, detail="Друг не найден")

    return {"friend": results[0]}

if __name__ == "__main__":
    main()
