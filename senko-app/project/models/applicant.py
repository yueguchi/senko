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


    """
    削除
    """
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    """
    id検索
    """
    @classmethod
    def find_by_id(cls, applicantId):
        return cls.query.filter_by(id = applicantId).first()


    @classmethod
    def return_list(cls, limit, page):
        def to_json(x):
            return {
                'id': x.id,
                'name': x.name,
                'sex': x.sex,
                'email': x.email,
                'birth': x.birth.isoformat(),
                'address': x.address,
                'zip1': x.zip1,
                'zip2': x.zip2,
                'final_education': x.final_education,
                'reason': x.reason,
                'janome_word': x.janome_word,
                'created_at': x.created_at.isoformat(),
                'updated_at': x.updated_at.isoformat()
            }
        return {"applicants": list(map(lambda x: to_json(x), cls.query.order_by(cls.created_at).paginate(page, limit).items))}
