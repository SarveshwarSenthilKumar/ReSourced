from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session 
from datetime import datetime
from sql import *
from collections import defaultdict
from collections import Counter
import os
import random
from datetime import datetime
from datetime import timedelta
import random
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True 
app.config["SESSION_TYPE"] = "filesystem" 
app.config['UPLOAD_FOLDER'] = "uploads"

Session(app)
  
@app.route("/modcommands", methods=["GET", "POST"])
def modcommands():
  if not session.get("name"):
    return redirect("/")
  else:
    db = SQL("sqlite:///users.db")

    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))

    rank = results[0]["rank"] 

    if rank >= 15:
      if request.method == "GET":
        return render_template("command.html")
      elif request.method == "POST":
        return render_template("sentence.html", sentence="Command went through")
    else:
      return redirect("/")

    return render_template("sentence.html", sentence="Working on it!")

"""@app.route("/games", methods=["GET", "POST"])
def games():
  """

@app.route("/crew")
def crew():
  file = open("roles.txt", "r")

  sentenceList=[
    "Current Crew Members of ReSourced",
    " "
  ]
  

  for line in file:
    sentenceList.append(line.strip())

  return render_template("sentence.html", sentenceList=sentenceList)

@app.route("/badwriting", methods=["GET","POST"])
def badwriting():
  
  s = request.form.get("writing")
  s2 = ""
  
  num=1
  
  for i in s:
      if num % 2 == 0:
          s2+=i.upper()
      else:
          s2+=i.lower()
      if i.isalpha():
          num+=1

  sentence = "The string converted is '" + s2 + "'"
  return render_template("sentence.html", sentence=sentence)

@app.route("/confirm", methods=["GET","POST"])
def confirm():
  if not session.get("name"):
    return redirect("/")
  else:
    if request.method == "GET":
      return render_template("confirmscreen.html")
    elif request.method == "POST":
      action = request.form.get("action")

      if action == "delete":
        password = request.form.get("password")
        
        db = SQL("sqlite:///users.db")
        results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))

        user = results[0]

        if password == results[0]["password"]:
          db = SQL("sqlite:///users.db")
          db.execute("DELETE FROM users WHERE username = :username", username=session.get("name"))

          return redirect("/logout")
        else:
            return render_template("sentence.html", sentence="Incorrect Password! You may not delete your account!")

@app.route("/sentence")
def sentence():
  db=SQL("sqlite:///courses.db")
  results=db.execute("SELECT * FROM courses")
  return render_template("sentence.html", sentenceList=results)

@app.route("/addgrade", methods=["GET","POST"])
def addgrade():
  if not session.get("name"):
    return redirect("/")
  else:
    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
    
    if results[0]["rank"] < 7:
      return redirect("/")
    else:
      grades = request.form.getlist("grade")
      
      if grades == []:
        return render_template("sentence.html", sentence="You have not entered a valid subject!")

      db2 = SQL("sqlite:///courses.db")

      results = db2.execute("SELECT * FROM courses WHERE title = :title", title=request.form.get("name"))

      gradesStr = results[0]["grades"]
      changed = False

      for sub in grades:
        if sub not in gradesStr.split(", "):
          gradesStr+=", " + sub + ", "
          changed = True
      if changed == True:
        gradesStr = gradesStr[:-2]

      if changed == False:
        return render_template("sentence.html", sentence="This course already contains this grade!")

      db2.execute("UPDATE courses SET grades = :gradesStr WHERE title = :name", gradesStr=gradesStr, name=request.form.get("name"))

      return render_template("sentence.html", sentence="You have successfully changed the grades for this course!")

@app.route("/addsubject", methods=["GET","POST"])
def addsubject():
  if not session.get("name"):
    return redirect("/")
  else:
    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
    
    if results[0]["rank"] < 7:
      return redirect("/")
    else:
      subject = request.form.getlist("subject")
      
      if subject == []:
        return render_template("sentence.html", sentence="You have not entered a valid subject!")

      db2 = SQL("sqlite:///courses.db")

      results = db2.execute("SELECT * FROM courses WHERE title = :title", title=request.form.get("name"))

      subjectStr = results[0]["subject"]
      changed = False

      for sub in subject:
        if sub not in subjectStr:
          subjectStr+=", " + sub + ", "
          changed = True
      if changed == True:
        subjectStr = subjectStr[:-2]

      if changed == False:
        return render_template("sentence.html", sentence="This course already contains this subject!")

      db2.execute("UPDATE courses SET subject = :subjectStr WHERE title = :name", subjectStr=subjectStr, name=request.form.get("name"))

      return render_template("sentence.html", sentence="You have successfully changed the subjects for this course!")

