from flask import Flask, render_template, request, redirect, url_for,flash
from werkzeug.security import check_password_hash
from database import insert_user, find_user_by_username
from validate import validate_username, validate_password


app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username =  request.form['username']
        password = request.form['password']
        role = request.form['role']

        valid_username = validate_username(username)
        valid_password = validate_password(password)


        if valid_password == True and valid_username == True:

            success = insert_user(username,password,role)
            if success:
              return redirect(url_for('login'))


       
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role'].lower()

        user = find_user_by_username(username, role)

        if user and check_password_hash(user['password'], password):
            if role == 'trainer':
                return redirect(url_for('trainer_dashboard', username=username))
            elif role == 'student':
                return redirect(url_for('student_dashboard', username=username))
        else:
            flash("Invalid username, password, or role", "error")
            return render_template('login.html')

    return render_template('login.html')




@app.route('/student_dashboard/<username>')
def student_dashboard(username):
    return f"Welcome to the Student Dashboard, {username}!"

@app.route('/trainer_dashboard/<username>')
def trainer_dashboard(username):
    return f"Welcome to the Trainer Dashboard, {username}!"



if __name__ == "__main__":
    app.run(debug=True)
