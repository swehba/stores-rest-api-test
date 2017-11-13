from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    """
    This resource allows users to register by sending a POST request with their username and password.
    """

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="The user's login identifier. Required.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="The user's password. Required.")

    def post(self):
        data = UserRegister.parser.parse_args()
        username = data['username']
        password = data['password']

        if UserModel.find_by_username(username):
            return {'message': f'A user with the username [{username}] already exists.'}, 400
        else:
            user = UserModel(**data)
            user.save_to_db()
            return {'message': f'A user with username [{username}] was successfully created.'}, 201


class UserResource(Resource):
    pass