@app.route("/addvideo", methods=["GET","POST"])
def addvideo():
  if not session.get("name"):
    return redirect("/")
  else:
    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
    
    if results[0]["rank"] < 7:
      return redirect("/")
    else:
      videoLink = request.form.get("link").strip()

      videoLinks = videoLink.split(" ")
  
      videoLink1 = ""
      for videoLink in videoLinks: 
        if "youtube" in videoLink:
          videoLink1 += videoLink.split("www.youtube.com/watch?v=")[1] + " "

        elif "." in videoLink:
          videoLink1 += videoLink + " "
      videoLink = videoLink1[:-1]

      if videoLink == "":
          return render_template("sentence.html", sentence="You have not entered a valid video link!")

      print(request.form.get("name"))

      db = SQL("sqlite:///courses.db")
      results = db.execute("SELECT * FROM courses WHERE title = :title", title=request.form.get("name"))
      currentLinks = results[0]["videoLinks"]
      newLinks = currentLinks + " " + videoLink

      db.execute("UPDATE courses SET videoLinks = :videoLinks WHERE title = :title", videoLinks=newLinks, title=request.form.get("name"))

      return render_template("sentence.html", sentence="You have successfully added this video link!")
    
""" #Testing
@app.route("/allusers", methods=["GET","POST"])
def allusers():

    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
    
    if results[0]["rank"] < 15:
      return redirect("/")
    else:
      
      results = db.execute("SELECT * FROM users")

      length = len(results)
      sentence = "There are " + str(length) + " users in total!"

      return render_template("searchusers.html", users=results, sentence=sentence)
"""

@app.route("/searchuser", methods=["GET","POST"])
def searchusers():
  if not session.get("name"):
    return redirect("/")
  else:
    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
    
    if results[0]["rank"] < 15:
      return redirect("/")
    else:
      username = request.form.get("username")
      results = db.execute("SELECT * FROM users WHERE username = :username", username=username)

      return render_template("searchusers.html", users=results)

@app.route("/changelink", methods=["GET","POST"])
def changelink():
  if not session.get("name"):
    return redirect("/")
  else:
    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
    
    if results[0]["rank"] < 7:
      return redirect("/")
    else:
      name = request.form.get("name")
      link = request.form.get("link")

      db = SQL("sqlite:///live.db")

      db.execute("UPDATE live SET videoLinks = :link  WHERE title = :title", link=link, title=name)

      return render_template("sentence.html", sentence="The link for this course has been changed!")

      return render_template("sentence.html", sentence="working on it")

@app.route("/")
def index():
  if not session.get("name"):
    return render_template("login.html")
  else:

    db = SQL("sqlite:///users.db")
    
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))

    courses=[]

    if results[0]["coursesInProgress"] == None:
      coursesInProgress = []
    elif "," not in results[0]["coursesInProgress"]:
      coursesInProgress = [results[0]["coursesInProgress"]]
    else:
      coursesInProgress = results[0]["coursesInProgress"].split(",")


    for i in coursesInProgress:
      if i != "":
        db = SQL("sqlite:///courses.db")
        result = db.execute("SELECT * FROM courses WHERE id = :id", id=i)
        
        if " " in result[0]["videoLinks"]:
          videoLinks = result[0]["videoLinks"].split()
          firstLink = videoLinks[0]
          quantity = "1/"+str(len(videoLinks))
        else:
          firstLink = result[0]["videoLinks"]
          quantity = "1/1"
  
        result[0]["firstLink"] = firstLink
        result[0]["quantity"] = quantity
  
        courses.append(result[0])
    
    return render_template("index.html", rank=results[0]["rank"], courses=courses)

