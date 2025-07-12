from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
import uuid

class Job(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    skill_required: str = Field(..., min_length=1, max_length=50)
    location: str = Field(..., min_length=1, max_length=100)
    date: str = Field(..., min_length=1)  # Format: YYYY-MM-DD
    time: str = Field(..., min_length=1)  # Format: HH:MM
    contact_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')
    status: str = Field(default="open", pattern=r'^(open|assigned|completed|cancelled)$')
    assigned_laborers: List[str] = Field(default_factory=list)  # List of phone numbers
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        json_schema_extra = {
            "example": {
                "title": "House Construction - Mason Required",
                "description": "Need an experienced mason for house construction work. 2-day project.",
                "skill_required": "mason",
                "location": "Tilak Nagar, Delhi",
                "date": "2025-07-15",
                "time": "08:00",
                "contact_number": "+919876543210"
            }
        }

class JobCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    skill_required: str = Field(..., min_length=1, max_length=50)
    location: str = Field(..., min_length=1, max_length=100)
    date: str = Field(..., min_length=1)  # Format: YYYY-MM-DD
    time: str = Field(..., min_length=1)  # Format: HH:MM
    contact_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "House Construction - Mason Required",
                "description": "Need an experienced mason for house construction work. 2-day project.",
                "skill_required": "mason",
                "location": "Tilak Nagar, Delhi",
                "date": "2025-07-15",
                "time": "08:00",
                "contact_number": "+919876543210"
            }
        }

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    skill_required: Optional[str] = Field(None, min_length=1, max_length=50)
    location: Optional[str] = Field(None, min_length=1, max_length=100)
    date: Optional[str] = Field(None, min_length=1)
    time: Optional[str] = Field(None, min_length=1)
    contact_number: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    status: Optional[str] = Field(None, pattern=r'^(open|assigned|completed|cancelled)$')

class LaborerAssignment(BaseModel):
    phone_numbers: List[str] = Field(..., min_items=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_numbers": ["+919876543210", "+919876543211"]
            }
        }