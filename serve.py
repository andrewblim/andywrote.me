
# Much thanks to Sylvain Hellegouarch's sample Twiseless app, which was a great
# help: https://bitbucket.org/Lawouach/twiseless/

from app.andywrote import AndyWrote
import cherrypy
import os.path

if __name__ == '__main__':

    cherrypy.tree.mount(AndyWrote(), 
                        config='config/andywrote.conf')
    cherrypy.engine.start()
    cherrypy.engine.block()