@app.route("/viewcompleted")
def viewcompleted():
  db = SQL("sqlite:///users.db")
  users = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))

  completedResults=[]
  
  coursesCompleted = users[0]["coursesCompleted"]
  
  if coursesCompleted == None:
    coursesCompleted = []
  elif "," not in coursesCompleted:
    coursesCompleted = [coursesCompleted]
  else:
    coursesCompleted = coursesCompleted.split(",")

  for c in coursesCompleted:
    db = SQL("sqlite:///courses.db")
    print(c)
    results = db.execute("SELECT * FROM courses WHERE id = :id", id=c)[0]
    if " " in results["videoLinks"]:
      videoLinks = results["videoLinks"].split()
      firstLink = videoLinks[0]
      quantity = "1/"+str(len(videoLinks))
    else:
      firstLink = results["videoLinks"]
      quantity = "1/1"
    
      results["firstLink"] = firstLink
      results["quantity"] = quantity
    completedResults.append(results)

  return render_template("displaycourses.html", courses=completedResults, sentence="You have completed the following courses")

@app.route("/progress")
def progress():

  db = SQL("sqlite:///users.db")
  users = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
  
  coursesCompleted = users[0]["coursesCompleted"]
  
  if coursesCompleted == None:
    coursesCompleted = []
  elif "," not in coursesCompleted:
    coursesCompleted = [coursesCompleted]
  else:
    coursesCompleted = coursesCompleted.split(",")

  subjectsList = []
  gradesList = []

  for c in coursesCompleted:
    db = SQL("sqlite:///courses.db")
    results = db.execute("SELECT * FROM courses WHERE id = :id", id=c)
    grades = results[0]["grades"]
    subjects = results[0]["subject"]

    if grades == None:
      grades = []
    elif "," not in grades:
      grades = [grades]
    else:
      grades = grades.split(",")

    if subjects == None:
      subjects = []
    elif "," not in subjects:
      subjects = [subjects]
    else:
      subjects = subjects.split(",")

    for g in grades:
      gradesList.append(g)

    for s in subjects:
      subjectsList.append(s)
      
  subjects = defaultdict(int)

  for i in subjectsList:
      i=i.lower()
      subjects[i]+=1

  keys=[]
  values=[]
  k = Counter(subjects)

  subjects = k.most_common(10)
  subjects=subjects[::-1]

  for key, value in subjects:
    keys.append(key)
    values.append(value)

  keys=keys[:10]
  values=values[:10]

  grades = defaultdict(int)

  for i in gradesList:
      i=i.lower()
      grades[i]+=1

  keys2=[]
  values2=[]
  k = Counter(grades)

  grades = k.most_common(10)
  grades=grades[::-1]

  for key, value in grades:
    keys2.append(key)
    values2.append(value)

  keys2=keys2[:10]
  values2=values2[:10]

  courseResults = []
  
  for k in keys:
    db = SQL("sqlite:///courses.db")
    courses = db.execute("SELECT * FROM courses")

    if k == keys[-1]:
      totalCoursesDenominator = len(courses)

    for cour in courses:
      if k not in cour["subject"].lower():
        courses.remove(cour)

    coursesString = ""


    for cour in courses:
      if cour["grades"] == None:
        courseGrades = []
      elif "," not in cour["grades"]:
        courseGrades = [cour["grades"]]
      else:
        courseGrades = cour["grades"].split(",")
      if keys2[0] in courseGrades:
        coursesString += str(cour["id"]) + ","
    coursesString = coursesString[:-1]    
    subjectStringToDisplay = "Grade " + str(keys2[0]) + " " + k.upper()
  
    if coursesString == None:
      courses = []
    elif "," not in coursesString:
      courses = [courses]
    else:
      courses = coursesString.split(",")

    db = SQL("sqlite:///users.db")
    coursesCompleted = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))[0]["coursesCompleted"]
  
    numerator = 0
    denominator = len(courses)
    fraction = ""

    if k == keys[-1]:
      if coursesCompleted == None:
        completedList = []
      elif "," not in coursesCompleted:
        completedList = [coursesCompleted]
      else:
        completedList = coursesCompleted.split(",")
      totalCoursesNumerator = len(completedList)
      totalCoursesFraction = str(totalCoursesNumerator) + "/" + str(totalCoursesDenominator)
      totalCoursesWidth = int(100/totalCoursesDenominator)
      totalCoursesDrawList = []
    
      for i in range(totalCoursesNumerator):
        totalCoursesDrawList.append("#")
      for i in range(totalCoursesDenominator-totalCoursesNumerator):
        totalCoursesDrawList.append("-")
    
    for course in coursesCompleted:
      if course in courses:
        numerator += 1
    
    width = int(100/denominator)
    
    drawList = []
    
    for i in range(numerator):
      drawList.append("#")
    for i in range(denominator-numerator):
      drawList.append("-")
    
    fraction = str(numerator) + "/" + str(denominator)
  
    courseToBeAdded = {}

    courseToBeAdded["subject"] = subjectStringToDisplay
    courseToBeAdded["width"] = width
    courseToBeAdded["fraction"] = fraction + " courses completed!"
    courseToBeAdded["drawList"] = drawList

    courseResults.append(courseToBeAdded)

    if k == keys[-1]:
      courseToBeAdded = {}
      courseToBeAdded["subject"] = "Total ReSourced Courses"
      courseToBeAdded["width"] = totalCoursesWidth
      courseToBeAdded["fraction"] = totalCoursesFraction + " courses completed!"
      courseToBeAdded["drawList"] = totalCoursesDrawList

      courseResults.append(courseToBeAdded)

  return render_template("progress.html", courseResults=courseResults)
  
