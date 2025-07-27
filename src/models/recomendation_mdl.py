from pydantic import BaseModel
from typing import Optional

class RecommendationBase(BaseModel):
    origen_id: int
    recomendado_id: int
    comentario: Optional[str] = None

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationResponse(RecommendationBase):
    id: int
    
    class Config:
        from_attributes = True