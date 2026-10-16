# Микросервис управления студентами

from flask import Flask, jsonify, request

app = Flask(__name__)

students = [
    {"id": 1, "fullName": "Иванов Иван Иванович", "group": "ПИ-21-1", "email": "ivanov@rosnou.ru"},
    {"id": 2, "fullName": "Петрова Анна Сергеевна", "group": "ПИ-21-2", "email": "petrova@rosnou.ru"},
    {"id": 3, "fullName": "Сидоров Пётр Алексеевич", "group": "ПИ-22-1", "email": "sidorov@rosnou.ru"},
]

@app.route('/students', methods=['GET'])
def get_students()
    return jsonify(students)

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    return jsonify(student) if student else ('Not Found', 404)

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    data['id'] = len(students) + 1
    students.append(data)
    return jsonify(data), 201

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"status": "deleted"}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)