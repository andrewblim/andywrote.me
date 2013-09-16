import cherrypy
import jinja2

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class AndyWrote(object):

    @cherrypy.expose
    def index(self):
        return env.get_template('index.jinja2') \
                  .render()

    @cherrypy.expose
    def about(self):
        return "ABOUTTTTT"
