from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    marspage = mongo.db.marspage.find_one()

    # Return template and data
    return render_template("index.html", marspage=marspage)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    marspage = mongo.db.marspage

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    marspage.update({}, mars_data, upsert=True)

    # Redirect back to home page
    #return redirect("/")
    return "S"

if __name__ == "__main__":
    app.run(debug=True)
