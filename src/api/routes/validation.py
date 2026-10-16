"""Validation routes."""
from fastapi import APIRouter
router = APIRouter()

@router.post("/validate")
def validate_code():
    return {"status": "ok"}
