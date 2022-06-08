from flask import Flask, jsonify, request, abort
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
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 5
        end = (start + 5)
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]    
        return jsonify({
            'success': True,
            'plants': formatted_plants[start:end],
            'total plants': len(formatted_plants)
        })

    @app.route("/plants/<int:plant_id>")
    def get_plant(plant_id):
        plant = Plant.query.filter(plant_id == Plant.id).one_or_none()
        if plant is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'plant': plant.format()
            })

    return app