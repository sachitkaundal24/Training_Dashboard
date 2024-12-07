from flask import Flask, request, render_template, redirect, url_for,Blueprint, session, flash
from pymongo import MongoClient
trainee_blueprint = Blueprint('trainee_blueprint', __name__)
app = Flask(__name__)
 
class Trainee:
    def __init__(self, username, trainee_name, task):
        self.username = username
        self.trainee_name = trainee_name
        self.task = task
 
client = MongoClient("mongodb+srv://ambikeshjha07:Flask123%40@flask.qfmcx.mongodb.net/")
db = client['TrainingDashboardDB']
collection = db['Data']
 
 
@trainee_blueprint.route('/tasks')
def get_user_tasks():
    # Ensure the user is logged in by checking the session
    if 'username' not in session:
        flash("Please log in to view your tasks.", "error")
        return redirect(url_for('login_signup_blueprint.login'))  # Redirect to login if not logged in
   
    # #for debugging
    # print(f"Session username: {session['username']}")
 
    # Get the logged-in user's username from the session
    username = session['username']
 
    # Fetch tasks specifically for the logged-in user
    tasks = list(collection.find({"username": username}, {"_id": 0}))
 
    # Render the template with the user's tasks
    return render_template('trainee.html', tasks=tasks, username=username)

@trainee_blueprint.route('/update_user_task_status', methods=['POST'])
def update_user_task_status():
    if 'username' not in session:
        flash("Please log in to view your tasks.", "error")
        return redirect(url_for('login_signup_blueprint.login'))
    
    task_updates = request.form.to_dict(flat=False)  # Get all form data
    print("Task Updates:", task_updates)  # Debugging line

    username = session['username']
    assigned_by = task_updates.get('assigned_by', [])
    tasks = task_updates.get('task', [])
    statuses = task_updates.get('task_status', [])
    
    # Debugging line
    print(f"User: {username}, Assigned By: {assigned_by}, Tasks: {tasks}, Statuses: {statuses}")

    # Iterate through each task and update the status
    for i in range(len(tasks)):
        query = {
            "username": username,
            "assigned_by": assigned_by[i],
            "task": tasks[i]
        }
        update = {"$set": {"task_status": statuses[i]}}
        result = collection.update_one(query, update)
        
        # Debugging line
        print(f"Update Result for query {query}: {result.modified_count} documents updated")

    return redirect(url_for('trainee_blueprint.get_user_tasks'))

@trainee_blueprint.route('/view_all_tasks')
def view_all_tasks():
    # Ensure the user is logged in by checking the session
    if 'username' not in session:
        flash("Please log in to view tasks.", "error")
        return redirect(url_for('login_signup_blueprint.login'))
   
    # Fetch all tasks from the database
    all_tasks = list(collection.find({}, {"_id": 0}).sort("username", 1))
   
    # Render the template with all tasks
    return render_template('all_tasks.html', tasks=all_tasks)
 
if __name__ == '__main__':
    app.run(debug=True)