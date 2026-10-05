# Микросервис управления оценками и долгами

from flask import Flask, jsonify, request

app = Flask(__name__)

grades = [
    {"id": 1, "studentId": 1, "discipline": "Программирование", "value": "5", "date": "2025-01-15"},
    {"id": 2, "studentId": 1, "discipline": "Математика", "value": "4", "date": "2025-01-20"},
    {"id": 3, "studentId": 2, "discipline": "Программирование", "value": "3", "date": "2025-01-16"},
]

debts = [
    {"id": 1, "studentId": 2, "discipline": "Базы данных", "type": "exam", "since": 3},
    {"id": 2, "studentId": 3, "discipline": "Физика", "type": "credit", "since": 2},
]

@app.route('/grades', methods=['GET'])
def get_grades():
    student_id = request.args.get('studentId', type=int)
    if student_id:
        return jsonify([g for g in grades if g["studentId"] == student_id])
    return jsonify(grades)

@app.route('/grades', methods=['POST'])
def add_grade():
    data = request.json
    data['id'] = len(grades) + 1
    grades.append(data)
    return jsonify(data), 201

@app.route('/debts', methods=['GET'])
def get_debts():
    student_id = request.args.get('studentId', type=int)
    if student_id:
        return jsonify([d for d in debts if d["studentId"] == student_id])
    return jsonify(debts)

if __name__ == '__main__':
    app.run(port=5002, debug=True)