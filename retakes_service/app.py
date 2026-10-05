# Микросервис управления пересдачами

from flask import Flask, jsonify, request

app = Flask(__name__)

retakes = [
    {
        "id": 1,
        "discipline": "Базы данных",
        "teacher": "Петров П.П.",
        "date": "2025-02-10T14:00:00",
        "location": "Ауд. 312",
        "maxStudents": 15,
        "enrolled": [2]
    },
]

@app.route('/retakes', methods=['GET'])
def get_retakes():
    return jsonify(retakes)

@app.route('/retakes', methods=['POST'])
def create_retake():
    data = request.json
    data['id'] = len(retakes) + 1
    data['enrolled'] = []
    retakes.append(data)
    return jsonify(data), 201

@app.route('/retakes/<int:retake_id>/enroll', methods=['POST'])
def enroll_retake(retake_id):
    retake = next((r for r in retakes if r["id"] == retake_id), None)
    if not retake:
        return jsonify({"error": "Retake not found"}), 404
    data = request.json
    student_id = data.get("studentId")
    if len(retake["enrolled"]) >= retake["maxStudents"]:
        return jsonify({"error": "No seats"}), 400
    if student_id in retake["enrolled"]:
        return jsonify({"error": "Already enrolled"}), 409
    retake["enrolled"].append(student_id)
    return jsonify(retake), 200

if __name__ == '__main__':
    app.run(port=5003, debug=True)