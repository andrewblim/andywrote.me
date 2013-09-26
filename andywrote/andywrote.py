
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask.ext.login import current_user
from flask.ext.security.utils import encrypt_password

from flask_wtf import Form
from wtforms import StringField, TextAreaField, validators

import bleach
import datetime
import re

DEBUG      = True
USERNAME   = 'andywrote'
SECRET_KEY = 'development_key'

SQLALCHEMY_DATABASE_URI = "postgresql://andywrote@localhost/andywrote"

## Flask-Security config

SECURITY_LOGIN_USER_TEMPLATE = "security/login_user.html"

SECURITY_TRACKABLE     = True
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = 'developmentsalt'

# all these flags are set to False, their defaults in Flask-Security, 
# but might be useful if you ever want to make this a multi-user site

SECURITY_CONFIRMABLE  = False
SECURITY_REGISTERABLE = False
SECURITY_RECOVERABLE  = False
SECURITY_CHANGEABLE   = False

# Set up app

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

# Schema/models

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
    'tags', 
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
        backref=db.backref('tags', lazy='dynamic')
    )

    def __init__(self, title, body, authors=[], tags=[],
                 created_at=datetime.datetime.now(),
                 updated_at=datetime.datetime.now()):
        self.title      = title
        self.body       = body
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Post %d: %s>' % (self.id, self.title)


class Tag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %d: %s>' % (self.id, self.name)

# Set up Flask-Security

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Functions

def create_user(email, name, password):
    user_datastore.create_user(
        email=email,
        name=name,
        password=encrypt_password(password)
    )

# Forms

class WriteForm(Form):
    title    = StringField(u'Title', \
        [validators.Length(min=1, max=300, \
            message=u'Your title must contain at least 1 character and no more than 300 characters.') \
        ])
    tag_list = StringField(u'Tags')
    body     = TextAreaField(u'Body')

# Routes

@app.route('/')
def about():
    if current_user.is_anonymous():
        email = None
    else:
        email = current_user.email
    return render_template('about.html', email=email)

@app.route('/blog/')
def blog():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('blog/index.html', posts=posts)

@app.route('/blog/write')
@login_required
def blog_write():
    return render_template('blog/write.html', form=WriteForm())

@app.route('/blog/write', methods=["POST"])
@login_required
def blog_submit_post():
    form = WriteForm()
    if form.validate_on_submit():
        title    = bleach.clean(form.title.data)
        tag_list = bleach.clean(form.tag_list.data)
        tag_list = re.sub('\s+', ' ', tag_list)
        tag_list = re.split('\s?,\s?', tag_list)
        body  = bleach.clean(form.body.data)

        new_post = Post(title=title, body=body, authors=[current_user])
        for tag_name in tag_list:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag is None:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            new_post.tags.append(tag)
        db.session.add(new_post)
        db.session.commit()
        flash(u'Successfully posted: %s' % form.title.data, category='blog')
        return redirect('/blog')

    else:
        flash(u'There were errors in your submission, please check below.')
    return render_template('blog/write.html', form=form)

@app.route('/blog/manage')
@login_required
def blog_manage():
    return render_template('blog/manage.html')

if __name__ == '__main__':
    app.run()