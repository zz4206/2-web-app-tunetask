from dotenv import load_dotenv
from flask import Flask, make_response
import os
import pymongo

load_dotenv('./.env')

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def show_home():
        # print("hello")
        response = make_response("Welcome to TuneTask!", 200) # put together an HTTP response with success code 200
        response.mimetype = "text/plain" # set the HTTP Content-type header to inform the browser that the returned document is plain text, not HTML
        connection = pymongo.MongoClient(os.getenv("MONGO_URI"))
        db = connection[os.getenv("MONGO_DBNAME")]
        try:
            connection.admin.command("ping")
            print("MongoDB connection successful")
        except Exception as e:
            print("MongoDB connection error:", e)
        return response # the return value is sent as the response to the web browser
    
    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "3000")
    app = create_app()
    app.run(port=FLASK_PORT)