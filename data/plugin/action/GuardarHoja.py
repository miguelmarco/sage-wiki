import os
from MoinMoin.Page import Page
from MoinMoin import config

 
def parseline(line):
    l1 = line.replace(u"'''", u'**')
    l2 = l1.replace(u"''", u'*')
    l3 = l2.replace(u'<<BR>>', u'\n')
    l4 = l3.replace(u'`', u'``')
    l4 = l4.replace(u'{{{', u'{ { {')
    l4 = l4.replace(u'}}}', u'} } }')
    if l4[:3] == u' * ':
        l4 = l4[1:]
    troz = l4.split(u'$')
    if len(troz) %2 ==1:
        l4 = u''
        for i in range(len(troz)):
            if i%2 == 1:
                l4  += troz[i].replace(u'\\', u'\\\\')
            else:
                l4 += troz[i]
            if i < len(troz)-1:
                l4 += u'$'
    troz = l4.split(u'$$')
    if len(troz) %2 ==1:
        l4 = u''
        for i in range(len(troz)):
            if i%2 == 1:
                l4  += troz[i].replace(u'\\', u'\\\\')
            else:
                l4 += troz[i]
            if i < len(troz)-1:
                l4 += u'$$'
    return l4



def moin2rst(string):
    lines = string.split('\n')
    resul = u''
    while lines:
        l = lines.pop(0)
        while len(l)>0 and l[-1] == u' ':
            l = l[:-1]
        if l == u'{{{#!sagecell':
            l = lines.pop(0)
            resul += u'\n::\n\n'
            while l != u'}}}':
                resul += u'    sage: ' + l + u'\n'
                l = lines.pop(0)
            resul += u'\n'
        elif l[:3] == u'{{{':
            resul +=u'\n::\n'
            l = lines.pop(0)
            while l != u'}}}':
                resul += '    ' + l + u'\n'
                l = lines.pop(0)
            resul += u'\n'
        elif l[:2] == '==' and l[-2:] == '==':
            resul += u'\n' +(len(l) - 4) * u'-' + u'\n'
            resul += l[2:-2] + u'\n'
            resul += (len(l) - 4) * u'-' + u'\n\n'
        elif l[:1] == '=' and l[-1:] == '=':
            resul += u'\n' + (len(l) - 2) * u'=' + u'\n'
            resul += l[1:-1] + u'\n'
            resul += (len(l) - 2) * u'=' + u'\n\n'
        elif l == u'<<TableOfContents()>>':
            resul += u'.. contents:: Tabla de Contenidos\n'
        elif l[:18] == u'<<TableOfContents(' and l[-3:] == u')>>':
            resul += u'.. contents:: Tabla de Contenidos\n'
            resul += u'   :depth: ' +  l[18:-3] + u'\n'
        elif l[:2] == u'||' and l[-2:] == '||':
            tabla = [map(parseline,l.split(u'||')[1:-1])]
            while lines and lines[0][:2] == u'||' and lines[0][-2:] == '||':
                l = lines.pop(0)
                tabla.append(map(parseline,l.split(u'||')[1:-1]))
            if len(set(map(len, tabla))) == 1:
                lengths = [max([len(i[j]) for i in tabla]) for j in range(len(tabla[0]))]
                for i in lengths:
                    resul += i * u'=' + u'  '
                resul += u'\n'
                for f in tabla:
                    for i in range(len(lengths)):
                        c = f[i]
                        resul += c + (lengths[i] - len(c) + 2) * u' '
                    resul += u'\n'
                for i in lengths:
                    resul += i * u'=' + u'  '
                resul += u'\n\n'
        else:
            resul += parseline(l) + u'\n'
    return resul

def execute(pagename, request):
    rev = request.rev or 0
    page = Page(request, pagename, rev=rev)
    request.mimetype = 'text/plain'
    content_disposition='attachment'
    if page.exists():
        request.status_code = 200
        request.last_modified = os.path.getmtime(page._text_filename())
        text = page.encodeTextMimeType(moin2rst(page.body))
        filename_enc = "%s.rst" % page.page_name.encode(config.charset)
        dispo_string = '%s; filename="%s"' % (content_disposition, filename_enc)
        request.headers['Content-Disposition'] = dispo_string
    else:
        request.status_code = 404
        text = u"Page %s not found." % self.page_name
    request.write(text)

