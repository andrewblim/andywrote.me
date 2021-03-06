
from flask import request, session, g, redirect, url_for, \
    abort, render_template, flash
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required
from flask.ext.login import current_user
from flask.ext.security.utils import encrypt_password

from alembic.config import Config
from alembic import command

from wtforms.validators import ValidationError
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed

import bleach
import os
from smartypants import smartypants
from lxml import etree
import re
import sqlalchemy
from getpass import getpass

from app import app, config_app_heroku
from db import db, Role, User, Post, Tag, users_roles, posts_authors, posts_tags
from forms import WriteForm

# Set up Flask-Security

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Functions/helper definitions

allowed_tags_body = [
    'a', 
    'abbr', 
    'acronym', 
    'address',
    'b', 
    'blockquote', 
    'br',
    'cite',
    'code', 
    'del',
    'div',
    'em', 
    'h3', 
    'h4', 
    'h5', 
    'h6', 
    'i', 
    'li', 
    'ol',
    'p',
    'pre', 
    'q',
    'strong',
    'ul',
]


def create_user(**kwargs):
    if 'email' not in kwargs:
        kwargs['email'] = raw_input('Email address: ')
    if 'name' not in kwargs:
        kwargs['name'] = raw_input('Name: ')
    if 'display_name' not in kwargs:
        kwargs['display_name'] = raw_input('Name to display (blank for the same as above): ')
        if kwargs['display_name'] == '':
            kwargs['display_name'] = kwargs['name']
    if 'password' not in kwargs:
        kwargs['password'] = getpass('Password: ')
    kwargs['password'] = encrypt_password(kwargs['password'])
    user_datastore.create_user(**kwargs)
    db.session.commit()

def delete_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is not None:
        user_datastore.delete_user(user)
        db.session.commit()
    else:
        raise sqlalchemy.orm.exc.NoResultFound('No user found with email %s' % email)

def delete_user_by_display_name(display_name):
    user = User.query.filter_by(display_name=display_name).first()
    if user is not None:
        user_datastore.delete_user(user)
        db.session.commit()
    else:
        raise sqlalchemy.orm.exc.NoResultFound('No user found with display name %s' % display_name)

def delete_all_records():
    for user in User.query:
        user_datastore.delete_user(user)
    Post.query.delete()
    Tag.query.delete()
    db.session.commit()


# generate_slug
# Used to generate stubs for URLs, i.e. a post titled "This is my fancy pants
# post" might have a slug of this-is-my-fancy-pants-post. 

def generate_slug(text):
    text = re.sub('\s', '-', text)
    text = re.sub('&[^;]*;', '-', text) # remove HTML escaped entities
    text = re.sub('[^A-Za-z0-9\-]', '', text)
    return text

# generate_slug_for_post
# Tries to attach a stem "-1, "-2" etc. if there is already a Post with said
# slug. 

def generate_slug_for_post(text, field_length=80):
    slug_stem = generate_slug(text)
    slug_stem = slug_stem.lower()[:(field_length-5)]
    slug_number = 1
    slug = slug_stem
    while Post.query.filter_by(slug=slug).first() is not None:
        slug = "%s-%d" % (slug_stem, slug_number)
        slug_number += 1
    return slug

# find_or_create_tag_by_name
# Useful in creating/editing posts. Does not commit it to the db session, you
# should do that separately. 

def find_or_create_tag_by_name(tag_name, field_length=80):
    slug_tag = generate_slug(tag_name)
    if len(slug_tag) > field_length:
        form.tag_list.errors.append("Couldn't generate a slug for tag %s - try a different title." % tag_name)
        raise ValidationError
    tag = Tag.query.filter_by(slug=slug_tag).first()
    if tag is None:
        tag = Tag(name=tag_name, slug=slug_tag)
        db.session.add(tag)
    return tag


# clean_post_text
# Returns sanitized version of text, raises ValidationError if it doesn't parse
# into valid HTML. 

def clean_post_text(text, convert_breaks=False, use_smartypants=False):
    if convert_breaks:
        text = re.sub('\n\n+', '\n</p>\n<p>\n', text)
        text = "<p>\n%s\n</p>" % text
        text = re.sub(r'<p><h([1-6])>', r'<h\1>', text)
        text = re.sub(r'</\s*h([1-6])><\/p>', r'</h\1>', text)
    if use_smartypants:
        text = smartypants(text)
    try:
        text_parse = "<article>%s</article>"
        etree.fromstring(text_parse)
    except etree.XMLSyntaxError:
        form.text.errors.append("Body appears to be improper HTML (forget to close a tag?).")
        raise ValidationError
    return text

# blog_submit_post
# This is used both by /blog/write to generate new posts and by
# /blog/posts/<post-slug>/edit to edit and save existing posts. 

