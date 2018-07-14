"""
モデル
"""
import datetime
from api import db
from passlib.hash import pbkdf2_sha256 as sha256

# スキーマ情報をmigrationから取得することで、modelに書かなくて済む
db.reflect()

"""
db.Modelを継承する
"""
class UserModel(db.Model):
    """
    DB定義
    """
    __tablename__ = 'users'

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
    def find_by_email(cls, email):
      return cls.query.filter_by(email = email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'email': x.email,
                'password': x.password
            }
        return {"users": list(map(lambda x: to_json(x), cls.query.all()))}
