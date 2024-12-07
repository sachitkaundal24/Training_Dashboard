from flask import Flask, render_template, request, redirect, url_for,flash, session, jsonify,Blueprint
from werkzeug.security import check_password_hash
from database import insert_user, find_user_by_username
from validate import validate_username, validate_password
from datetime import timedelta
from flask_jwt_extended import create_access_token, JWTManager

login_signup_blueprint = Blueprint('login_signup_blueprint', __name__)
app = Flask(__name__)


app.permanent_session_lifetime = timedelta(days=2)
jwt = JWTManager(app)


@login_signup_blueprint.route('/signup',methods=['GET','POST'])
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
              return redirect(url_for('login_signup_blueprint.login'))

    return render_template('signup.html')



@login_signup_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        session.permanent = True

        username = request.form['username']
        password = request.form['password']
        role = request.form['role'].lower()

       

        user = find_user_by_username(username, role)

        if user and check_password_hash(user['password'], password):

                session['username'] = username
                session['role'] = role
                
                #for debugging
                print(f"User logged in: {session['username']}")

                access_token = create_access_token(identity=str(user['_id']))

                if request.headers.get('Accept') == 'application/json':
                
                    return jsonify({
                        'message': 'Login successful',
                        'access_token': access_token
                    })

                if role == 'trainer':

                    session['trainer_username'] = username
                    return redirect(url_for('trainer_blueprint.add_tasks'))
                
                elif role == 'student':
                    session['trainee_username'] = username
                    return redirect(url_for('trainee_blueprint.get_user_tasks'))
        else:
            flash("Invalid username, password, or role", "error")
            return render_template('login.html')

    return render_template('login.html')


@login_signup_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_signup_blueprint.login'))




if __name__ == "__main__":
    app.run(debug=True)