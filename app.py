from flask import Flask, render_template, request
from book_recomendations import load_books, get_recommendations

# Initialize Flask
app = Flask(__name__)

# Load your dataset once when the app starts
df = load_books("/Users/lilianatrejo/Data_Science_Project/Books.csv")

# Home page route
@app.route("/")
def index():
    return render_template("index.html")

# Results page route
@app.route("/results", methods=["POST"])
def results():
    mood = request.form["mood"]  # Get the user's input from the form
    recommendations = get_recommendations(mood, df)
    return render_template("results.html", mood=mood, books=recommendations)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
