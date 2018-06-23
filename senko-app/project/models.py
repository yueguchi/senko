"""
モデル
"""
from api import db
from passlib.hash import pbkdf2_sha256 as sha256

"""
db.Modelを継承する
"""
class UserModel(db.Model):
    """
    DB定義
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    """
    passwordとpasswordをsha256が一致するか返す
    @return Bool
    """
    @staticmethod
    def verify_hash(password, hash):
        try:
            return sha256.verify(password, hash)
        except ValueError:
            return False

    """
    User登録
    """
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    """
    User名検索: first
    """
    @classmethod
    def find_by_username(self, username):
      return self.query.filter_by(username = username).first()

    @classmethod
    def return_all(self):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {"users": list(map(lambda x: to_json(x), self.query.all()))}


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(self, jti):
        query = self.query.filter_by(jti = jti).first()
        return bool(query)

