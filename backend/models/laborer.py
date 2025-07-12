from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class Laborer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., regex=r'^\+?[1-9]\d{1,14}$')
    skill: str = Field(..., min_length=1, max_length=50)
    location: str = Field(..., min_length=1, max_length=100)
    language: str = Field(..., min_length=1, max_length=30)
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    available: bool = True
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "name": "Raju",
                "phone": "+919876543210",
                "skill": "mason",
                "location": "Tilak Nagar",
                "language": "hindi"
            }
        }

class LaborerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., regex=r'^\+?[1-9]\d{1,14}$')
    skill: str = Field(..., min_length=1, max_length=50)
    location: str = Field(..., min_length=1, max_length=100)
    language: str = Field(..., min_length=1, max_length=30)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Raju",
                "phone": "+919876543210",
                "skill": "mason",
                "location": "Tilak Nagar",
                "language": "hindi"
            }
        }

class LaborerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, regex=r'^\+?[1-9]\d{1,14}$')
    skill: Optional[str] = Field(None, min_length=1, max_length=50)
    location: Optional[str] = Field(None, min_length=1, max_length=100)
    language: Optional[str] = Field(None, min_length=1, max_length=30)
    available: Optional[bool] = None