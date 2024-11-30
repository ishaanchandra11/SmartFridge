import cv2
import numpy as np
import Database_CRUD
import numpy as np
import torch

def identify(files, slider_data):
    #identifies food AND recommends recipe. 
    #return {"Recommended Recipes": ["Pasta Primavera", "Tomato Soup", "Caesar Salad"]}

    ingredients_list = []
    for image in files:
      ingredients = get_ingredients(image)
      for i in ingredients:
         if i not in ingredients_list:
            ingredients_list.append(i)

    #ingredients_list = ["apples", "bananas"]
    print(ingredients_list)

    valid_recipes = get_recipes(ingredients_list, slider_data)

    ingred_str = ""
    for i in ingredients_list:
       ingred_str+=i+', '

    valid_recipes['Ingredients Available'] = ingred_str.strip()[0:-1]

    print(valid_recipes)
    
    '''demo output of valid_recipes
    recipes = {"Recommended Recipes": [
    {
      "Pasta Primavera": {
        "ingredients": ["x", "y", "z"],
        "instructions": "dsfdsfsdfs"
      }
    },
    {
      "Tomato Soup": {
        "ingredients": ["x", "y", "z"],
        "instructions": "dsfdsfsdfs"
      }
    },
    {
      "Sandwich": {
        "ingredients": ["x", "y", "z"],
        "instructions": "dsfdsfsdfs"
    }}]}'''

    return valid_recipes


def get_ingredients(image):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    image_data = image.read()

    # Convert image data to a NumPy array
    nparr = np.frombuffer(image_data, np.uint8)

    # Decode the image into OpenCV format
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the image to RGB (YOLOv5 expects RGB format)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform detection using YOLOv5
    results = model(img_rgb)

    # Extract detected objects and filter for food-related labels
    detected_objects = results.pandas().xyxy[0]  # Pandas DataFrame with detection results
    food_items = list(set(detected_objects['name'].tolist()))  # List of detected class labels

    print(food_items)
    return food_items


def get_recipes(ingredients, slider_data):
   #consult the database here. 
   result = Database_CRUD.search_recipes_by_ingredients(ingredients, slider_data) 
   return result