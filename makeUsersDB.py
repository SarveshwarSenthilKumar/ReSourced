import sqlite3
import os

os.remove("users.db")

connection = sqlite3.connect("users.db")
crsr = connection.cursor()
crsr.execute("CREATE TABLE users (id INTEGER, username, password, rank, coursesCompleted, coursesInProgress, PRIMARY KEY(id))")
connection.commit()
crsr.close()
connection.close()
test = open("users.db", "r")
test.close()

"""
db = SQL("sqlite:///users.db")
    db.execute("UPDATE users SET rank = :rank WHERE username = :username", rank=10, username="sarveshwarsenthilkumar")"""