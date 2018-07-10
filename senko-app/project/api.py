# [参考] https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

# JWT設定
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

# DB設定
app.config.from_object('config.Config')
db = SQLAlchemy(app)

# sqlarchemy-migrateに移行した
# @app.before_first_request
# def create_tables():
#     db.create_all()


# tokenブラックリストチェック
import redis
from datetime import timedelta
# 使い終わったtokenはredisに期限つき自動削除で突っ込む
revoked_store = redis.StrictRedis(host='senko-redis', port=6379, db=0, decode_responses=True)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is None:
        return False
    return True


# access_tokenに付加情報をつけたい時に使う。@jwt_requiredの中でclaims = get_jwt_claims() -> claims['hello']で参照できる。
# @jwt.user_claims_loader
# def add_claims_to_access_token(identity):
#     return {
#         'hello': identity,
#         'foo': ['bar', 'baz']
#     }

# ルーティング設定
api = Api(app)
import resources
api.add_resource(resources.UserRegistration, '/users/regist')
api.add_resource(resources.UserLogin, '/users/login')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.TokenRefresh, '/users/refresh')
api.add_resource(resources.UserLogoutAccess, '/users/logout')

# エラーハンドラ
@app.errorhandler(404)
def error_handler(error):
    msg = 'Error: {code}'.format(code=error.code)
    return jsonify({"message": msg}), 404


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
