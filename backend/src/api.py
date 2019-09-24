import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()

    # ROUTES

    @app.route('/drinks', methods=['GET'])
    def get_drinks():
        '''Returns all available drinks'''
        selection = Drink.query.all()

        drinks = [drink.short() for drink in selection]
        if not drinks:
            abort(404)
        return jsonify({
            'success': True,
            'drinks': drinks
        })

    @app.route('/drinks-detail', methods=['GET'])
    @requires_auth('get:drinks-detail')
    def get_drink_detail(payload):
        """Returns drinks and the details for the recipes"""
        selection = Drink.query.all()

        drinks = [drink.long() for drink in selection]
        if not drinks:
            abort(404)
        return jsonify({
            'success': True,
            'drinks': drinks
        })

    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def create_drink(paylod):
        """Creates a new drink"""
        body = request.get_json()
        if not body:
            abort(400)

        if 'title' not in body or 'recipe' not in body:
            abort(400)

        new_drink = Drink(title=body['title'],
                          recipe=json.dumps(body['recipe']))

        try:
            new_drink.insert()
        except KeyError:
            abort(422)

        selection = Drink.query.all()

        drinks = [drink.long()
                  for drink in selection if drink.id == new_drink.id]
        if not drinks:
            abort(404)
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 201

    @app.route('/drinks/<int:drink_id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def update_drink(payload, drink_id):
        """Updates a drink with the provided ID"""
        drink = Drink.query.get(drink_id)
        if not drink:
            abort(404)
        body = request.get_json()

        if 'title' in body:
            drink.title = body['title']
        if 'recipe' in body:
            new_recipe = body['recipe']
            drink.recipe = json.dumps(new_recipe)

        try:
            drink.update()
        except SystemError:
            abort(500)

        selection = Drink.query.filter_by(id=drink.id)
        drinks = [drink.long() for drink in selection]
        return jsonify({
            'success': True,
            'drinks': drinks
        })

    @app.route('/drinks/<int:drink_id>', methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drink(payload, drink_id):
        """Deletes the drink with the provided ID"""
        drink = Drink.query.get(drink_id)
        if not drink:
            abort(404)

        try:
            drink.delete()
        except SystemError:
            abort(400)

        return jsonify({
            'success': True,
            'delete': drink.id
        })

    # Error Handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request - check parameters"
        }), 400

    @app.errorhandler(401)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "not authorized"
        }), 401

    @app.errorhandler(403)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(404)
    def no_results(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable - check parameters"
        }), 422

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "unknown error - try again later"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        """Returns a JSON response for Authentication errors"""
        return jsonify({
            "success": False,
            "error": error.code,
            "message": error.description
        }), error.code

    return app
