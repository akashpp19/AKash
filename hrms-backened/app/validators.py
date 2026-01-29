from fastapi import HTTPException

def validate_attendance_status(status: str):
    if status.strip().lower() not in ["present", "absent"]:
        raise HTTPException(
            status_code=422,
            detail="Status must be either 'Present' or 'Absent'"
        )
