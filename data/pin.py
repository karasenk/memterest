import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Pin(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'pin'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    mem_filename = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    alt = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    source = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    categories = orm.relation("Category",
                              secondary="pin_category_association",
                              backref="pin")
    boards = orm.relation("Board",
                          secondary="pin_board_association",
                          backref="pin")
