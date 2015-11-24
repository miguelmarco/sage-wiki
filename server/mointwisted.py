import os, sys

from zope.interface import implements
 
from twisted.web import server, resource, wsgi, static
from twisted.internet import reactor, defer
from twisted.application import internet, service
from twisted.python import usage, threadpool

sys.path.insert(0, os.path.join(r'/home/timdumol/sage_wiki'))
from MoinMoin.web.serving import make_application
application = make_application(shared=True)

class MyOptions(usage.Options):
    optParameters = [
        ['port', 'p', 9000, 'Port to listen on'],
        ['address', 'a', '', 'Host address to listen on'],
        ]

class Root(resource.Resource):
    pass
    
class WikiRoot(resource.Resource):

    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource
        
    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource
 
pool = threadpool.ThreadPool()
reactor.callWhenRunning(pool.start)
reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
 

resource_root = WikiRoot(wsgi.WSGIResource(reactor, pool, application))

#resource_root.putChild("data", data_resource)
 
class ServiceMaker(object):
 
    implements(service.IServiceMaker, service.IPlugin)
    tapname = "moin"
    description = "Sage Moin Moin Wiki WSGI service"
    options = MyOptions
 
    def makeService(self, options):
        desktop_service = service.MultiService()
        
        web_resource_factory = server.Site(resource_root)
 
        tcp_server = internet.TCPServer(int(options['port']),
                                       web_resource_factory,
                                       interface='')
        
        tcp_server.setServiceParent(desktop_service)
 
        return desktop_service
 
serviceMaker = ServiceMaker()
