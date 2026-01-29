from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Employee, Attendance
from .schemas import EmployeeCreate, AttendanceCreate
from .validators import validate_attendance_status

def create_employee(db: Session, data: EmployeeCreate):
    if db.query(Employee).filter(Employee.employee_id == data.employee_id).first():
        raise HTTPException(status_code=409, detail="Employee ID already exists")

    if db.query(Employee).filter(Employee.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")

    emp = Employee(**data.dict())

    print("<<<<<<<<<<<<< EMP DATA >>>>>>")
    print(emp)

    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

def get_all_employees(db: Session):
    return db.query(Employee).all()

def delete_employee(db: Session, emp_id: str):

    emp = db.query(Employee).filter(Employee.employee_id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()
    return {"message": "Employee deleted successfully"}

def mark_attendance(db: Session, emp_id: str, data: AttendanceCreate):
    validate_attendance_status(data.status)

    emp = db.query(Employee).filter(Employee.employee_id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    if db.query(Attendance).filter(
        Attendance.employee_id == emp_id,
        Attendance.date == data.date
    ).first():
        raise HTTPException(status_code=409, detail="Attendance already marked for this date")

    record = Attendance(
        employee_id=emp_id,
        date=data.date,
        status=data.status
    )

    db.add(record)
    db.commit()
    success= {"message":f"{data.status} added Successfully "}
    return success

def get_attendance(db: Session, emp_id: str):
    emp = db.query(Employee).filter(Employee.employee_id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    return db.query(Attendance).filter(
        Attendance.employee_id == emp_id
    ).all()
