import datetime
from sqlalchemy import *
from migrate import *

meta = MetaData()
 
users = Table(
        'users', meta,
        Column('id', Integer, primary_key=True, nullable=False),
        Column('email', String(255), nullable=False, unique=True),
        Column('username', String(255), nullable=False, unique=False),
        Column('password', String(120), nullable=False, unique=False),
        Column('created_at', DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP')),
        Column('updated_at', DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    users.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    users.drop()
