import sqlite3
from modu import Recipe, RecipeCreate
def create_connection():
    """Creates a connection to the SQLite database."""
    connection = sqlite3.connect("recipe.db")
    connection.row_factory = sqlite3.Row
    return connection



def create_table():
    """Creates the recipes table in the database if it doesn't exist."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        """)
    connection.commit()
    connection.close()


create_table()

def read_recipes():
    """
    Retrieves all recipes from the database.

    Returns:
        list: A list of recipe models representing all recipes in the database.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recipes")
    rows = cursor.fetchall()
    connection.close()
    recipes = [Recipe(id=row[0], title=row[1]) for row in rows]
    return recipes


def read_recipe(recipe_id: int):
    """
    Retrieves a single recipe from the database by its ID.

    Args:
        recipe_id (int): The ID of the recipe to retrieve.

    Returns:
        recipe: A recipe model representing the retrieved recipe.
        Returns None if the recipe is not found.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return Recipe(id=row["id"], title=row["title"])


def update_recipes(recipe_id: int, recipe: RecipeCreate) -> bool:
    """
    Updates an existing recipe in the database.

    Args:
        recipe_id (int): The ID of the recipe to update.
        recipe (recipeCreate): A pydantic model containing the new title and director of the recipe.

    Returns:
        bool: True if the recipe was updated successfully, False otherwise.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE recipes SET title = ?, director = ? WHERE id = ?", (recipe.title, recipe.director, recipe_id))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0


def delete_recipe(recipe_id: int) -> bool:
    """
    Deletes a recipe from the database by its ID.

    Args:
        recipe_id (int): The ID of the recipe to delete.

    Returns:
        bool: True if the recipes was deleted successfully, False otherwise.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0