from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import food_identifier

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session usage

#access at http://127.0.0.1:5000/
@app.route('/')
def home():
    return render_template('home.html')
#"Welcome to the FOOD ID App"

@app.route('/process-image', methods=['POST'])
def process_image():
    # Check if an image was provided
    if 'images' not in request.files:
        return render_template("error.html", error="No image files provided")
    
    # Get the image file
    files = request.files.getlist('images')
    if not files or any(file.filename == '' for file in files):
        return render_template("error.html", error="No valid image files provided")
    
    # Retrieve slider values from the form
    calories = int(request.form.get('calories', 0))
    protein = int(request.form.get('protein', 0))
    carbohydrates = int(request.form.get('carbohydrates', 0))
    fats = int(request.form.get('fats', 0))
    
    # Combine slider data into a dictionary
    slider_data = {
        "calories": calories,
        "protein": protein,
        "carbohydrates": carbohydrates,
        "fats": fats
    }
    
    # Pass the image and slider data to the food_identifier function
    recipes = food_identifier.identify(files, slider_data)

    # Store the recipes in the session to access in /results
    session['recipes'] = recipes

    # Redirect to the results page
    return redirect(url_for("results"))


@app.route('/results')
def results():
    # Retrieve the recipes from the session
    recipes = session.get('recipes')

    # Handle case where no recipes are found
    if recipes is None:
        return render_template("error.html", error="No recipes found")
    
    # Render results page with the recipes
    return render_template("results.html", recipes=recipes)



if __name__ == "__main__":
    app.run(debug=True)

