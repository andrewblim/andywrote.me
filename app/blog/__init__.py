import cherrypy
import jinja2

# specify a base_dir...
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class Blog(object):

    @cherrypy.expose
    def index(self):
        return env.get_template('blog.jinja2').render()

    # temporary, obviously not going to write this for every post
    @cherrypy.expose
    def testpost(self):
        post = open('blog/content/test-post.html').read()
        return env.get_template('blogpost.jinja2').render(post=post)
