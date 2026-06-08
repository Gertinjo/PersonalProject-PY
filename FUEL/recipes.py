from fastapi import FastAPI, HTTPException
from typing import List
import database
import model
from modu import Recipe, RecipeCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the recipes CRUD API"}

@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: RecipeCreate):
    """Creates a new recipe in the database."""
    recipe_id = database.create_recipe(recipe)
    return model.recipe(id=recipe_id, **recipe.dict())

@app.get("/recipes/", response_model=List[Recipe])
def read_recipes():
    """Retrieves all recipes from the database."""
    return database.read_recipes()

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def read_recipe(recipe_id: int):
    """Retrieves a single recipe by its ID."""
    recipe = database.read_recipe(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="recipe not found")
    return recipe

@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: RecipeCreate):
    """Updates an existing recipe in the database."""
    updated = database.update_recipe(recipe_id, recipe)
    if not updated:
        raise HTTPException(status_code=404, detail="recipe not found")
    return model.recipe(id=recipe_id, **recipe.dict())

@app.delete("/recipes/{recipe_id}", response_model=dict)
def delete_recipe(recipe_id: int):
    """Deletes a recipe from the database by its ID."""
    deleted = database.delete_recipe(recipe_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="recipe not found")
    return {"message": "recipe deleted successfully"}