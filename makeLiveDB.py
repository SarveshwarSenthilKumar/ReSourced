
#Database Schema: Subject, Suggested Grades, Name of course, YouTube video link, creator

import sqlite3
import os

os.remove("live.db")
connection = sqlite3.connect("live.db")
crsr = connection.cursor()
crsr.execute("CREATE TABLE live (id INTEGER, subject, grades, title, videoLinks, creator, description, featured, endcard, endcardLink, PRIMARY KEY(id))")
connection.commit()
crsr.close()
connection.close()
test = open("live.db", "r")
test.close()
