from flask import Flask, request, jsonify,render_template
from pymongo import MongoClient

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database']
collection = db['your_collection']


# @app.route('/')
# def index():
#     # Fetch the first user from the collection (or modify to fetch as needed)
#     user = collection.find_one({}, {'_id': 0, 'username': 1})
#     if user:
#         username = user.get('username')
#         return render_template('trainer.html', username=username)
#     else:
#         return "No user found", 404


@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        # Get JSON data from the request
        data = request.get_json()
        username = data.get('username')
        assigned_by = data.get('assigned_by')
        task_name = data.get('task')
        status = data.get('status', 'to do')  # Default status to 'to do' if not provided

        # Validate input data
        if not username or not assigned_by or not task_name:
            return jsonify({'error': 'Missing username, assigned_by, or task field'}), 400

        # Check if the task already exists for the user
        existing_task = collection.find_one({
            "username": username,
            "assigned_by": assigned_by,
            "task": task_name
        })

        if existing_task:
            return jsonify({'message': 'Task already exists'}), 400

        # Insert the new task
        collection.insert_one({
            "username": username,
            "assigned_by": assigned_by,
            "task": task_name,
            "task_status": status
        })

        return jsonify({'message': 'Task added successfully'}), 201

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

