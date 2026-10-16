"""Benchmarks routes."""
from fastapi import APIRouter
router = APIRouter()

@router.get("/benchmarks")
def list_benchmarks():
    return []
