from flask import Flask, render_template, request, jsonify
from models.task_model import TaskModel

app = Flask(__name__, template_folder='views')
db = TaskModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = db.get_all_tasks()
    return jsonify([dict(task) for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    if title:
        new_task = db.add_task(title)
        return jsonify(dict(new_task)), 201
    return jsonify({'error': 'Título obrigatório'}), 400

@app.route('/api/tasks/<int:task_id>/toggle', methods=['PATCH'])
def toggle_task(task_id):
    db.toggle_task(task_id)
    return jsonify({'success': True})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db.delete_task(task_id)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
