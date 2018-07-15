import datetime
from sqlalchemy import *
from migrate import *

meta = MetaData()
 
applicants = Table(
        'applicants', meta,
        Column('id', Integer, primary_key=True, nullable=False),
        Column('name', String(255), nullable=False, unique=False),
        Column('email', String(255), nullable=False, unique=False),
        Column('sex', Integer, nullable=True),
        Column('birth', Date, nullable=True),
        Column('address', String(255), nullable=True),
        Column('zip1', String(255), nullable=True),
        Column('zip2', String(255), nullable=True),
        Column('final_education', String(255), nullable=True),
        Column('reason', String(2000), nullable=True),
        Column('janome_word', Text, nullable=True),
        Column('created_at', DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP')),
        Column('updated_at', DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    applicants.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    applicants.drop()
