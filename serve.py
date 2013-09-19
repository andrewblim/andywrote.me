
# Much thanks to Sylvain Hellegouarch's sample Twiseless app, which was a great
# help: https://bitbucket.org/Lawouach/twiseless/

from app import AndyWrote, Blog
import cherrypy
import os.path

if __name__ == '__main__':

    site = AndyWrote()
    site.blog = Blog()

    cherrypy.tree.mount(site, config='config/andywrote.conf')
    cherrypy.engine.start()
    cherrypy.engine.block()