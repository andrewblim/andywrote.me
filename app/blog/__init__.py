import cherrypy
import jinja2

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class Blog(object):

    @cherrypy.expose
    def index(self):
        return env.get_template('blog.jinja2').render()
