import sqlalchemy
from .db_session import SqlAlchemyBase


class EmailCode(SqlAlchemyBase):
    __tablename__ = 'email_check'
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True, primary_key=True)
    code = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
