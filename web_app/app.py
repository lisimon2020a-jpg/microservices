# Веб-приложение с графическим интерфейсом

from flask import Flask, render_template, request, redirect, url_for, flash
import httpx

app = Flask(__name__)
app.secret_key = 'change-me-in-production'

API_GATEWAY_URL = "http://localhost:8000"
TIMEOUT = 5.0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    try:
        r = httpx.get(f"{API_GATEWAY_URL}/students", timeout=TIMEOUT)
        r.raise_for_status()
        return render_template('students.html', students=r.json())
    except httpx.HTTPError as e:
        flash(f"Ошибка загрузки студентов: {e}", "error")
        return render_template('students.html', students=[])

@app.route('/grades')
def grades():
    student_id = request.args.get('studentId', type=int)
    try:
        params = {"studentId": student_id} if student_id else {}
        r = httpx.get(f"{API_GATEWAY_URL}/grades", params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return render_template('grades.html', grades=r.json(), student_id=student_id)
    except httpx.HTTPError as e:
        flash(f"Ошибка загрузки оценок: {e}", "error")
        return render_template('grades.html', grades=[], student_id=student_id)

@app.route('/retakes', methods=['GET', 'POST'])
def retakes():
    if request.method == 'POST':
        try:
            retake_data = {
                "discipline": request.form['discipline'],
                "teacher": request.form['teacher'],
                "date": request.form['date'],
                "location": request.form['location'],
                "maxStudents": int(request.form['maxStudents']),
            }
            r = httpx.post(f"{API_GATEWAY_URL}/retakes", json=retake_data, timeout=TIMEOUT)
            r.raise_for_status()
            flash("Пересдача создана!", "success")
            return redirect(url_for('retakes'))
        except (httpx.HTTPError, ValueError) as e:
            flash(f"Ошибка создания: {e}", "error")
    try:
        r = httpx.get(f"{API_GATEWAY_URL}/retakes", timeout=TIMEOUT)
        r.raise_for_status()
        return render_template('retakes.html', retakes=r.json())
    except httpx.HTTPError as e:
        flash(f"Ошибка загрузки: {e}", "error")
        return render_template('retakes.html', retakes=[])

if __name__ == '__main__':
    app.run(port=5004, debug=True)