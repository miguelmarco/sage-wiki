# -*- coding: iso-8859-1 -*-
"""
    Theme preferences by user

    @copyright: 2001-2004 Juergen Hermann <jh@web.de>
                2003-2007 MoinMoin:ThomasWaldmann
                2010 Renato Silva

    @license: See the README file.
"""

from MoinMoin import util
from MoinMoin.widget import html
from MoinMoin.userprefs import UserPrefBase

from MoinMoin import log
logger = log.getLogger(__name__)

class Settings(UserPrefBase):

    def __init__(self, request):
        UserPrefBase.__init__(self, request)
        self.request = request
        self._ = request.getText
        self.cfg = request.cfg
        self.user = request.user
        self.theme = request.theme
        self.name = 'themeprefs'
        self.title = self._('Theme preferences')
        self.fields = self._seek_fields()

    def _seek_fields(self):
        fields = getattr(self.theme, 'userprefs_definition', [])
        try:
            for kind, name, description in fields:
                for field in (name, description):
                    if not isinstance(field, (str, unicode)):
                        return []
                if kind != bool:
                    logger.warning("Unsupported theme preference type: %s" % kind)
                    return []
        except Exception, e:
            logger.warning("Error while validating theme preference fields: %s" % e)
            return []
        return fields

    def _full_attr_name(self, attribute_name):
        return '%s_%s' % (self.theme.name, attribute_name)

    def _read(self, name, kind):
        full_name = self._full_attr_name(name)
        value = getattr(self.user, full_name, None)
        if kind == bool:
            if value in ('0', '1'):
                return value
            return '2'

    def _write(self, name, kind):
        full_name = self._full_attr_name(name)
        try:
            value = self.request.values.get(name) # Moin 1.9
        except AttributeError:
            value = self.request.form[name][0] # Moin 1.8
        if kind == bool:
            if value not in ('0', '1'):
                value = ''
            setattr(self.user, full_name, value)

    def _render_config(self, name, kind):
        if kind == bool:
            options = [
                ('1', self._('Activate')),
                ('0', self._('Deactivate')),
                ('2', '<%s>' % self._('Default'))]
            value = self._read(name, kind)
            return util.web.makeSelection(name, options, value)

    def allowed(self):
        return UserPrefBase.allowed(self) and self.fields != []

    def create_form(self):
        explanation = self._('User preferences for %s theme:') % self.theme.Name
        self._form = self.make_form(html.Text(explanation))

        for kind, name, description in self.fields:
            self.make_row(description, [self._render_config(name, kind)])

        self._form.append(html.INPUT(type='hidden', name='action', value='userprefs'))
        self._form.append(html.INPUT(type='hidden', name='handler', value=self.name))

        save_button = html.INPUT(type="submit", name='save', value=self._('Save'))
        cancel_button = html.INPUT(type="submit", name='cancel', value=self._('Cancel'))

        self.make_row('', [save_button, ' ', cancel_button])
        return unicode(self._form)

    def handle_form(self):
        form = self.request.form
        try:
            request_method = self.request.method # Moin 1.9
        except AttributeError:
            request_method = self.request.request_method # Moin 1.8

        if ('cancel' in form) or not ('save' in form and request_method == 'POST'):
            return

        for kind, name, description in self.fields:
            self._write(name, kind)

        self.user.save()
        return self._('Theme preferences saved!')
