
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

DEBUG      = True
USERNAME   = 'andywrote'
SECRET_KEY = 'development_key'

SQLALCHEMY_DATABASE_URI = "postgresql://andywrote@localhost/andywrote"

## Flask-Security

SECURITY_LOGIN_USER_TEMPLATE = "security/login_user.html"

SECURITY_TRACKABLE     = True
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = 'development_salt'

# all these flags are set to False, their defaults in Flask-Security, 
# but might be useful if you ever want to make this a multi-user site

SECURITY_CONFIRMABLE  = False
SECURITY_REGISTERABLE = False
SECURITY_RECOVERABLE  = False
SECURITY_CHANGEABLE   = False


app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)

roles_users = db.Table('roles_users', 
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(80))
    email        = db.Column(db.String(255), unique=True)
    password     = db.Column(db.String(255))
    active       = db.Column(db.Boolean)

    last_login_at    = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip    = db.Column(db.String(40))
    current_login_ip = db.Column(db.String(40))
    login_count      = db.Column(db.Integer)

    roles        = db.relationship('Role', secondary=roles_users, 
                                   backref=db.backref('users', lazy='dynamic'))

# Set up Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()