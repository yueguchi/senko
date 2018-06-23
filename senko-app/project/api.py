# [参考] https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# JWT設定
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)


# DB設定
app.config.from_object('config.Config')
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


# tokenブラックリストチェック
import models
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


"""
TODO これやるとlogoutも影響しちゃう
"""
# @jwt.token_in_blacklist_loader
# def my_expired_token_callback():
#     return {
#         'status': 401,
#         'sub_status': 42,
#         'msg': 'The token has expired'
#     }, 401


# ルーティング設定
api = Api(app)
import resources
api.add_resource(resources.UserRegistration, '/users/regist')
api.add_resource(resources.UserLogin, '/users/login')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.TokenRefresh, '/users/refresh')
api.add_resource(resources.UserLogoutAccess, '/users/logout')
api.add_resource(resources.UserLogoutRefresh, '/users/refresh/logout')

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
