#!/usr/bin/env python3
"""
Pinkberries flask-based web application.
"""
import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values  ### You will need to install dotenv from terminal
from datetime import date
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# Create and configure Flask app
def create_app():
    """
    Create and configure the Flask application.
    returns: app: the Flask application object
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 's3cr3t'
    # load flask config from env variables
    config = dotenv_values()
    app.config.from_mapping(config)

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")

    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    try:
        client.admin.command("ping")
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(" MongoDB connection error:", e)

    return app, db  # ✅ Now correctly returning app and db


# ✅ Flask app and database created here
app, db = create_app()


### Add your functions here: ###
@app.route("/")
def home():
    """
    Fetches all exhibitions and displays them on the home page.
    """
    try:
        exhibitions = list(db.exhibitions.find())  # ✅ Ensure exhibitions collection is used
        return render_template("index.html", exhibitions=exhibitions)
    except Exception as e:
        print(f"Error occurred while fetching exhibitions: {e}")
        return f"An error occurred while fetching the exhibitions: {e}", 500


@app.route("/search")
def search():
    """
    Renders the search page.
    """
    return render_template("search.html")


@app.route("/filter", methods=["GET"])
def filter_exhibitions():
    """
    Filters exhibitions based on user-selected criteria.
    """
    style = request.args.getlist("style")
    medium = request.args.getlist("medium")
    event_type = request.args.getlist("event_type")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # Build MongoDB query
    query = {}
    if style:
        query["Art Style"] = {"$in": style}
    if medium:
        query["Art Medium"] = {"$in": medium}
    if event_type:
        query["Event Type"] = {"$in": event_type}
    
    # Handle date filtering
    if start_date and end_date:
        try:
            start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            query["Dates"] = {"$gte": start_dt, "$lte": end_dt}
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."

    # Fetch results from MongoDB
    results = list(db.exhibitions.find(query, {"_id": 0}))  # ✅ Fixed to use "exhibitions"

    return render_template("filtered_results.html", results=results)


@app.route("/exhibition/<exhibition_id>")
def exhibition_detail(exhibition_id):
    """
    Displays details of a single exhibition.
    """
    exhibition = db.exhibitions.find_one({"_id": ObjectId(exhibition_id)})
    
    if not exhibition:
        return "Exhibition not found", 404
    
    return render_template("exhibition_detail.html", exhibition=exhibition)


@app.route("/create_exhibit", methods=["GET", "POST"])
def create_exhibit():
    """
    Route for GET, POST requests to the create page.
    Accepts the form submission data for a new exhibit and saves the exhibition to the database.
    Returns:
        redirect (Response): A redirect response to the home page.
    """
    if request.method == "POST":
        title = request.form["ftitle"]
        start = request.form["start_date"]
        end = request.form["end_date"]
        location = request.form["flocation"]
        cost = request.form["fcost"]
        artist = request.form["fartist"]
        artist_url = request.form["farturl"]
        art_style = request.form["fart_style"]
        art_medium = request.form["fart_medium"]
        event_type = request.form["fevent_type"]
        description = request.form["fdescription"]
        image_url = request.form["fimage_url"]
        created_by = request.form["created_by"]

        exhibition = {
            "title": title,
            "dates": {"start": start, "end": end},
            "location": location,
            "cost": cost,
            "artist": {"artist": artist, "profile_url": artist_url},
            "art_style": art_style,
            "art_medium": art_medium,
            "event_type": event_type,
            "description": description,
            "image_url": image_url,
            "created_by": created_by,
            "created_at": datetime.datetime.utcnow(),
        }

        db.exhibitions.insert_one(exhibition)
        return redirect(url_for("home"))

    return render_template("create_exhibit.html")


@app.route("/edit/<post_id>")
def edit(post_id):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    Args:
        post_id (str): The ID of the post to edit.
    Returns:
        rendered template (str): The rendered HTML template.
    """
    exhibition = db.exhibitions.find_one({"_id": ObjectId(post_id)})
    return render_template("edit.html", exhibition=exhibition)


@app.route("/edit/<exhibition_id>", methods=["POST"])
def edit_post(exhibition_id):
    """
    Edits an existing exhibition in the database.
    """
    exhibition = db.exhibitions.find_one({"_id": ObjectId(exhibition_id)})
    if not exhibition:
        return "Exhibition not found", 404

    updated_exhibition = {}

    # Only update fields that are provided
    title = request.form.get("ftitle")
    if title:
        updated_exhibition["title"] = title
    start = request.form.get("start_date")
    end = request.form.get("end_date")
    if start or end:
        updated_exhibition["dates"] = {
            "start": start if start else exhibition["dates"]["start"],
            "end": end if end else exhibition["dates"]["end"]
        }
    location = request.form.get("flocation")
    if location:
        updated_exhibition["location"] = location
    cost = request.form.get("fcost")
    if cost:
        updated_exhibition["cost"] = cost

    if updated_exhibition:
        db.exhibitions.update_one({"_id": ObjectId(exhibition_id)}, {"$set": updated_exhibition})

    return redirect(url_for("exhibition_detail", exhibition_id=exhibition_id))


@app.route("/delete/<exhibition_id>", methods=["POST"])
def delete(exhibition_id):
    """
    Deletes an exhibition from the database.
    """
    try:
        object_id = ObjectId(exhibition_id)
        result = db.exhibitions.delete_one({"_id": object_id})
        
        if result.deleted_count == 0:
            flash('Exhibition not found or already deleted.', 'error')
            return redirect(url_for('home'))

        flash('Exhibition successfully deleted.', 'success')
        return redirect(url_for("home"))

    except Exception as e:
        flash(f"An error occurred while deleting the exhibition: {str(e)}", 'error')
        return redirect(url_for("home"))


### Run Flask App ###
if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=int(FLASK_PORT))
