#!/usr/bin/env python3

"""
Pinkberries flask-based web application.
"""

import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

# Load environment variables
load_dotenv()

# Create and configure Flask app
def create_app():
    app = Flask(__name__)

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

    return app, db


app, db = create_app()


@app.route("/")
def home():
    return render_template("home.html") 


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.users.find_one({"username": username, "password": password})

        if user:
            login_user(User(str(user["_id"]), user["username"]))
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        
        flash("Invalid credentials", "danger")
    
    return render_template("login.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/filter", methods=["GET"])
def filter_exhibitions():
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
            return " Invalid date format, Use YYYY-MM-DD."

    # Fetch results from MongoDB
    results = list(db.exhibits.find(query, {"_id": 0}))

    return render_template("filtered_results.html", results=results)

@app.route("/create_exhibit", methods=["POST"])
def create_exhibit():
    title = request.form["ftitle"]
    dates = request.form["fdates"]
    location = request.form["flocation"]
    cost = request.form["fcost"]
    artist = request.form["fartist"]
    art_style = request.form["fart_style"]
    art_medium = request.form["fart_medium"]
    event_type = request.form["fevent_type"]
    description = request.form["fdescription"]
    image_url = request.form["fimage_url"]
    created_by = request.form["created_by"]

    exhibition = {
        "Exhibition Title": title,
        "Dates": dates,
        "Location": location,
        "Cost": cost,
        "Artist": artist,
        "Art Style": art_style,
        "Art Medium": art_medium,
        "Event Type": event_type,
        "Description": description,
        "Image_url": image_url,
        "Created_by": created_by,
        "created_at": datetime.datetime.utcnow(),
    }

    db.exhibits.insert_one(exhibition)
    return redirect(url_for("home"))

@app.route("/edit/<post_id>")
def edit(post_id):
    exhibition = db.exhibits.find_one({"_id": ObjectId(post_id)})
    return render_template("edit.html", exhibition=exhibition)

@app.route("/edit/<post_id>", methods=["POST"])
def edit_post(post_id):
    title = request.form["ftitle"]
    dates = request.form["fdates"]
    location = request.form["flocation"]
    cost = request.form["fcost"]
    artist = request.form["fartist"]
    art_style = request.form["fart_style"]
    art_medium = request.form["fart_medium"]
    event_type = request.form["fevent_type"]
    description = request.form["fdescription"]
    image_url = request.form["fimage_url"]
    created_by = request.form["created_by"]

    exhibition = {
        "Exhibition Title": title,
        "Dates": dates,
        "Location": location,
        "Cost": cost,
        "Artist": artist,
        "Art Style": art_style,
        "Art Medium": art_medium,
        "Event Type": event_type,
        "Description": description,
        "Image_url": image_url,
        "Created_by": created_by,
        "created_at": datetime.datetime.utcnow(),
    }

    db.exhibits.update_one({"_id": ObjectId(post_id)}, {"$set": exhibition})
    return redirect(url_for("home"))

@app.route("/delete/<post_id>")
def delete(post_id):
    db.exhibits.delete_one({"_id": ObjectId(post_id)})
    return redirect(url_for("home"))

@app.route("/delete-by-content/<Created_by>/<Exhibition_title>", methods=["POST"])
def delete_by_content(Created_by, Exhibition_title):
    db.exhibits.delete_many({"Created_by": Created_by, "Exhibition Title": Exhibition_title})
    return redirect(url_for("home"))

### Run Flask App ###
if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")
    app.run(port=int(FLASK_PORT), debug=True)