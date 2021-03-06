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

import setuptools


setuptools.setup(name='pypi-notify',
                 version='0.0.1',
                 author='Jamie Lennox',
                 author_email='jamielennox@redhat.com',
                 license='ASL 2.0',
                 install_requires=[
                     'Jinja2',
                     'requests',
                     'sqlalchemy',
                     'prettytable',
                 ],
                 packages=['pypinotify'],
                 package_data={
                     'pypinotify': ['etc/pypi-notify.conf',
                                    'templates/mail.txt'],
                 },
                 entry_points={'console_scripts': [
                     'pypi-notify = pypinotify.shell:main'
                 ]},
                 )
