from bson import ObjectId


def initialize_users(db):
    
    users = [
        {'name': 'Ulrich', 'email': 'ulrich@example.com'},
        {'name': 'Deo', 'email': 'deo@example.com'},
        {'name': 'Gracias', 'email': 'gracias@example.com'}
    ]
    
    
    if db.users.count_documents({}) == 0:
        db.users.insert_many(users)

def get_all_users(db):

    """
    La fonction get_all_users permet de récupérer tous les utilisateurs
    """
    users = db.users.find()
    return [{
        'user_id': str(user['_id']),
        'name': user['name'],
        'email': user['email']
    } for user in users]


def create_task_in_db(db, data):

    """
    Cette fonction pour créer une nouvelle tâche
    """
    task = {
        'title': data['title'],
        'description': data['description'],
        'assigned_to': None ,
        'status': None, 
        'due_date': data.get('due_date')
    }
    db.tasks.insert_one(task)
    return task


def update_task_in_db(db, task_id, data):
    """
    Cette fonction permet de modifier une tâche
    """
    db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': data})


def delete_task_from_db(db, task_id):

    """
    La fonction delete_task_from_db permet de supprimer une tâche
    """
    db.tasks.delete_one({'_id': ObjectId(task_id)})


def get_tasks_by_user_from_db(db, user_id):

    """
    La fonction get_task_by_user_from_db permet de récupérer les tâches d'un utilisateur
    """
    tasks = db.tasks.find({"assigned_to": user_id})
    return [{
        'task_id': str(task['_id']),
        'title': task['title'],
        'description': task['description'],
        'assigned_to': task['assigned_to'],
        'status': task['status'],
        'due_date': task.get('due_date')
    } for task in tasks]


def update_status_in_db(db, task_id, status):
    """
    Cette fonction permet de changer ou de mettre à jour le statut d'une tâche
    """
    db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'status': status}})


def assign_user_to_task_in_db(db, task_id, user_id):
    """
    L'objectif de cette fonction est d'assigner un utilisateur à une tâche
    """
    db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'assigned_to': user_id}})


def get_unassigned_tasks(db):

    """
    Fonction pour récupérer les tâches non assignées, les tâches qui n'ont été affecté à aucun utilisateur
    """
    tasks = db.tasks.find({"assigned_to": None})  
    return [{
        'task_id': str(task['_id']),
        'title': task['title'],
        'description': task['description'],
        'assigned_to' : task.get('assigned_to'),
        'status': task['status'],
        'due_date': task.get('due_date')
    } for task in tasks]

