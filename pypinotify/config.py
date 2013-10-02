# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import ConfigParser
import os
import socket

DB_PATH = 'sqlite:///%s' % os.path.expanduser('~/pypi-notify.db')
TEMPLATE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            '..', 'templates')


class Config(object):

    CONFIGS = {
        'main': {
            'url': {'default': 'https://pypi.python.org'},
            'sql': {'default': DB_PATH},
        },

        'templates': {
            'directory': {'default': TEMPLATE_DIR},
            'mail': {'default': 'mail.txt', 'section': 'template'},
        },

        'mail': {
            'from': {'default': 'pypi-notify@%s' % socket.gethostname()},
            'to': {'default': ''},
            'server': {'default': 'localhost'},
            'port': {'default': 25},
        },
    }

    def __init__(self):
        self.config = ConfigParser.ConfigParser()

    def readfp(self, fp):
        self.config.readfp(fp)

    def read(self, filenames):
        self.config.read(filenames)

    def __getattr__(self, name):
        section, n = name.split('_', 1)
        try:
            val = self.CONFIGS[section][n]
        except KeyError:
            raise AttributeError(name)
        else:
            try:
                return self.config.get(section, n)
            except ConfigParser.Error:
                return val.get('default')


_config = None


def get_config():
    return _config


def set_config(*args, **kwargs):
    global _config
    _config = Config(*args, **kwargs)
    return _config
