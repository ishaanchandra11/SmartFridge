import json
import sqlite3
import pandas as pd


def calculate_recipe_macros(ingredients, ingredient_nutrition):
    macros = {"carbs": 0, "fats": 0, "calories": 0, "protein": 0}
    for ingredient in ingredients:
        if ingredient in ingredient_nutrition:
            macros["carbs"] += ingredient_nutrition[ingredient]["carbs"]
            macros["fats"] += ingredient_nutrition[ingredient]["fats"]
            macros["calories"] += ingredient_nutrition[ingredient]["calories"]
            macros["protein"] += ingredient_nutrition[ingredient]["protein"]
        else:
            print(f"Warning: Nutrition data for '{ingredient}' not found.")
    return macros

json_file = "recipes_raw_nosource_fn.json"
database_file = "recipes.db"

nutrition_file = "nutrition.xlsx"

with open(json_file, "r") as file:
    recipes_data = json.load(file)


conn = sqlite3.connect(database_file)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS recipes;")

cursor.execute("""
CREATE TABLE recipes (
    id TEXT PRIMARY KEY,
    title TEXT,
    ingredients TEXT,
    instructions TEXT,
    picture_link TEXT,
    UNIQUE(title, ingredients)
)
""")

for recipe_id, recipe_details in recipes_data.items():

    if not recipe_details.get("title") or not recipe_details.get("instructions") or not recipe_details.get("ingredients"):
        print(f"Skipping recipe ID: {recipe_id} due to missing essential fields.")
        continue  

    
    title = recipe_details["title"]
    ingredients = "\n".join(recipe_details["ingredients"])
    instructions = recipe_details["instructions"]
    picture_link = recipe_details.get("picture_link")

    
    try:
        cursor.execute("""
        INSERT INTO recipes (id, title, ingredients, instructions, picture_link)
        VALUES (?, ?, ?, ?, ?)
        """, (
            recipe_id,
            title,
            ingredients,
            instructions,
            picture_link
        ))
    except sqlite3.IntegrityError:
        
        print(f"Recipe '{title}' with the same ingredients already exists. Skipping.")

nutrition_data = pd.read_excel(nutrition_file)

nutrition_data_cleaned = nutrition_data.drop(columns=["Unnamed: 0"], errors="ignore")
nutrition_data_cleaned.fillna("N/A", inplace=True)

cursor.execute("DROP TABLE IF EXISTS nutrition;")
nutrition_data_cleaned.to_sql("nutrition", conn, if_exists="replace", index=False)


conn.commit()
conn.close()


