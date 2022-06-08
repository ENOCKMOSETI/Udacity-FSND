from flask import Flask, jsonify
from models import setup_db, Plant
from flask_cors import CORS

def create_app(test_Config=None):
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, DELETE, OPTIONS"
        return response

    @app.route("/plants")
    def get_plants():
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]    
        return jsonify({
            'success': True,
            'plants': formatted_plants
        })
    return app