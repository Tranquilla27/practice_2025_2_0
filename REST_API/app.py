from flask import Flask, request, jsonify

app = Flask(__name__)

# Пример хранилища задач
tasks = [
    {"id": 1, "title": "Купить хлеб", "done": False},
    {"id": 2, "title": "Выучить REST API", "done": False}
]

# Получить все задачи
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Получить одну задачу по id
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Задача не найдена"}), 404
    return jsonify(task)

# Добавить новую задачу
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": data.get("title"),
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Обновить задачу
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Задача не найдена"}), 404
    task["title"] = data.get("title", task["title"])
    task["done"] = data.get("done", task["done"])
    return jsonify(task)

# Удалить задачу
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run(debug=True)