def blog_submit_post(post=None):

    form = WriteForm()
    if form.is_submitted():

        # pre-validation sanitization
        title    = bleach.clean(form.title.data, tags=[])
        tag_list = bleach.clean(form.tag_list.data, tags=[])
        tag_list = re.sub('\s+', ' ', tag_list).strip()
        body     = bleach.clean(form.body.data, tags=allowed_tags_body)

        if form.validate():
            try:

                # Convert line breaks/apply smartypants as needed

                body = clean_post_text(body,
                                       form.convert_breaks.data,
                                       form.use_smartypants.data)
                if form.use_smartypants.data:
                    title = smartypants(title)

                # Get list of tag names

                tag_list = set(re.split('\s?,\s?', tag_list))
                if len(tag_list) == 1 and '' in tag_list:
                    tag_list = set([])

                # Generate slug for post if it's not specified. It's a ValidationError to
                # have a duplicate slug, though generate_slug_for_post will try to get
                # around that. 

                if form.slug.data == '':
                    slug_title = generate_slug_for_post(title)
                    if len(slug_title) > 80:
                        form.title.errors.append("Couldn't generate a slug from title - try a different title.")
                        raise ValidationError
                else: 
                    slug_title = form.slug.data
                    if post is None and Post.query.filter_by(slug=form.slug.data).first() is not None:
                        form.slug.errors.append("There is already a post with that slug")
                        raise ValidationError

                # Add the post, if it's a new one. 

                if post is None:
                    new_post = Post(title=title, 
                                    body=body, 
                                    slug=slug_title,
                                    authors=[current_user])
                    for tag_name in tag_list:
                        tag = find_or_create_tag_by_name(tag_name)
                        new_post.tags.append(tag)
                    db.session.add(new_post)

                # If it's not new, edit post

                else:
                    post.title     = title
                    post.body      = body
                    post.slug      = slug_title
                    post.authors   = [current_user]
                    post.published = form.published.data
                    tags_removed   = filter(lambda x: x.name not in tag_list, post.tags)
                    post.tags      = []
                    for tag_name in tag_list:
                        tag = find_or_create_tag_by_name(tag_name)
                        post.tags.append(tag)
                    # remove tags that are now not used by any posts
                    for tag in tags_removed:
                        if len(tag.posts.all()) == 1:
                            db.session.delete(tag)

                db.session.commit()
                if post is None:
                    flash(u'Successfully posted: %s' % title, category='blog')
                else:
                    flash(u'Successfully edited: %s' % title, category='blog')
                return redirect('/blog')

            except ValidationError:
                pass
        else:
            pass

    flash(u'There were errors in your submission. Please check below.')
    return render_template('blog/write.html', form=form)

# Routes

@app.errorhandler(404)
def resource_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def about():
    if current_user.is_anonymous():
        email = None
    else:
        email = current_user.email
    return render_template('about.html', email=email)

@app.route('/blog/')
def blog():
    posts = Post.query.order_by(Post.created_at.desc(), Post.id.desc()).all()
    return render_template('blog/index.html', posts=posts)

@app.route('/blog/write')
@login_required
def blog_write():
    return render_template('blog/write.html', form=WriteForm())

@app.route('/blog/write', methods=["POST"])
@login_required
def blog_submit_new_post():
    return blog_submit_post()

@app.route('/blog/manage')
@login_required
def blog_manage():
    posts = Post.query.order_by(Post.created_at.desc(), Post.id.desc()) \
                      .all()
    return render_template('blog/manage.html', posts=posts)


# Post-specific routes

@app.route('/blog/posts/<post_slug>')
def blog_post(post_slug):
    post = Post.query.filter_by(slug=post_slug) \
                     .first()
    if post is None or not post.published:
        abort(404)
    return render_template('blog/post.html', post=post, preview=False)

@app.route('/blog/posts/<post_slug>/preview')
@login_required
def blog_post_preview(post_slug):
    post = Post.query.filter_by(slug=post_slug) \
                     .first()
    if post is None:
        abort(404)
    return render_template('blog/post.html', post=post, preview=True)

@app.route('/blog/posts/<post_slug>/edit')
@login_required
def blog_edit_post(post_slug):
    post = Post.query.filter_by(slug=post_slug) \
                     .first()
    if post is None:
        abort(404)
    form = WriteForm()
    form.title.data    = post.title
    form.slug.data     = post.slug
    form.tag_list.data = ', '.join(map(lambda x: x.name, post.tags))
    form.body.data     = post.body
    return render_template('blog/write.html', form=form,
                           post=post)

@app.route('/blog/posts/<post_slug>/edit', methods=["POST"])
@login_required
def blog_submit_edited_post(post_slug):
    post = Post.query.filter_by(slug=post_slug) \
                     .first()
    if post is None:
        abort(404)
    return blog_submit_post(post=post)

# make this more RESTful...

@app.route('/blog/posts/<post_slug>/delete')
@login_required
def blog_delete_post(post_slug):
    post = Post.query.filter_by(slug=post_slug) \
                     .first()
    if post is None:
        abort(404)
    # remove tags that are not used by any other posts
    for tag in post.tags:
        if len(tag.posts.all()) == 1:
            db.session.delete(tag)
            flash(u'Deleted emptied tag: %s' % tag.name)
    db.session.delete(post)
    db.session.commit()
    flash(u'Deleted post: %s' % post.title, category='blog')
    return redirect('/blog/manage')

@app.route('/blog/tags/<tag_slug>')
def blog_posts_by_tag(tag_slug):
    tag = Tag.query.filter_by(slug=tag_slug).first()
    if tag is None:
        abort(404)
    posts = Post.query.filter(Post.tags.any(Tag.id == tag.id)) \
                      .order_by(Post.created_at.desc(), Post.id.desc()) \
                      .all()
    return render_template('blog/index.html', 
                            posts=posts, 
                            tag_view=tag.name)

def make_external(url):
    return urljoin(request.url_root, url)

@app.route('/blog/feed.atom')
def recent_feed():
    feed = AtomFeed('andywrote - recent blog posts',
                    feed_url=request.url,
                    url=request.url_root)
    posts = Post.query.order_by(Post.created_at.desc(), Post.id.desc()) \
                      .limit(20) \
                      .all()
    for post in posts:
        feed.add(post.title, 
                 unicode(post.body),
                 content_type='html',
                 author=', '.join(map(lambda x: x.name, post.authors)),
                 url=make_external('/blog/posts/%s' % post.slug),
                 updated=post.updated_at)
    return feed.get_response()

if __name__ == '__main__':
    app.run()