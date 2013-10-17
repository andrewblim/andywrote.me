
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, validators

class WriteForm(Form):

    title = StringField(u'Title', \
        [validators.Length(
            min=1, max=300,
            message=u'Your title must contain at least 1 character and no more than 300 characters.')
        ])
    slug = StringField(u'Slug', \
        [validators.Length(
            max=80,
            message=u'Your slug must contain at most 80 characters'),
         validators.Regexp(
            regex=r'^[A-Za-z0-9\-]*$',
            message=u'Your slug may only contain letters, numbers, and hyphens')
        ])
    tag_list = StringField(u'Tags')
    body     = TextAreaField(u'Body')

    convert_breaks = BooleanField(u'Convert line breaks to &lt;p&gt;')
    use_smartypants = BooleanField(u'Use SmartyPants')