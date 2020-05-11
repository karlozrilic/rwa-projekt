from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from model import db
from model.pizza import Pizzas
from service.auth_service import authenticated, authenticated_admin
from service.log_service import trace

api = Namespace(name='Admin Pizza API', path='/api/pizzas', decorators=[trace])

pizza_create = api.model('CreatePizza', {
    'naziv': fields.String(required=True, description='Naziv'),
    'sastojci': fields.String(required=True, description='Sastojci'),
    'cijena': fields.String(required=True, description='Cijena')
})

pizza_dto = api.model('Pizza', {
    'id': fields.Integer(required=True, description='ID'),
    'naziv': fields.String(required=True, description='Naziv'),
    'sastojci': fields.String(required=True, description='Sastojci'),
    'cijena': fields.String(required=True, description='Cijena'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'created': fields.DateTime(required=True, description='Created'),
    'updated': fields.DateTime(required=True, description='Updated')
})


@api.route('/')
class PizzaListResource(Resource):
  
    @api.doc(description='Create pizza', responses={201: 'Success', 401: 'Unauthorized'}, security='Bearer Auth')
    @api.expect(pizza_create)
    @api.marshal_with(pizza_dto)
    @authenticated_admin
    def post(current_user,self):
        try:
            sastojci = api.payload['sastojci']
        except:
            sastojci = None 

        new_pizza = Pizzas(naziv=api.payload['naziv'], sastojci=sastojci, cijena=False, user_id=current_user.id)
        db.session.add(new_pizza)
        db.session.commit()
        
        return new_pizza, 201

    @api.doc(description='Get all pizzas', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_list_with(pizza_dto)
    @api.param('sastojci', description='Sastojci', type='string')
    @api.param('cijena', description='Cijena', type='integer')
    @api.param('naziv', description='Naziv', type='string')
    @authenticated_admin
    def get(current_user, self):
        
        sastojci = request.args.get('sastojci')
        naziv = request.args.get('naziv')

        try:
            cijena = int(request.args.get('cijena'))
        except:
            cijena = None
        
        pizzas = Pizzas.query.filter_by(user_id=current_user.id)
        
        if sastojci and cijena and naziv:
            print(f'..filtering by sastojci {sastojci}, cijena {cijena} and naziv {naziv}')
            pizzas = pizzas.filter(Pizzas.sastojci.ilike('%'+sastojci+'%')).filter(Pizzas.cijena.ilike('%'+str(cijena)+'%')).filter(Pizzas.naziv.ilike('%'+naziv+'%'))
            #pizzas = pizzas.filter_by(sastojci=sastojci, cijena=cijena, naziv=naziv)
        elif sastojci and cijena:
            print(f'..filtering by sastojci {sastojci} and cijena {cijena}')
            pizzas = pizzas.filter(Pizzas.sastojci.ilike('%'+sastojci+'%')).filter(Pizzas.cijena.ilike('%'+str(cijena)+'%'))
            #pizzas = pizzas.filter_by(sastojci=sastojci, cijena=cijena)
        elif sastojci and naziv:
            print(f'..filtering by sastojci {sastojci} and naziv {naziv}')
            pizzas = pizzas.filter(Pizzas.sastojci.ilike('%'+sastojci+'%')).filter(Pizzas.naziv.ilike('%'+naziv+'%'))
            #pizzas = pizzas.filter_by(sastojci=sastojci, naziv=naziv)
        elif cijena and naziv:
            print(f'..filtering by cijena {cijena} and naziv {naziv}')
            pizzas = pizzas.filter(Pizzas.cijena.ilike('%'+str(cijena)+'%')).filter(Pizzas.naziv.ilike('%'+naziv+'%'))
            #pizzas = pizzas.filter_by(cijena=cijena, naziv=naziv)
        elif sastojci:
            print(f'..filtering by sastojci {sastojci}')
            pizzas = pizzas.filter(Pizzas.sastojci.ilike('%'+sastojci+'%'))
            #pizzas = pizzas.filter_by(sastojci=sastojci)
        elif cijena:
            print(f'..filtering by cijena {cijena}')
            pizzas = pizzas.filter(Pizzas.cijena.ilike('%'+str(cijena)+'%'))
            #pizzas = pizzas.filter_by(cijena=cijena)
        elif naziv:
            print(f'..filtering by naziv {naziv}')
            pizzas = pizzas.filter(Pizzas.naziv.ilike('%'+naziv+'%'))
            #pizzas = pizzas.filter_by(naziv=naziv)
   
        output = []

        for pizza in pizzas:
            pizza_data = {}
            pizza_data['id'] = pizza.id
            pizza_data['naziv'] = pizza.naziv
            pizza_data['sastojci'] = pizza.sastojci
            pizza_data['cijena'] = pizza.cijena
            pizza_data['user_id'] = pizza.user_id            
            pizza_data['created'] = pizza.created
            pizza_data['updated'] = pizza.updated
            output.append(pizza_data)

        return output     

@api.route('/<id>')
@api.param('id', 'ID')
@api.response(404, 'Pizza not found.')
class PizzaResource(Resource):
    @api.doc(description='Get pizza', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_with(pizza_dto)
    @authenticated_admin
    def get(current_user, self, id):
        pizza = Pizzas.query.filter_by(id=id, user_id=current_user.id).first()
        if not pizza:
            api.abort(404)
        else:
            return pizza  

    @api.doc(description='Update pizza', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_with(pizza_dto)
    @api.param('sastojci', description='Sastojci', type='string')
    @api.param('cijena', description='Cijena', type='integer')
    @authenticated_admin
    def put(current_user, self, id):
        pizza = Pizzas.query.filter_by(id=id, user_id=current_user.id).first()
        if not pizza:
            api.abort(404)
        else:
            sastojci = request.args.get('sastojci')
            cijena = request.args.get('cijena')

            if sastojci:
                pizza.sastojci = sastojci

            if cijena:
                pizza.cijena = cijena

            db.session.commit()
            return pizza             

    @api.doc(description='Delete pizza', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @authenticated_admin
    def delete(current_user, self, id):
        pizza = Pizzas.query.filter_by(id=id, user_id=current_user.id).first()
        if not pizza:
            api.abort(404)
        else:
            db.session.delete(pizza)
            db.session.commit()
            return {'message':'Pizza has been deleted'}         