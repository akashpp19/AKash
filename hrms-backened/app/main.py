from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .database import SessionLocal, engine

from . import models

from .crud import get_all_employees,get_attendance,create_employee,delete_employee,mark_attendance
from .schemas import EmployeeCreate,EmployeeResponse,AttendanceCreate,AttendanceResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS Lite Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health():
    return {"status": "HRMS Lite Backend Running"}

@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def add_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db, emp)

@app.get("/employees", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return get_all_employees(db)

@app.delete("/employees/{emp_id}")
def remove_employee(emp_id: str, db: Session = Depends(get_db)):
    emp_id=emp_id.strip().lower()
    return delete_employee(db, emp_id)

@app.post("/employees/{emp_id}/attendance",response_model=AttendanceResponse, status_code=201)
def add_attendance(emp_id: str, data: AttendanceCreate, db: Session = Depends(get_db)):
    emp_id=emp_id.strip().lower()
    return mark_attendance(db, emp_id, data)

@app.get("/employees/{emp_id}/attendance")
def view_attendance(emp_id: str, db: Session = Depends(get_db)):
    emp_id=emp_id.strip().lower()
    return get_attendance(db, emp_id)

