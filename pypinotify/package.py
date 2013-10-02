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

import requests
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm

from pypinotify import config
from pypinotify import exceptions

Base = declarative_base()


def url_join(*bits):
    return "/".join([b.strip("/") for b in bits])


def package_url(package):
    return url_join(config.get_config().main_url, 'pypi', package, 'json')


class Package(Base):
    __tablename__ = 'packages'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    version = Column(String)

    def __init__(self, name, version=None):
        self.name = name
        self._data = None

        if not version:
            version = self.latest_version

        self.version = version

    @orm.reconstructor
    def init_on_load(self):
        self._data = None

    @property
    def data(self):
        if not self._data:
            url = package_url(self.name)
            req = requests.get(url)

            if not req.ok:
                raise exceptions.NotFound("Couldn't retrieve information")

            self._data = req.json()

        return self._data

    @property
    def info(self):
        return self.data['info']

    @property
    def urls(self):
        return self.data['urls']

    @property
    def latest_version(self):
        return self.info['version']

    def new_version_available(self):
        return self.latest_version != self.version

    def update_version(self, version=None):
        if not version:
            version = self.latest_version

        if self.version != version:
            self.version = version
            return True

        return False
