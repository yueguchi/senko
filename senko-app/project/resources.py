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
            password = data['password']
        )
        try:
            new_user.save_to_db()
            return {
                'message': 'User {} was created'.format(data['username'])
            }, 201
        except:
            return {'message': 'Something went wrong'}, 500

"""
ログイン
"""
class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        return data


"""
応募者RESTクラス
"""
class Applicant(Resource):
    def get(self):
        return {'applicant': [1, 2, 3]}, 200
    def post(self):
        return {'msg': 'created'}, 201
    def patch(self):
        return {'msg': 'modified'}, 200
    def delete(self):
        return {'msg': 'no content'}, 204