@app.route('/home')
def index2():
    return redirect("https://resourced.repl.co/")

@app.route("/searchcourses", methods=["GET", "POST"])
def searchcourses():
  if not session.get("name"):
    return redirect("/")
  if request.method == "POST":

    subjects = request.form.getlist("subject")
    grade = str(request.form.get("grade"))
    
    db=SQL("sqlite:///courses.db")
    results = db.execute("SELECT * FROM courses")
    searchResults = []

    db2 = SQL("sqlite:///users.db")
    user = db2.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))[0]

    workingOn = user["coursesInProgress"]
    completed = user["coursesCompleted"]

    if workingOn == None:
      workingOn = []
    elif "," not in workingOn:
      workingOn = [workingOn]
    else:
      workingOn = workingOn.split(",")

    if completed == None:
      completed = []
    elif "," not in completed:
      completed = [completed]
    else:
      completed = completed.split(",")
    if len(completed) > 0:
      if completed[-1] == "":
        completed = completed[:-1]
    if len(workingOn) > 0:
      if workingOn[-1] == "":
        workingOn = workingOn[:-1]

    for i in results:
      for subject in subjects:
        if subject.strip() in i["subject"].strip() and grade in i["grades"]:
          if str(i["id"]) not in workingOn:
            if str(i["id"]) not in completed:

              if " " in i["videoLinks"]:
                videoLinks = i["videoLinks"].split()
                firstLink = videoLinks[0]
                quantity = "1/"+str(len(videoLinks))
              else:
                firstLink = i["videoLinks"]
                quantity = "1/1"
    
              i["firstLink"] = firstLink
              i["quantity"] = quantity
              
              searchResults.append(i)

    return render_template("displaycourses.html", courses=searchResults)
  

@app.route("/deleteacc", methods=["GET", "POST"])
def deleteacc():
  if not session.get("name"):
    return redirect("/")
  else:
    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))

    if int(results[0]["rank"]) < 10:
      return redirect("/")
    else:
      username = request.form.get("username")

      db = SQL("sqlite:///users.db")

      results2 = db.execute("SELECT * FROM users WHERE username = :username", username=username)

      if int(results2[0]["rank"]) >= int(results[0]["rank"]):
        return render_template("sentence.html", sentence="You may not delete this account as it is rated higher than you!")
      db.execute("DELETE FROM users WHERE username = :username", username=username)

      return render_template("sentence.html", sentence="This user has been deleted")

@app.route("/login", methods=["GET", "POST"])
def login():
  if session.get("name"):
    return redirect("/")
  else:
    if request.method == "GET":
      return render_template("login.html")
    elif request.method == "POST":
      username = request.form.get("username").lower().strip()
      password = request.form.get("password").lower().strip()
      
      db = SQL("sqlite:///users.db")
      results = db.execute("SELECT * FROM users WHERE username = :username", username=username)
      if len(results) == 0:
        return render_template("login.html", sentence="Incorrect Username!")
      elif password != results[0]["password"]:
        return render_template("login.html", sentence="Incorrect Password!")

      elif password == results[0]["password"]:
        session["name"] = username
        session["rank"] = results[0]["rank"]
        return redirect('/')

