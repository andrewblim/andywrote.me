import cherrypy
import jinja2

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class Blog(object):

    @cherrypy.expose
    def index(self):
        return "Blog"

class HelloWorld(object):

    blog = Blog()

    @cherrypy.expose
    def index(self):
        return env.get_template('helloworld.jinja2') \
                  .render(salutation='hello', target='world')

    @cherrypy.expose
    def about(self):
        return "ABOUTTTTT"

cherrypy.quickstart(HelloWorld())