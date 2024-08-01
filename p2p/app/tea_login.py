from fastapi import APIRouter, HTTPException, Depends
from db import get_db1
import mysql.connector
from pydantic import BaseModel

tl_router = APIRouter()

class TeacherLogin(BaseModel):
    userId: str
    password: str

@tl_router.post("/teacher_login")
async def teacher_login(teacher: TeacherLogin, db: mysql.connector.connection.MySQLConnection = Depends(get_db1)):
    teacherId = teacher.userId
    password = teacher.password
    print(teacherId, password)
    
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM teachers WHERE TEACHER_ID = %s AND PASSWORD = %s", (teacherId, password))
    teacher_row = cursor.fetchone()
    
    if teacher_row is None:
        print("Not found")
        raise HTTPException(status_code=400, detail="Invalid teacherId or password")
    
    teacher_dict = {column[0]: value for column, value in zip(cursor.description, teacher_row)}
    
    cursor.execute("SELECT TEACHER_NAME FROM teachers WHERE TEACHER_ID = %s", (teacherId,))
    teacher_details = cursor.fetchone()
    
    cursor.execute("SELECT SUBJECT FROM subjects WHERE TEACHER_ID = %s", (teacherId,))
    subjects = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT SCHOOL_NAME FROM schools WHERE SCHOOL_ID = %s", (teacher_row[0],))  # Assuming SCHOOL_ID is the third column
    school_name = cursor.fetchone()[0]
    
    teacher_dict.update({
        "SCHOOL_NAME": school_name,
        "subjects": subjects
    })
    print(teacher_dict)
    return {"message": "Login successful", "teacher": teacher_dict}