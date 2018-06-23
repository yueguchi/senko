"""
コントローラー
"""
from flask_restful import Resource, reqparse
from models import UserModel

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


"""
登録
"""
class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'. format(data['username'])}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()

            # access_token = create_access_token(identity = data['username'])
            # refresh_token = create_refresh_token(identity = data['username'])

            return {
                'message': 'User {} was created'.format(data['username'])
                # 'access_token': access_token,
                # 'refresh_token': refresh_token
            }, 201
        except:
            return {'message': 'Something went wrong'}, 500

"""
ログイン
"""
class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user or not UserModel.verify_hash(data['password'], current_user.password):
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 401

        # access_token = create_access_token(identity = data['username'])
        # refresh_token = create_refresh_token(identity = data['username'])

        return {
            'message': 'Logged in as {}'.format(current_user.username)
            # 'access_token': access_token,
            # 'refresh_token': refresh_token
        }

class AllUsers(Resource):
    # @jwt_required
    def get(self):
        return UserModel.return_all()

"""
応募者RESTクラス
"""
class Applicant(Resource):
    # @jwt_required
    def get(self):
        return {'applicant': [1, 2, 3]}, 200
    # @jwt_required
    def post(self):
        return {'msg': 'created'}, 201
    # @jwt_required
    def patch(self):
        return {'msg': 'modified'}, 200
    # @jwt_required
    def delete(self):
        return {'msg': 'no content'}, 204
