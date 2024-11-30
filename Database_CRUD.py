import sqlite3
import random

DATABASE_FILE = "recipes.db"

def search_recipes_by_ingredients(ingredients, macros):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Construct SQL query with placeholders for ingredients
        placeholders = " AND ".join(["ingredients LIKE ?"] * len(ingredients))
        sql_query = f"""
        SELECT title, ingredients, instructions
        FROM recipes
        WHERE {placeholders}
        """

        # Parameters to match ingredients
        parameters = [f"%{ingredient}%" for ingredient in ingredients]

        # Execute query
        cursor.execute(sql_query, parameters)

        # Fetch up to 5 random matching samples 
        recs = cursor.fetchall()
        if(len(recs))<5:
            recipes_data = random.sample(recs, len(recs))
        else:
            recipes_data = random.sample(recs, 5)

        # Initialize the result dictionary
        recipes = {"Recommended Recipes": []}

        # Populate the dictionary
        for title, ingredients, instructions in recipes_data:
            recipe_entry = {
                title: {
                    "ingredients": ingredients.split("\n"),  # Convert to a list
                    "instructions": instructions
                }
            }
            recipes["Recommended Recipes"].append(recipe_entry)

        # Return the structured dictionary
        return recipes

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {"Recommended Recipes": []}

    finally:
        if conn:
            conn.close()


#print(search_recipes_by_ingredients(['apples', 'cinnamon'], {'calories': 0}))



# if __name__ == "__main__":
#     ingredient_list = ["apples", "cinnamon"]
#     num_recipes_found = search_recipes_by_ingredients(ingredient_list, True)
#     print(f"\n{num_recipes_found}")