@app.route("/signup", methods=["GET","POST"])
def signup():
  if session.get("name"):
    return redirect("/")
  if request.method == "GET":
    return render_template("login.html")
  elif request.method == "POST":
    username = request.form.get("username").lower().strip()
    password = request.form.get("password").lower().strip()

    if len(username) > 32 or len(username) < 8:
        return render_template("login.html", sentence="You have to register a username between the length of 8 and 32 characters.")

    allowedChars = "abcdefghijklmnopqrstuvwxyz1234567890"

    for letter in username:
      if letter not in allowedChars:
        return render_template("login.html", sentence="You cannot have any special characters in your name.")
          
    if username == "guest":
      return render_template("You may not impersonate a guest!")

    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=username)
    
    if len(results) == 0:
      db.execute("INSERT INTO users (username, password, rank) VALUES (?,?,?)", username, password, 1)
      session["name"] = username
      session["rank"] = 1
      return render_template("sentence.html", sentence="You have successfully created a new account!")
    else:
      return render_template("login.html", sentence="Sorry, this username is already taken, please try another one.")

@app.route("/logout")
def logout():
  if not session.get("name"):
    return redirect("/")
  else:
    session["name"] = None
    session["rank"] = None

    return redirect("/")

@app.route("/guest")
def guest():
  session["name"] = "guest"
  session["rank"] = 1

  return redirect("/")

@app.route("/changerank", methods=["GET", "POST"])
def changerank():
  if not session.get("name"):
    return redirect("/")
  else:
    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))

    if int(results[0]["rank"]) < 10:
      return redirect("/")
    else:
      username = request.form.get("username").lower().strip()
      rank = request.form.get("rank")

      if int(rank) >= int(results[0]["rank"]):
        return render_template("sentence.html", sentence="This rank is higher than your rank! You do not have the permission to do this!")

      if username == session.get("name"):
        return render_template("You may not change your own rank!")

      db = SQL("sqlite:///users.db")

      rankOfOther = db.execute("SELECT * FROM users WHERE username = :username", username=username)

      if int(rankOfOther[0]["rank"]) >= int(results[0]["rank"]):
        return render_template("sentence.html", sentence="You cannot change the rank of someone ranked equally or higher than you!")

      db.execute("UPDATE users SET rank = :rank WHERE username = :username", rank=int(rank), username=username)

      sentence= "The rank of " + username + " has been changed to " + rank

      return render_template("sentence.html", sentence=sentence)


@app.route("/changepassword", methods=["GET", "POST"])
def changepassword():
  if not session.get("name"):
    return redirect("/")
  else:
    newpassword = request.form.get("password").lower().strip()
    oldpassword = request.form.get("oldpass").lower().strip()

    db = SQL("sqlite:///users.db")
    results=db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))

    if oldpassword == results[0]["password"]:
      db.execute("UPDATE users SET password = :password WHERE username = :username", password=newpassword, username=session.get("name"))
      return render_template("sentence.html", sentence="Your password has been changed!")
    else:
      return render_template("sentence.html", sentence="Incorrect Password!")

@app.route("/unfeaturecourse", methods=["GET", "POST"])
def unfeaturecourse():
  if not session.get("name"):
    return redirect("/")
  else:
  
    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
    
    if results[0]["rank"] < 7:
      return redirect("/")
    else:
      name = request.form.get("name")

      db = SQL("sqlite:///live.db")

      db.execute("UPDATE live SET featured = NULL  WHERE title = :title", title=name)

      return render_template("sentence.html", sentence="This course has been unfeatured!")

@app.route("/deletecourse", methods=["GET", "POST"])
def deletecourse():
  if not session.get("name"):
    return redirect("/")
  else:
  
    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
    
    if results[0]["rank"] < 7:
      return redirect("/")
    else:
      name = request.form.get("name")

      db = SQL("sqlite:///courses.db")

      course = db.execute("SELECT * FROM courses WHERE title = :title", title=name)[0]

      courseID = str(course["id"])

      db2 = SQL("sqlite:///users.db")

      users = db2.execute("SELECT * FROM users")

      for user in users:
        workingOn = user["coursesInProgress"]
        finished = user["coursesCompleted"]

        if workingOn == None:
          workingOn = []
        elif "," not in workingOn:
          workingOn = [workingOn]
        else:
          workingOn = workingOn.split(",")
    
        if finished == None:
          finished = []
        elif "," not in finished:
          finished = [finished]
        else:
          finished = finished.split(",")

        if courseID in workingOn:
          workingOn.remove(course)
          workStr = ""
          for i in workingOn:
            workStr += i +","
          workStr = workStr[:-1]
          db = SQL("sqlite:///users.db")
          db.execute("UPDATE users SET coursesInProgress = :courses WHERE username = :username", courses=workStr, username=user["username"])
          
        if courseID in finished:
          finished.remove(course)
          workStr = ""
          for i in finished:
            workStr += i +","
          workStr = workStr[:-1]
          db = SQL("sqlite:///users.db")
          db.execute("UPDATE users SET coursesCompleted = :courses WHERE username = :username", courses=workStr, username=user["username"])
              
      db.execute("DELETE FROM courses WHERE title = :title", title=name)

      return render_template("sentence.html", sentence="The course has been deleted!")
      

