"""Pydantic schemas."""
from pydantic import BaseModel

class ProgramSchema(BaseModel):
    id: int
    program_id: str
    domain: str
    validation_status: str
