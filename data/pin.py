import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Pin(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'pin'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    alt = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    categories = orm.relation("Category",
                              secondary="pin_category_association",
                              backref="pins")
    boards = orm.relation("Board",
                          secondary="pin_board_association",
                          backref="pins")
