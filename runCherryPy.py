__author__ = 'amit'


from cherrypy import wsgiserver
from app import app
import cherrypy

PORT = 9000


def start():
    d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
    server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', PORT), d)

    try:
        print "starting cherryPy on port %d" % PORT
        server.start()
    except KeyboardInterrupt:
        print "stopping cherryPy"
        server.stop()

def start_engine():
	cherrypy.tree.graft(app, '/')
	cherrypy.tree.mount(None, '/static', {'/' : {
		'tools.staticdir.dir': app.static_folder,
		'tools.staticdir.on': True,
		}})
	cherrypy.config.update({
		'server.socket_port': PORT,
		'server.socket_host': '0.0.0.0',
		})
	cherrypy.engine.start()
	cherrypy.engine.block()

if __name__ == '__main__':
   start_engine()
