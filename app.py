from flask import Flask, request, jsonify
from models import (create_task_in_db, update_task_in_db, delete_task_from_db, 
                    get_tasks_by_user_from_db, update_status_in_db, assign_user_to_task_in_db, 
                    initialize_users, get_all_users,get_unassigned_tasks)
from config import Config
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object(Config)


client = MongoClient(app.config['MONGO_URI'])
db = client.todo_db

initialize_users(db)  

# Endpoint pour créer une tâche
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = create_task_in_db(db, data) 
    users = get_all_users(db)  
    return jsonify({
        'message': 'Tâche créée avec succès',
        'task_id': str(task['_id']),
        'users': users 
    }), 201

# Endpoint pour modifier une tâche existante
@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    update_task_in_db(db, task_id, data)  
    return jsonify({'message': 'Tâche modifiée avec succès'}), 200

# Endpoint pour supprimer une tâche
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    delete_task_from_db(db, task_id)  
    return '', 204

# Endpoint pour récupérer les tâches assignées à un utilisateur
@app.route('/tasks/user/<user_id>', methods=['GET'])
def get_tasks_by_user(user_id):
    if (user_id.lower() == "none" or user_id == "" ):
        
        tasks = get_unassigned_tasks(db)
    else:
        tasks = get_tasks_by_user_from_db(db, user_id)
    
    return jsonify(tasks), 200

# Endpoint pour changer le statut d'une tâche
@app.route('/tasks/<task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    data = request.json
    update_status_in_db(db, task_id, data['status'])  
    return jsonify({'message': 'Statut de la tâche mis à jour'}), 200

# Endpoint pour assigner un utilisateur à une tâche après création
@app.route('/tasks/<task_id>/assign', methods=['PATCH'])
def assign_user_to_task(task_id):
    data = request.json
    assign_user_to_task_in_db(db, task_id, data['user_id'])  
    return jsonify({'message': 'Utilisateur assigné avec succès'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

