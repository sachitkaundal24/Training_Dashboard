from flask import Flask, request, render_template, redirect, url_for,Blueprint, session, flash
from pymongo import MongoClient
 
app = Flask(__name__)
trainer_blueprint = Blueprint('trainer_blueprint', __name__)
client = MongoClient("mongodb+srv://ambikeshjha07:Flask123%40@flask.qfmcx.mongodb.net/")
db = client['TrainingDashboardDB']
collection = db['Students']
new_collection = db['Data']
@trainer_blueprint.route('/add_tasks')
def add_tasks():
    # Fetch distinct usernames from the DB
    users = collection.distinct("username")
    # Create a list of dictionaries with the usernames
    user_list = [{"username": user} for user in users]
    return render_template('trainer.html', users=user_list)
 
@trainer_blueprint.route('/add_task', methods=['POST'])
def add_task():
    # Get lists of usernames and tasks from the form data
    if 'trainer_username' not in session:
        flash("Please log in as trainer to assign tasks.", "error")
        return redirect(url_for('login'))  
   
    trainer_username = session['trainer_username']
    usernames = request.form.getlist('username[]')
    tasks = request.form.getlist('task[]')
 
    # Debug: Print received data
    print(f"Usernames: {usernames}")
    print(f"Tasks: {tasks}")
 
    # Insert tasks into the DB
    for username, task in zip(usernames, tasks):
     print(f"Inserting task for {username}: {task}")  # Debug: Print each task being inserted
     if task.strip():
        new_collection.insert_one({
            "username": username,
            "assigned_by": trainer_username,  # Assuming tasks added here are self-assigned
            "task": task,
            "task_status": "to do"
        })
 
    return redirect(url_for('trainer_blueprint.add_tasks'))