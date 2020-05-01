from flask_restplus import Api

from .first_admin_controller import api as first
from .auth_controller import api as auth
from .admin_pizza_controller import api as admin_pizza
from .user_pizza_controller import api as pizza
from .user_controller import api as user

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'Basic Auth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    title='Pizzas API',
    version='1.0.0',
    description='Sveučilište u Zadru - Studij informacijskih tehnologija - Razvoj web aplikacija',
    contact='kazrile@gmail.com',
    authorizations=authorizations,
    serve_challenge_on_401=False
)

api.add_namespace(first)
api.add_namespace(auth)
api.add_namespace(admin_pizza)
api.add_namespace(pizza)
api.add_namespace(user)