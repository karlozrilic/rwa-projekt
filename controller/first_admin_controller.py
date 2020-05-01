from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from model import db
from model.user import User
from werkzeug.security import generate_password_hash
import datetime

api = Namespace(name='First time API', path='/api')

@api.route('/db-init')
class createDbFirstTime(Resource):
    @api.doc(description='First time database initalization', responses={200: 'Success'})
    def post(self):
        db.create_all()
        return {'message': 'Database succesfully initalized'}
    
@api.route('/add-first-admin')
@api.param('email', 'First admin email')
@api.param('first_name', 'First admin first name')
@api.param('last_name', 'First admin last name')
@api.param('password', 'First admin password')
class addFirstAdmin(Resource):
    @api.doc(description='Add first admin', responses={200: 'Success'})
    def post(self):
        admin = User(id=1, email=request.args.get('email'), first_name=request.args.get('first_name'), 
        last_name=request.args.get('last_name'), password=generate_password_hash(request.args.get('password')), admin=True)
        db.session.add(admin)
        db.session.commit()
        return {'message': 'First admin succesfuly added'}