@app.route("/createcourse", methods=["GET", "POST"])
def createCourse():
  if not session.get("name"):
    return redirect("/")
  else:
  
    db = SQL("sqlite:///users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))

    if request.method == "GET":
      if results[0]["rank"] < 7:
        return redirect("/")
      else:
        return render_template("createcourse.html")
    elif request.method == "POST":
      file = request.files.get("file")
      if file:
        filename=secure_filename(file.filename)[:-4]
        file.save(filename)
        doc = aw.Document(file.filename)
        doc.save(filename+".html")        
      subject = request.form.getlist("subject")
      grades = request.form.getlist("grade")
      title = request.form.get("title").strip()
      videoLink = request.form.get("link").strip()
      creator = session.get("name")
      live = request.form.get("live")

      description = request.form.get("description").strip()
      endcard = request.form.get("endcard").strip()
      videoLinks = videoLink.split(" ")
  
      videoLink1 = ""
      for videoLink in videoLinks: 
        if "youtube" in videoLink or "youtu" in videoLink:
          videoLink1 += videoLink.split("www.youtube.com/watch?v=")[1] + " "

        elif "." in videoLink:
          videoLink1 += videoLink + " "
      videoLink = videoLink1[:-1]

      db = SQL("sqlite:///courses.db")
      results = db.execute("SELECT * FROM courses WHERE title = :title", title=title)

      db2 = SQL("sqlite:///live.db")
      resultsDB2 = db2.execute("SELECT * FROM live WHERE title = :title", title=title)

      if len(results) > 0 or len(resultsDB2) > 0:
        return render_template("sentence.html", sentence="There is already an existing course with this title!")

      if subject == "":
        return render_template("sentence.html", sentence="You have not entered a valid subject!")
      if grades == "":
        return render_template("sentence.html", sentence="You have not entered a valid grade!")
      if title == "":
        return render_template("sentence.html", sentence="You have not entered a valid title!")
      if creator == "":
        return render_template("sentence.html", sentence="You have not entered a valid creator!")
      if description == "":
        return render_template("sentence.html", sentence="You have not entered a valid description!")
      if endcard == "":
        return render_template("sentence.html", sentence="You have not entered a valid endcard!")

      subjectStr = ""
      gradesStr = ""

      for sub in subject:
        subjectStr+=sub+", "
      subjectStr = subjectStr[:-2]

      for grade in grades:
        gradesStr+=grade+", "
      gradesStr = gradesStr[:-2]

      if live == "live":
        db = SQL("sqlite:///live.db")
        db.execute("INSERT INTO live (subject, grades, title, videoLinks, creator, description, featured, endcard) VALUES (?,?,?,?,?,?,?,?)", subjectStr, gradesStr, title, videoLink, creator, description,"yes", endcard)
        id = db.execute("SELECT * FROM live WHEre title = :title", title=title)[0]["id"]
        endcardLink = "https://App.resourced.repl.co/endcard?id="+str(id)
        db = SQL("sqlite:///live.db")
        db.execute("UPDATE live SET endcardLink = :endcardLink WHERE id = :id", endcardLink=endcardLink, id=id)
      else:
        if file:
          endcardLink=""
          db = SQL("sqlite:///courses.db")
          db.execute("INSERT INTO courses (subject, grades, title, videoLinks, creator, description, endcard, endcardLink, pdfLink) VALUES (?,?,?,?,?,?,?,?,?)", subjectStr, gradesStr, title, videoLink, creator, description, endcard, endcardLink, filename)
          id = db.execute("SELECT * FROM courses WHEre title = :title", title=title)[0]["id"]
          endcardLink = "https://App.resourced.repl.co/endcard?id="+str(id)
          db = SQL("sqlite:///courses.db")
          db.execute("UPDATE courses SET endcardLink = :endcardLink WHERE id = :id", endcardLink=endcardLink, id=id)
        else:
          endcardLink=""
          db = SQL("sqlite:///courses.db")
          db.execute("INSERT INTO courses (subject, grades, title, videoLinks, creator, description, endcard, endcardLink) VALUES (?,?,?,?,?,?,?,?)", subjectStr, gradesStr, title, videoLink, creator, description, endcard, endcardLink)
          id = db.execute("SELECT * FROM courses WHEre title = :title", title=title)[0]["id"]
          endcardLink = "https://App.resourced.repl.co/endcard?id="+str(id)
          db = SQL("sqlite:///courses.db")
          db.execute("UPDATE courses SET endcardLink = :endcardLink WHERE id = :id", endcardLink=endcardLink, id=id)

      sentence = "You have successfully uploaded " + title
      
      return render_template("sentence.html", sentence=sentence)

@app.route("/endcard", methods=["GET","POST"])
def endcard():
  id = request.args.get("id")

  db = SQL("sqlite:///courses.db")
  results = db.execute("SELECT * FROM courses WHERE id = :id", id=id)
  print(results)

  endcard = results[0]["endcard"]
  print(endcard)
  title = results[0]["title"]

  db = SQL("sqlite:///users.db")
  user = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
  
  currentWOstr = user[0]["coursesInProgress"]
  currentFinStr = user[0]["coursesCompleted"]

  workingOn = False
  finished = False

  if currentWOstr != None:
    if "," not in currentWOstr:
      if str(id) == str(currentWOstr):
        workingOn = True
    elif str(id) in currentWOstr.split(","):
      workingOn = True
      
  if currentFinStr != None:
    if "," not in currentFinStr:
      if str(id) == str(currentFinStr):
        finished = True
    elif str(id) in currentFinStr.split(","):
      finished = True

  return render_template("endcard.html", id=id, endcard=endcard, title=title, finished=finished, workingOn=workingOn)

@app.route("/currentcourses")
def currentcourses():
  db = SQL("sqlite:///courses.db")
  results=db.execute("SELECT * FROM courses")
  return render_template("sentence.html", sentenceList=results)

@app.route("/liveevents")
def liveevents():
  db = SQL("sqlite:///live.db")
  results = db.execute("SELECT * FROM live WHERE featured = :featured", featured="yes")
  searchResults=[]
  for i in results:
    if i["videoLinks"] != None:
      if " " in i["videoLinks"]:
        videoLinks = i["videoLinks"].split()
        firstLink = videoLinks[0]
        quantity = "1/"+str(len(videoLinks))
      else:
        firstLink = i["videoLinks"]
        quantity = "1/1"
    else:
      firstLink = "There is no link for this live course available yet!"
      quantity = 0
    
    i["firstLink"] = firstLink
    i["quantity"] = quantity
              
    searchResults.append(i)

  return render_template("displaycourses.html", courses=searchResults, live=True)

@app.route("/workon", methods=["GET", "POST"])
def workon():
  course = request.args.get("course")

  db = SQL("sqlite:///users.db")
  results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
  currentWork = results[0]["coursesInProgress"]
  if currentWork == None:
    currentWork = course
  elif course in currentWork.split():
    return render_template("sentence.html", sentence="You have already set the course of this course to Working On!")
  else:
    currentWork += "," + course

  db.execute("UPDATE users SET coursesInProgress = :courses WHERE username = :username", courses=currentWork, username=session.get("name"))

  return render_template("sentence.html", sentence="You have successfully set this course's status as Working On!")

@app.route("/finishcourse", methods=["GET", "POST"])
def finishcourse():
  course = str(request.args.get("course"))

  db = SQL("sqlite:///users.db")
  results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
  currentWork = results[0]["coursesInProgress"]
  if currentWork == None:
    currentWork = []
  elif "," not in currentWork:
    currentWork = [str(currentWork)]
  else:
    currentWork = currentWork.split(",")

  if course in currentWork:
    currentWork.remove(course)
    workStr = ""
    for i in currentWork:
      workStr += i +","
    workStr = workStr[:-1]
    db = SQL("sqlite:///users.db")
    db.execute("UPDATE users SET coursesInProgress = :courses WHERE username = :username", courses=workStr, username=session.get("name"))

  db = SQL("sqlite:///users.db")
  results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))

  currentFinished = results[0]["coursesCompleted"]

  if currentFinished == None:
    currentFinished = course
  elif course in currentFinished.split(","):
    return render_template("sentence.html", sentence="You have already finished this course!")
  else:
    currentFinished += "," + course

  db.execute("UPDATE users SET coursesCompleted = :currentFinished WHERE username = :username", currentFinished=currentFinished, username=session.get("name"))

  return render_template("sentence.html", sentence="You have successfully set this course's status as Finished!")

