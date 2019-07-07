import datetime

#from flask.ext.bcrypt import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
#from flask.ext.login import UserMixin
from flask_login import UserMixin
from peewee import *


DATABASE = SqliteDatabase('social.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    bio = TextField(default='')

    class Meta:
        database = DATABASE

    def get_posts(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):
        return Post.select().where(
            (Post.user << self.following()) |
            (Post.user == self)
            )

    def following(self):
        """ The users who we follow"""
        return(
            User.select().join(Relationship, on=Relationship.to_user).where(
                (Relationship.from_user == self)
                )
        )

    def followers(self):
        """ Get users who following the current user"""
        return( User.select().join(Relationship, on=Relationship.from_user).where(
            (Relationship.to_user == self)

            )
        )
    
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        model = User,
        backref = 'posts'
        )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)

class Relationship(Model):
    from_user = ForeignKeyField(User, backref='relationships')
    to_user = ForeignKeyField(User, backref='related_to')

    class Meta:
        database = DATABASE
        indexes = (
            (('from_user', 'to_user'), True),

        )

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Relationship], safe=True)
    DATABASE.close()