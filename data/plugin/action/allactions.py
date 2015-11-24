# -*- coding: iso-8859-1 -*-
"""
    All Actions action

    Lists the actions available for the current page.
    Based on Mandarin's PageAction.

    @copyright: Radomir Dopieralski, and possibly others
                2009, 2010 Renato Silva

    @license: See the README file.
"""

from MoinMoin import wikiutil
from MoinMoin.Page import Page

def execute(pagename, request):
    _ = request.getText
    from MoinMoin.formatter.text_html import Formatter
    fmt = request.formatter = Formatter(request)

    emit_http_headers = getattr(request, 'emit_http_headers', None) or getattr(request, 'http_headers', None)
    if emit_http_headers is not None:
        emit_http_headers()

    request.setContentLanguage(request.lang)
    request.theme.send_title(_('Actions for %s') % pagename, page_name=pagename)
    request.write(fmt.startContent("content")) # content div provides direction support
    request.write(availableactions(request))
    request.write(fmt.endContent())
    request.theme.send_footer(pagename)

def actionlink(request, action, title, comment=''):
    page = request.page
    params = '%s?action=%s' % (page.page_name, action)
    if action == 'RenamePage':
        params += '&subpages_checked=1'
    link = wikiutil.link_tag(request, params, title)
    return u''.join([u'<li>', link, comment, u'</li>'])


def availableactions(request):
    page = request.page
    _ = request.getText
    links = []
    try:
        available = request.getAvailableActions(page) # Moin 1.8
    except AttributeError:
        from MoinMoin.action import get_available_actions
        available = get_available_actions(request.cfg, page, request.user) # Moin 1.9

    def split_and_translate(title):
        title = Page(request, title).split_title(request)
        return _(title, formatted=False)

    available = [(split_and_translate(action), action) for action in available]

    if page.isWritable() and request.user.may.write(page.page_name):
        available.append((_('Edit Text'), 'edit'))

    if request.user.valid and request.user.email:
        subscribed = request.user.isSubscribedTo([page.page_name])
        title = (_('Subscribe'), _('Unsubscribe'))[subscribed]
        action = ('subscribe', 'unsubscribe')[subscribed]
        available.append((title, action))

    available.append((_('Print View'), 'print'))
    available.append((_('View Raw Text'), 'raw'))
    available.append((_('Delete Cache'), 'refresh'))

    available.sort()
    for title, action in available:
        links.append(actionlink(request, action, title))

    return u'<ul>%s</ul>' % u''.join(links)
