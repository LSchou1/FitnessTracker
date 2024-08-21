# Workout tracker
#### Description:
Workout Tracker is a website to keep track of your workouts and progression over time. The unique feature of this tracker is that it automatically updates the weight to an exercise if the required number of reps is achieved.

Users can register or log in to the webste, then add, delete and edit exercises and workouts. The user can view their workout history and weight progression to each workout with a graph

## Updates
### 13/8/2024 - Previous workout reps is now a placeholder for each set
## Features
### Registration and Login
- **Registration and Login:** Users can register and log to the webste. All passwords are hashed and stored in an SQL database (database.db) Hashing a password is a one-way function to secure that passwords can be stored safely. One-way function means that the input is being hashed to a cyphertext, so the input password to an username is being hashed and then compared to the stored hashed password.

### Main Page
Once logged in users sees all their workouts and can add or delete workouts. When adding an exercise, the user must enter a exercise name, sets, reps, weight and a progression weight. The progression weight indicates how much weight must be added for progression.

To each workout there is three options:

- **Perform Workout:** When pressed the user will perform a workout and will be presented to all exercises in the giving workout. To each exercise it will display number of sets, reps and weight. The user can enter the number of reps he/she has performed, then the application automatically updates the weights if the user meets the required number of reps across all sets to an exercise.

- **Edit Workout:** Users can add or edit exercise details such as exercise name, number of sets and reps, weight, and progression weight.

- **View Progression:** Users can view their progress over time for   each workout and exercise through a visual graph, allowing track strength improvements. To begin with all exercises to an workout is displayed, the user can deselect exercises on the graph by pres an exercise above the graph.

## Built with:
- **Python**
- **Flask**
- **Sqlite3**
- **HTML**
- **JavaScipt**
- **CSS**
- **Jinja**
- **Chart JS**
- **Bootstrap**
- **Other small libraries or packages**

## Future improvements
- **AI-assistent** Assistent to make programs.
- **Email to user registration:**
- **Forgot password:** Following the addition of emails, it could be necessary to integrate a "forgot password" system.

## About CS50

This project is the final part of the CS50x course, an introduction to computer science and programming. Tools and concepts covered in this course include:

- **Languages:** C, Python, SQL, HTML, CSS, JavaScript
- **Frameworks and Libraries:** Flask, Jinja, Bootstrap
- **Concepts:** Data structures, algorithms, web development, databases.

The skills gained in CS50 were crucial for developing this Workout Tracker application.

