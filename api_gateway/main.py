# API Gateway для портала ДОТ РосНОУ

from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="API Gateway ДОТ РосНОУ", version="1.0.0")

STUDENTS_SERVICE = "http://localhost:5001"
GRADES_SERVICE = "http://localhost:5002"
RETAKES_SERVICE = "http://localhost:5003"

TIMEOUT = 5.0

# === СТУДЕНТЫ ===
@app.get("/students")
async def get_students():
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f'{STUDENTS_SERVICE}/students')
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Students service unavailable: {e}")

@app.get("/students/{student_id}")
async def get_student(student_id: int):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f'{STUDENTS_SERVICE}/students/{student_id}')
            if r.status_code == 404:
                raise HTTPException(status_code=404, detail="Student not found")
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Students service unavailable: {e}")

@app.post("/students")
async def add_student(student: dict):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f'{STUDENTS_SERVICE}/students', json=student)
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Students service unavailable: {e}")

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.delete(f'{STUDENTS_SERVICE}/students/{student_id}')
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Students service unavailable: {e}")

# === ОЦЕНКИ И ДОЛГИ ===
@app.get("/grades")
async def get_grades(studentId: int = None):
    try:
        params = {"studentId": studentId} if studentId else {}
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f'{GRADES_SERVICE}/grades', params=params)
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Grades service unavailable: {e}")

@app.post("/grades")
async def add_grade(grade: dict):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f'{GRADES_SERVICE}/grades', json=grade)
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Grades service unavailable: {e}")

@app.get("/debts")
async def get_debts(studentId: int = None):
    try:
        params = {"studentId": studentId} if studentId else {}
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f'{GRADES_SERVICE}/debts', params=params)
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Grades service unavailable: {e}")

# === ПЕРЕСДАЧИ ===
@app.get("/retakes")
async def get_retakes():
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f'{RETAKES_SERVICE}/retakes')
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Retakes service unavailable: {e}")

@app.post("/retakes")
async def create_retake(retake: dict):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f'{RETAKES_SERVICE}/retakes', json=retake)
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Retakes service unavailable: {e}")

@app.post("/retakes/{retake_id}/enroll")
async def enroll_retake(retake_id: int, data: dict):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f'{RETAKES_SERVICE}/retakes/{retake_id}/enroll', json=data)
            if r.status_code == 404:
                raise HTTPException(status_code=404, detail="Retake not found")
            if r.status_code == 400:
                raise HTTPException(status_code=400, detail="No seats")
            if r.status_code == 409:
                raise HTTPException(status_code=409, detail="Already enrolled")
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Retakes service unavailable: {e}")

# === HEALTH CHECK ===
@app.get("/health")
async def health():
    results = {}
    async with httpx.AsyncClient(timeout=2.0) as client:
        for name, url in [
            ("students", STUDENTS_SERVICE),
            ("grades", GRADES_SERVICE),
            ("retakes", RETAKES_SERVICE),
        ]:
            try:
                r = await client.get(f"{url}/")
                results[name] = "ok" if r.status_code < 500 else "error"
            except Exception:
                results[name] = "unavailable"
    return results