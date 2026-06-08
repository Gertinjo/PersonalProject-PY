from pydantic import BaseModel

class RecipeCreate(BaseModel):
    title: str
class Recipe(RecipeCreate):
    id: int