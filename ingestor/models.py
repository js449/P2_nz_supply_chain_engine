from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, Literal

class RoadEvent(BaseModel):
    event_id: int 
    event_type: Literal["Construction", "Accident", "Weather", "Road Closure"]
    impact_score: float = Field(ge=0, le=10)  # ge = greater/equal, le = less/equal
    location: str
    status: Optional[str] = "Unknown"

    @field_validator('location')
    @classmethod
    def location_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Location cannot be empty')
        return v