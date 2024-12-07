from flask import Flask
from login_signup_render import login_signup_blueprint
from trainee_render import trainee_blueprint  
from trainer_render import trainer_blueprint  
from flask_jwt_extended import JWTManager

app = Flask(__name__)


app.secret_key = 'hello_world' 


jwt = JWTManager(app)


app.register_blueprint(login_signup_blueprint)
app.register_blueprint(trainee_blueprint)
app.register_blueprint(trainer_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
