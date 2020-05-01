from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from model import db
from model.pizza import Pizzas
from werkzeug.security import generate_password_hash
import datetime
from service.auth_service import authenticated

api = Namespace(name='User API', path='/api')

@api.route('/list-pizzas')
class listPizzas(Resource):
    @api.doc(description='List all pizzas', responses={200: 'Success', 401: 'Unauthorized'}, security='Bearer Auth')
    @authenticated
    def get(self, current_user):
        pizzas = Pizzas.query.all()
        if pizzas == []:
            return "There is no pizzas in database"
        else:
            output = []
            for pizza in pizzas:
                pizza_data = {}
                pizza_data['id'] = pizza.id
                pizza_data['naziv'] = pizza.naziv
                pizza_data['sastojci'] = pizza.sastojci
                pizza_data['cijena'] = pizza.cijena 
                output.append(pizza_data)
            return output