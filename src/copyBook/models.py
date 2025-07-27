from pydantic import BaseModel
from datetime import date
from typing import Optional

class CopyBase(BaseModel):
    codigo: str
    libro_id: int
    observaciones: Optional[str] = None

class CopyCreate(CopyBase):
    pass

class CopyResponse(CopyBase):
    id: int
    fecha_adquisicion: date
    disponible: bool
    
    class Config:
        from_attributes = True