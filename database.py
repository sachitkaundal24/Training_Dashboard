from pymongo import MongoClient,errors
from werkzeug.security import generate_password_hash

try:

   

    client = MongoClient('mongodb+srv://ambikeshjha07:Flask123%40@flask.qfmcx.mongodb.net/')

    db = client['TrainingDashboardDB']
    trainers_collection = db['Trainers']
    students_collection = db['Students']

except errors.ConnectionError as e:
    print(f"Error connecting to MongoDB: {e}")

    raise SystemExit("Terminating application.")


def insert_user(username,password,role):

    try:
            hashed_passwword = generate_password_hash(password, method='pbkdf2:sha256')

            user_data = {
                "username": username,
                "password": hashed_passwword,
                "role":role
            }

            if role.lower() == 'trainer':
                trainers_collection.insert_one(user_data)

            else:
                students_collection.insert_one(user_data)
            return True
    
    except Exception as e:
         print(f'Error inserting user: {e}')
         return False
         

'''Returns true if username found'''  
def find_user_by_username(username,role):
      
      if role.lower() == "trainer":
            return trainers_collection.find_one({"username":username})
      else:

            return students_collection.find_one({"username":username})

           

def get_all_users():    
     all_users = {"students": list(students_collection.find({})) } 
     return all_users

def get_all_students():

    return list(students_collection.find({}, {"_id": 0, "username": 1}))

           

