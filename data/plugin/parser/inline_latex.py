#format python
"""
inline_latex is a parser that allows regular moin moin wiki syntax,
but also latex style inline formulas like $...$ and latex style
paragraph formulas like $$...$$. Note that in the latter case, you
are (unlike in latex) limited to a single line. If you absolutely
need multiple lines, use the parser directly.

Copyright 2005 Johannes Berg <johannes@sipsolutions.net>

Released under GPLv2.

"""

from MoinMoin.parser import wiki
from MoinMoin import wikiutil

class Parser(wiki.Parser):

    def __init__(self, raw, request, **kw):
	self.formatting_rules += r'|(?P<latex_formula>\$[^$].*?(?<!\\)\$)'
	self.formatting_rules += r'|(?P<latex_formula_para>\$\$.*?(?<!\\)\$\$)'
        wiki.Parser.__init__(self, raw, request, **kw)
    
    _latex_plugin = None
    def _aquire_latex_plugin(self):
        if self._latex_plugin is None:
            # get an exception? for moin before 1.3.2 use the following line instead:
            # self._latex_plugin = wikiutil.importPlugin('parser', 'latex', 'Parser', self.cfg.data_dir)
            self._latex_plugin = wikiutil.importPlugin(self.cfg, 'parser', 'latex', 'Parser')
	
    def _latex_formula_repl(self, text, **kw):
        self._aquire_latex_plugin()
        if self._latex_plugin is None:
            return self.formatter.text("<<please install the latex parser>>")
	return self._latex_plugin('', self.request).get(self.formatter, text, '')

    def _latex_formula_para_repl(self, text, **kw):
        self._aquire_latex_plugin()
        if self._latex_plugin is None:
            return self.formatter.text("<<please install the latex parser>>")
	return self.formatter.paragraph(1) + \
	       self._latex_plugin('', self.request).get(self.formatter, text, '') + \
	       self.formatter.paragraph(0)
