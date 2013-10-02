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

import email
import time

import jinja2
import smtplib

from pypinotify import config
from pypinotify import exceptions


class Mailer(object):

    def __init__(self):
        self.config = config.get_config()

        loader = jinja2.FileSystemLoader(self.config.templates_directory)
        template_env = jinja2.Environment(loader=loader)
        self.template = template_env.get_template(self.config.templates_mail)

        self.smtp = smtplib.SMTP(self.config.mail_server,
                                 self.config.mail_port)

    def mail(self, pkg):
        mail_from = self.config.mail_from
        mail_to = self.config.mail_to
        date = email.utils.formatdate(time.time())

        message = self.template.render(info=pkg.info,
                                       urls=pkg.urls,
                                       mail={'from': mail_from,
                                             'to': mail_to},
                                       date=date)
        print "Sending message", message

        mail_to = mail_to.split(',')
        print mail_to
        self.smtp.sendmail(mail_from, mail_to, message)

    def quit(self):
        self.smtp.quit()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.quit()
