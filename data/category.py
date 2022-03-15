import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pin_table = sqlalchemy.Table(
        'pin_category_association',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column('pin', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('pin.id')),
        sqlalchemy.Column('category', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('category.id')))