@app.route("/stopworkingon")
def stopworkingon():
  course = str(request.args.get("course"))

  db = SQL("sqlite:///users.db")
  results = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
  currentWork = results[0]["coursesInProgress"]
  if currentWork == None:
    currentWork = []
  elif "," not in currentWork:
    currentWork = [str(currentWork)]
  else:
    currentWork = currentWork.split(",")

  if course in currentWork:
    currentWork.remove(course)
    workStr = ""
    for i in currentWork:
      workStr += i +","
    workStr = workStr[:-1]
    db = SQL("sqlite:///users.db")
    db.execute("UPDATE users SET coursesInProgress = :courses WHERE username = :username", courses=currentWork, username=session.get("name"))
    return render_template("sentence.html", sentence="You have stopped working on this course!")
  else:
    return render_template("sentence.html", sentence="You never set the status of this course as Working On!")

@app.route("/itempage")
def itempage():
  course = request.args.get("course")

  db = SQL("sqlite:///courses.db")
  results = db.execute("SELECT * FROM courses WHERE id = :id", id=course)
  result = results[0]

  workingOn = False
  finished = False

  db = SQL("sqlite:///users.db")
  user = db.execute("SELECT * FROM users WHERE username = :username", username=session.get("name"))
  
  currentWOstr = user[0]["coursesInProgress"]
  currentFinStr = user[0]["coursesCompleted"]

  if currentWOstr != None:
    if "," not in currentWOstr:
      if str(course) == str(currentWOstr):
        workingOn = True
    elif str(course) in currentWOstr.split(","):
      workingOn = True
      
  if currentFinStr != None:
    if "," not in currentFinStr:
      if str(course) == str(currentFinStr):
        finished = True
    elif str(course) in currentFinStr.split(","):
      finished = True

  if " " in result["videoLinks"]:
    videoLinks = result["videoLinks"].split()
    quantity = str(len(videoLinks))
  else:
    videoLinks = [result["videoLinks"]]
    quantity = "1"

  result["quantity"] = quantity

  return render_template("itempage.html", course=result, videoLinks=videoLinks, finished=finished, workingOn=workingOn)
  
