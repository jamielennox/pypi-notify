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

import argparse
import logging
import sys

import prettytable
import sqlalchemy

from pypinotify import config
from pypinotify import exceptions
from pypinotify import mailer
from pypinotify import package

logging.basicConfig()

logger = logging.getLogger(__name__)


class Shell(object):

    def __init__(self):
        self._template = None

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-d', '--debug', action='store_true')
        self.parser.add_argument('-c', '--config', action='append',
                                 type=argparse.FileType('r'),
                                 default=[], help='Config file to read')
        self.parser.add_argument('-n', '--dry-run', action='store_true',
                                 help="Run commands and print output but "
                                      "don't persist any results")

        subparsers = self.parser.add_subparsers(help='sub-command help',
                                                dest='command')

        package_add = subparsers.add_parser('package-add',
                                            help='Add a package to the list')
        package_add.add_argument('packages', nargs='+')

        subparsers.add_parser('package-list', help='List all checked packages')

        package_add = subparsers.add_parser('package-delete',
                                            help='Remove packages from list')
        package_add.add_argument('packages', nargs='+')

        subparsers.add_parser('execute',
                              help='Check and notify package changes')

        notify_test = subparsers.add_parser('notify-test',
                                            help='Test run a notification')
        notify_test.add_argument('packages', nargs='*', default=['requests'])

    def run(self, args=None):
        if not args:
            args = sys.argv[1:]

        self.args = self.parser.parse_args(args)
        self.config = config.set_config()

        for config_fp in self.args.config:
            self.config.readfp(config_fp)

        if self.args.debug:
            logging.getRootLogger().setLevel(logging.DEBUG)

        engine = sqlalchemy.create_engine(config.get_config().main_sql,
                                          echo=True)
        self.session = sqlalchemy.orm.sessionmaker(bind=engine)()
        package.Base.metadata.create_all(engine)

        command = self.args.command.replace("-", "_")

        try:
            func = getattr(self, command)
        except AttributeError:
            logging.error("Couldn't find function to use: %s", command)
        else:
            func()

    def package_add(self):
        packages = []

        for name in self.args.packages:
            try:
                pkg = package.Package(name)
            except exceptions.NotFound:
                logger.warn("Couldn't find package: %s", name)
            else:
                logger.debug("Package found and added: %s - %s",
                             name, pkg.version)
                packages.append(pkg)

        if packages:
            self.session.add_all(packages)
            self.session.commit()

    def package_list(self):
        table = prettytable.PrettyTable(['Name', 'Version'])

        for pkg in self.session.query(package.Package) \
                               .order_by(package.Package.name):
            table.add_row([pkg.name, pkg.version])

        print table

    def package_delete(self):
        for name in self.args.packages:
            self.session.query(package.Package).filter_by(name=name).delete()
        self.session.commit()

    def execute(self):
        for pkg in self.session.query(package.Package):
            if pkg.update_version():
                self.do_notify(pkg)
                self.session.add(pkg)

    def notify_test(self):
        with mailer.Mailer() as mail:
            for name in self.args.packages:
                try:
                    pkg = package.Package(name)
                except exceptions.NotFound:
                    logger.warn("Couldn't find package: %s", name)
                else:
                    logger.info("Sending notification: %s", name)
                    mail.mail(pkg)


def main():
    shell = Shell()
    shell.run()


if __name__ == '__main__':
    main()
