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
    def return_list(cls, limit, page):
        def to_json(x):
            return {
                'name': x.name
            }
        return {"applicants": list(map(lambda x: to_json(x), cls.query.order_by(cls.created_at).paginate(page, limit).items))}
