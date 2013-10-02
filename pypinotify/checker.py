

import jinja2
import logging
import sqlalchemy

from pypinotify import config
from pypinotify import package


logging.basicConfig()

logger = logging.getLogger(__name__)

PACKAGE = 'httpretty'

TEMPLATE = """
A new version of package {{info.name}} has been detected: {{info.version}}

Links:
{% for url in urls -%}
* {{url.packagetype}}:
  url: {{url.url}}
  size: {{url.size}}
  md5: {{url.md5_digest}}
  upload time: {{url.upload_time}}

{%- endfor %}

Good luck!
"""

config.set_config()

engine = sqlalchemy.create_engine(config.get_config().sql, echo=True)
Session = sqlalchemy.orm.sessionmaker(bind=engine)


session = Session()

p = package.Package('httpretty', '0.6.2')
session.add(p)


if p.new_version_available():
    template = jinja2.Template(TEMPLATE)
    print template.render(info=p.info, urls=p.urls)
    p.version = p.latest_version
    session.add(p)
