import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Anecdote(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'anecdote'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    source = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    categories = orm.relation("Category",
                              secondary="anecdote_category_association",
                              backref="anecdotes")
    boards = orm.relation("Board",
                          secondary="anecdote_board_association",
                          backref="anecdotes")
