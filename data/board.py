import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Board(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'board'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    pins_table = sqlalchemy.Table(
        'pin_board_association',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column('pin', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('pin.id')),
        sqlalchemy.Column('board', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('board.id')))
