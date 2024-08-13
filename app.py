import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
print("test")

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")
""""
# to work in any folder:
# Find the directory where the app.py is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Create the full path for the database
db_path = os.path.join(basedir, 'database.db')

# Configure CS50 Library to use SQLite database with the full path
db = SQL(f"sqlite:///{db_path}")
"""

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# index - homepage
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show all workouts"""
    if request.method == "POST":
        if 'workout' in request.form:
            # if workout button pushed
            session["workoutId"] = request.form.get("workout")
            return redirect("/workout")

        elif 'editWorkout' in request.form:
            # if editWorkout button pushed
            session["workoutId"] = request.form.get("editWorkout")
            return redirect("/editWorkout")

        elif 'workoutGraph' in request.form:
            # if workoutGraph button pushed
            session["workoutId"] = request.form.get("workoutGraph")
            #return render_template("workoutGraph.html")
            return redirect("/workoutGraph")
    else:
        userId = session["user_id"]

        # load all workouts from DB
        workouts = db.execute("SELECT * FROM programs WHERE user_id = ?", userId)

        return render_template("index.html", workouts=workouts)


# add workout
@app.route("/addWorkout", methods=["GET", "POST"])
@login_required
def addWorkout():
    """Add workout"""
    if request.method == "POST":
        # get variables from HTML
        name = request.form.get("workoutName")
        userId = session["user_id"]

        # add new workout name to DB
        db.execute("INSERT INTO programs (user_id, program_name) VALUES (?, ?)", userId, name)

        # get new workoutId
        workoutId = db.execute("SELECT program_id FROM programs WHERE user_id = ? ORDER BY program_id DESC", userId)
        if workoutId is None:
            return redirect("/")
        session["workoutId"] = workoutId[0]["program_id"]

        return render_template("addExercise.html")
    else:
        return render_template("addWorkout.html")


# add exercise
@app.route("/addExercise", methods=["GET", "POST"])
@login_required
def addExercise():
    """Add workout"""
    if request.method == "POST":
        # get variables from HTML
        exercise = request.form.get("exercise")
        sets = request.form.get("sets")
        reps = request.form.get("reps")
        startWeight = request.form.get("startWeight")
        progressionWeight = request.form.get("addWeight")

        userId = session["user_id"]
        workoutId = session["workoutId"]


        # add new exercise to DB
        db.execute("INSERT INTO exercises (program_id, exercise_name, sets, reps, start_weight, progression_weight) VALUES (?, ?, ?, ?, ?, ?)", workoutId, exercise, sets, reps, startWeight, progressionWeight)


        return redirect("/")
    else:
        return render_template("addWorkout.html")


@app.route("/workout", methods=["GET", "POST"])
@login_required
def workout():
    """Show specifik workout with all exercises"""
    if request.method == "POST":
        if 'submitWorkout' in request.form:
            # submit workout into exercise_weights
            # if all sets in an exercise have correct numbers of reps - increase weight
            # if not - insert same data as previous workout
            workoutId = session["workoutId"]
            userId = session["user_id"]

            # Extracting exercise data from the form
            setsAndReps = []

            # for every input extract info and save it in a tuple
            for key, value in request.form.items(): # key / value: exercise_1_set_2
                if key.startswith('exercise_'):
                    parts = key.split("_")
                    # get info from splittet key
                    exerciseId = int(parts[1])
                    setNumber = int(parts[3])
                    reps = int(value)
                    setsAndReps.append((exerciseId, setNumber, reps))

            # group sets by exerciseId
            exerciseGroups = {}
            for exerciseId, setNumber, reps in setsAndReps:
                if exerciseId not in exerciseGroups:
                    exerciseGroups[exerciseId] = []
                exerciseGroups[exerciseId].append(reps)

            currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
            currentTime = datetime.datetime.now()

            # Process each exercise group
            for exerciseId, repsList in exerciseGroups.items():
                # get required reps for the specifik exercise
                requiredReps = db.execute("SELECT reps FROM exercises WHERE exercise_id = ?", exerciseId)[0]["reps"]

                # check if all reps is above the required
                allSetsMeetReps = all(reps >= requiredReps for reps in repsList) # help from ChatGPT

                # get number of reps from DB with current exerciseID
                exerciseInfo = db.execute("SELECT * FROM exercises WHERE exercise_id = ?", exerciseId)[0]
                currentWeight = exerciseInfo["start_weight"]
                progressionWeight = exerciseInfo["progression_weight"]

                # make an combined string with all reps ex: 1/2/5/5/
                allRepsInString = ""
                print(f"repsList: {repsList}")
                for rep in repsList:
                    if allRepsInString:
                        allRepsInString += "/"
                    allRepsInString += str(rep)
                print(f"allRepsInString: {allRepsInString}")
                # if true
                if allSetsMeetReps:
                    newWeight = currentWeight + progressionWeight
                    # insert into exercise_weights with new weight, time and reps for each set
                    db.execute("INSERT INTO exercise_weights (exercise_id, weight, time, reps) VALUES(?, ?, ?, ?)", exerciseId, currentWeight, currentTime, allRepsInString)
                    
                    # update exercises with new weight and reset reps for each sets
                    db.execute("UPDATE exercises SET start_weight = ?, previous_reps = '' WHERE exercise_id = ?", newWeight, exerciseId)
                else:
                    # insert into exercise_weights with current weight, time and reps for each set
                    db.execute("INSERT INTO exercise_weights (exercise_id, weight, time, reps) VALUES(?, ?, ?, ?)", exerciseId, currentWeight, currentTime, allRepsInString)

                    # update exercise with previous reps for each set
                    db.execute("UPDATE exercises SET previous_reps = ? WHERE exercise_id = ?", allRepsInString, exerciseId)

            return redirect("/")

    else:
        userId = session["user_id"]
        workoutId = session["workoutId"]

        # load all exercises from DB
        exercises = db.execute("SELECT * FROM exercises WHERE program_id = ?", workoutId)
        
        # check if dict is empty
        if exercises is None:
            return redirect("/")

        # find max sets to make enough columns
        # find reps from previous workout
        maxSet = 0
        for ex in exercises:
            # find max sets
            if ex["sets"] > maxSet:
                maxSet = ex["sets"]

            if ex["previous_reps"]:
                ex["previous_reps"] = ex["previous_reps"].split("/")
                print(ex["previous_reps"])
            else:
                ex["previous_reps"] = []


        return render_template("workout.html", exercises=exercises, maxSet=maxSet)


@app.route("/workoutGraph", methods=["GET", "POST"])
@login_required
def workoutGraph():
    # get data from DB
    programData = db.execute("SELECT e.exercise_name, ew. * FROM exercises e JOIN exercise_weights ew ON e.exercise_id = ew.exercise_id WHERE e.program_id = ? ORDER BY exercise_id, time", session["workoutId"])

    # if no workouts done - DB returns an empty list
    if not programData:
            return redirect("/")

    exercises = {}
    for row in programData:
        exercise_name = row['exercise_name']
        # if name not in exercise_name
        if exercise_name not in exercises:
            # add labels and weights
            exercises[exercise_name] = {
                'labels': [],
                'weights': []
            }
        exercises[exercise_name]['labels'].append(row['time'])
        exercises[exercise_name]['weights'].append(row['weight'])

        # Get the labels from the first exercise
        first_exercise_labels = list(exercises.values())[0]['labels']

    return render_template("workoutGraph.html", exercises=exercises, labels=first_exercise_labels)


# editWorkout
@app.route("/editWorkout", methods=["GET", "POST"])
@login_required
def editWorkout():
        if request.method == "POST":
            # if addExercise button pressed
            if 'addExercise' in request.form:
                return render_template("addExercise.html")
            else:
                # get variables from HTML
                # first get exerciseId
                exerciseId = request.form.get("saveWorkout")
                # use exerciseId to get the specific name, sets etc.
                name = request.form.get(f"name_{exerciseId}")
                sets = request.form.get(f"sets_{exerciseId}")
                reps = request.form.get(f"reps_{exerciseId}")
                weight = request.form.get(f"weight_{exerciseId}")
                progressionWeight = request.form.get(f"progression_weight_{exerciseId}")

                # update DB with new values
                db.execute("UPDATE exercises SET exercise_name=?, sets=?, reps=?, start_weight=?, progression_weight=? WHERE exercise_id=?", name, sets, reps, weight, progressionWeight, exerciseId)

                return redirect("/editWorkout")
        else:
            userId = session["user_id"]
            workoutId = session["workoutId"]

            # load all exercises from DB
            exercises = db.execute("SELECT * FROM exercises WHERE program_id = ?", workoutId)

            if exercises is None:
                return redirect("/")
            return render_template("editWorkout.html", exercises=exercises)

# deleteWorkout
@app.route("/deleteWorkout", methods=["GET", "POST"])
@login_required
def deleteWorkout():
        if request.method == "POST":
            # get variables from HTML
            programId = request.form.get("programId")
            # delete weights related to exercises in the program
            db.execute("DELETE FROM exercise_weights WHERE exercise_id IN ( SELECT exercise_id FROM exercises WHERE program_id = ?)", programId)

            # delete exercises related to the program
            db.execute("DELETE FROM exercises WHERE program_id = ?", programId)

            # delete the program itself
            db.execute("DELETE FROM programs WHERE program_id = ?", programId)

            return redirect("/")
        else:
            userId = session["user_id"]
            #workoutId = session["workoutId"]

            # load all exercises from DB
            programs = db.execute("SELECT * FROM programs WHERE user_id = ?", userId)

            if programs is None:
                return redirect("/")

            return render_template("deleteWorkout.html", programs=programs)


# login - same as w9 finance
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# logout - same as w9 finance
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# register  - same as w9 finance
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # post
    if request.method == "POST":
        # convert data from html
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # check blanks
        if not username:
            return apology("fill in a username", 400)
        # check length of password
        if not(password):
            return apology("enter a password", 400)

        # check password and clarifyPassword
        if password != confirmation:
            return apology("passwords dont match", 400)

        # check if username already taken
        if db.execute("SELECT * FROM users WHERE username = ?", username):
            return apology("username already taken", 400)

        # hash password
        # nyt password, defualt, længde
        hashedPassword = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        # add user and password to DB
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashedPassword)
        # log user in - find id for new user
        userId = db.execute("SELECT user_id FROM users WHERE username = ?", username)
        session["user_id"] = userId[0]["user_id"]

        return redirect("/")

    else:
        return render_template("register.html")






