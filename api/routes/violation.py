from fastapi import APIRouter
from db.models import get_all_violation, get_violation_by_date, get_violation_by_id

router = APIRouter(prefix="/violations", tags=["violations"])

@router.get('/')
def all_violation():
    return get_all_violation()

@router.get('/{person_id}')
def person_violations(id : str):
    return get_violation_by_id(id)

@router.get('/date/{date}')
def date_violations(date: str):
    return get_violation_by_date(date)
