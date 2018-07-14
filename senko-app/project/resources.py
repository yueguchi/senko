"""
コントローラー
"""
import redis
import datetime
from datetime import timedelta
from flask_restful import Resource, reqparse
from models import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

# 使い終わったtokenはredisに期限つき自動削除で突っ込む
revoked_store = redis.StrictRedis(host='senko-redis', port=6379, db=0, decode_responses=True)

parser = reqparse.RequestParser()
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('username', help = 'This field cannot be blank', required = False)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

# ブラックリストreddisの期限(1ヶ月)
ACCESS_EXPIRES = timedelta(days=30)


"""
登録
"""
class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {'message': 'User {} already exists'. format(data['email'])}

        new_user = UserModel(
            email = data['email'],
            username = data['username'],
            password = UserModel.generate_hash(data['password']),
            # TODO これがあるとエラー...
            # created_at = datetime.datetime.now,
            # updated_at = datetime.datetime.now
        )
        new_user.save_to_db()

        access_token = create_access_token(identity = data['email'])
        refresh_token = create_refresh_token(identity = data['email'])

        return {
            'message': 'User {} was created'.format(data['email']),
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201


"""
ログイン
"""
class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_email(data['email'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}, 401
        elif not UserModel.verify_hash(data['password'], current_user.password):
            return {'message': 'Invalid LoginError.'}, 401

        access_token = create_access_token(identity = data['email'])
        refresh_token = create_refresh_token(identity = data['email'])

        return {
            'message': 'Logged in as {}'.format(current_user.email),
            'access_token': access_token,
            'refresh_token': refresh_token
        }


"""
リフレッシュトークン
Authorizationにrefresh_tokenを設定してrequestすることで、最新のaccess_tokenを返却する
"""
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    @jwt_required
    def get(self):
        return UserModel.return_all()


"""
ログアウト
redisに今使っているtokenを無効なtokenとして格納する
"""
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_store.set(jti, 'true', ACCESS_EXPIRES)
        return {'message': 'Access token has been revoked'}
