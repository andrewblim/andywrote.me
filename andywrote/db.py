
from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin
import datetime

# Set up database and object mapping

db = SQLAlchemy(app)

users_roles = db.Table(
    'users_roles', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

posts_authors = db.Table(
    'posts_authors', 
    db.Column('post_id',   db.Integer, db.ForeignKey('post.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('user.id'))
)

posts_tags = db.Table(
    'posts_tags', 
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id',  db.Integer, db.ForeignKey('tag.id'))
)

class Role(db.Model, RoleMixin):

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(200))

class User(db.Model, UserMixin):

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(80))
    display_name = db.Column(db.String(80), unique=True)
    email        = db.Column(db.String(200), unique=True)
    password     = db.Column(db.String(200))
    active       = db.Column(db.Boolean)

    last_login_at    = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip    = db.Column(db.String(40))
    current_login_ip = db.Column(db.String(40))
    login_count      = db.Column(db.Integer)

    roles = db.relationship(
        'Role', 
        secondary=users_roles, 
        backref=db.backref('users', lazy='dynamic')
    )

    def __repr__(self):
        return '<User %d: %s>' % (self.id, self.email)

class Post(db.Model):

    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(300))
    slug       = db.Column(db.String(80), unique=True)
    body       = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    authors = db.relationship(
        'User', 
        secondary=posts_authors,
        backref=db.backref('posts', lazy='dynamic')
    )

    tags = db.relationship(
        'Tag',
        secondary=posts_tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title, slug, body, 
                 authors=[], tags=[],
                 created_at=datetime.datetime.now(),
                 updated_at=datetime.datetime.now()):
        self.title      = title
        self.slug       = slug
        self.body       = body
        self.authors    = authors
        self.tags       = tags
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Post %d: %s>' % (self.id, self.title)


class Tag(db.Model):

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    slug = db.Column(db.String(80), unique=True)

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

    def __repr__(self):
        return '<Tag %d: %s>' % (self.id, self.name)