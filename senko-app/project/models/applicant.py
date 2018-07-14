"""
モデル
"""
import datetime
from api import db

# スキーマ情報をmigrationから取得することで、modelに書かなくて済む
db.reflect()

"""
db.Modelを継承する
"""
class ApplicantModel(db.Model):
    """
    DB定義
    """
    __tablename__ = 'applicants'


    """
    登録
    """
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'name': x.username
            }
        return {"users": list(map(lambda x: to_json(x), cls.query.all()))}
