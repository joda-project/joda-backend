import os

from joda.version import get_version


VERSION = (0, 1, 0, 'alpha', 0)
version_string = get_version(VERSION,
                             os.path.dirname(os.path.abspath(__file__)))
