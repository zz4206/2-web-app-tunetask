from dotenv import load_dotenv
from flask import Flask, make_response, request, redirect, url_for, render_template
from flask_login import login_manager, login_user, UserMixin
import os
import pymongo

load_dotenv('./.env')
class User(UserMixin):
    pass

def create_app():
    app = Flask(__name__)
    connection = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = connection[os.getenv("MONGO_DBNAME")]

    @app.route('/')
    def show_home():
        
        connection = pymongo.MongoClient(os.getenv("MONGO_URI"))
        db = connection[os.getenv("MONGO_DBNAME")]

        try:
            connection.admin.command("ping")
            print("MongoDB connection successful")
        except Exception as e:
            print("MongoDB connection error:", e)

        return render_template('home.html')
    
    @app.route('/profile/<user>')
    def show_profile(user):
        tune_tasks = list(db.tune_tasks.find({"created_by":user}))
        if len(tune_tasks) == 0:
            return make_response("no tunetasks yet, make your first tunetask!", 200)

        # return make_response("all good", 200)
        return render_template('profile.html', user=user, collection=tune_tasks)
    
    @app.route('/search')
    def show_search():
        return render_template('search.html')
    
    @app.route('/search', methods=["POST"])
    def post_search():
        user = request.form["user"]
        tune_tasks= list(db.tune_tasks.find({"created_by":user}))
        # return make_response("hello", 200)
        if len(tune_tasks) == 0:
            return make_response("user not found", 200)
        return render_template('profile.html', user=user, collection=tune_tasks)
    
    @app.route('/login', methods=["GET"])
    def login():
        return render_template('login.html')
    
    return app


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "3000")
    app = create_app()
    app.run(port=FLASK_PORT)