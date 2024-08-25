
#our first course

import sqlite3
import os
from sql import *

db = SQL("sqlite:///users.db")
db.execute("UPDATE users SET coursesCompleted = NULL, coursesInProgress = NULL WHERE username IS NOT NULL")
os.remove("courses.db")
connection = sqlite3.connect("courses.db")
crsr = connection.cursor()
crsr.execute("CREATE TABLE courses (id INTEGER, subject, grades, title, videoLinks, creator, description, endcard, endcardLink, pdfLink, PRIMARY KEY(id))")
connection.commit()
crsr.close()
connection.close()
test = open("courses.db", "r")
test.close()