@app.route("/suggest", methods=["GET","POST"])
def suggestions():
  if not session.get("name"):
    return redirect("/")
  else:
      global email

      description=request.form.get("description")
      description=description.strip()
      email=request.form.get("email")
      email=email.strip()

      if description == "":
        return render_template("sentence.html", sentence="You haven't entered a valid suggestion!")
      if email == "":
        return render_template("sentence.html", sentence="You haven't entered a valid email address!")
      if "@" not in email:
        return render_template("sentence.html", sentence="You haven't entered a valid email address!")
      """
      port = 587  # For SSL
      password = os.getenv("emailPassword")
      print(password)
      
      # Create a secure SSL context
      context = ssl.create_default_context()
      
      with smtplib.SMTP_SSL("smtp-mail.outlook.com.", port, context=context) as server:
        server.login("officialresourced@outlook.com", password)
        sender_email = "officialresourced@outlook.com"
        receiver_email = "officialresourced@outlook.com"
        message = "New Suggestion/Bug Report: " + description
        server.sendmail(sender_email, receiver_email, message)"""

      tz_NY = pytz.timezone('America/New_York')
      now=datetime.now(tz_NY)
      OTime= now.strftime("%d/%m/%y %H:%M:%S")
      file = open("suggestions.txt", "a")
      file.write("\n" + email + " at " + OTime + " - " + description + "\n")

      return render_template("sentence.html", sentence="Thank you for the amazing suggestion!")

app.run(host='0.0.0.0', port=81)
