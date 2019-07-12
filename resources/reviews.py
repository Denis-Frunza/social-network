import  json

from flask import jsonify, Blueprint, url_for, make_response
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with
from auth import  auth

import models

user_field = {
    'id':fields.Integer,
    'username': fields.String,
    'email':fields.String,
    'joined_at':fields.String
}

field_name = {
    'username': fields.String,
}

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        users = [marshal(user, user_field)for user in models.User.select(models.User.id, models.User.username, models.User.email, models.User.joined_at )]
        return {'users':users}
    
    def post(self):
        args = self.reqparse.parse_args()
        if args.get('password') == args.get('verify_password'):
            user = models.User.create_user(username = args.get('username'),
                email = args.get('email'),
                password = args.get('password')
                )
            return marshal(user, field_name),201
        return make_response(json.dumps({'error': 'password and  password verification do not match'}),400)


 
class Users(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name provided',
            location = ['form', 'json']
            )
        self.reqparse.add_argument(
            'url',
            required=True,
            help='No url provided',
            location=['form', 'json'],
            type=inputs.url
            )
        super().__init__()

    @auth.login_required
    def delete(self, id):
        query = models.User.delete().where(models.User.id==id)
        query.execute()
        return '', 204, {'Location': url_for('resources.reviews.reviews')}


review_api = Blueprint('resources.reviews', __name__)
api = Api(review_api)
api.add_resource(
    UserList,
    '/api/v1/users',
    endpoint='reviews'
    )

api.add_resource(
    Users,
    '/api/v1/users/<int:id>',
    endpoint='review'
)

