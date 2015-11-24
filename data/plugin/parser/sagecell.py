# -*- coding: iso-8859-1 -*-
"""
MoinMoin - Sage Cell Parser
@copyright: 2010 by Chris Martino <chris@console.org>, Jason Grout <jason-sage@creativetrax.com>
@license: GNU GPL.
"""
 
from MoinMoin.parser._ParserBase import ParserBase
from uuid import uuid4
 
Dependencies = ['user']

template=""" 
<div class="sage">
  <script type="text/x-sage">%(code)s</script>
</div>
"""

#template="""
#<div id="%(random)s"><script type="text/x-sage">%(code)s</script></div>
#<script type="text/javascript">
#$(function () {
#sagecell.makeSagecell({inputLocation: '#%(random)s',
#hide: ["computationID", "messages", "sessionTitle"],
#linked: true});
#});
#</script>
#"""
 
class Parser(ParserBase):
    parsername = "sagecell"
    Dependencies = []

    def __init__(self, code, request, **kw):
        self.code = self.sanitize(code)
        self.request = request
 
    def sanitize(self, code):
        # escape any instances of </script>
        sanitized=code.replace("</script>", "<\/script>")
        return sanitized
 
    def format(self, formatter):
        self.request.write(formatter.rawHTML(template%{'random': uuid4(), 'code': self.code})) 
