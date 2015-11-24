#FORMAT python
#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""
A jsMath formatter

Author: Thomas Themel <themel0r@wannabehacker.com>

r20080615

"""

Dependencies = []

jsmathinclude = '''
    <script src="/moin_static191/jsMath/jsMath.js"></script>
    <script>
      addLoadEvent (function () {
        jsMath.Process();
      });
    </script>
    '''

import sha, os, tempfile, shutil, re
from MoinMoin.Page import Page
from MoinMoin.parser import text_moin_wiki

class Parser(text_moin_wiki.Parser):
    extensions = ['*']

    scripts_loaded = None

    def __init__(self, raw, request, **kw):
        self.scan_rules += r'|(?P<jsmath_formula>\$[^$].*?(?<!\\)\$)'
        self.scan_rules += r'|(?P<jsmath_formula_para>\$\$.*?(?<!\\)\$\$)'
        self.scan_re = re.compile(self.scan_rules, re.UNICODE|re.VERBOSE)
        text_moin_wiki.Parser.__init__(self, raw, request, **kw)
        self.raw = raw
        self.request = request
        self.exclude = []

    def script_header(self):
        if self.scripts_loaded is None:
            return jsmathinclude
            self.scripts_loaded = 1 
        else:
            return ''

#    def format(self, formatter):
#    	self.request.write(self.script_header())
#    	text_moin_wiki.Parser.format(self, formatter)
            
    def _jsmath_formula_repl(self, text, groups):
        return '<span class="math">'  + text[1:-1] .replace('>','&gt;').replace('<','&lt;')+ '</span>'

    def _jsmath_formula_para_repl(self, text, groups):
        return '<div class="math">'  + text[2:-2].replace('>','&gt;').replace('<','&lt;') + '</div>'

