"""Get app version and git changeset"""

import os
import subprocess

from django.utils.lru_cache import lru_cache


@lru_cache()
def get_version(path=None, no_revision=False):
    """Returns a version string from VERSION and git."""
    base_dir = path if path else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(base_dir, 'VERSION')) as version_file:
        version = version_file.read().strip()

    if no_revision:
        return version

    revision = get_git_changeset(path)

    if revision:
        version += '+' + revision

    return version


@lru_cache()
def get_git_changeset(path=None):
    """Returns a hash of the latest git changeset."""
    base_dir = path if path else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_tag = subprocess.Popen(
        'git describe --exact-match HEAD',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, cwd=base_dir, universal_newlines=True,
    )
    tag_info = git_tag.communicate()

    if 'not found' in tag_info[1]:
        return ''

    if 'fatal' not in tag_info[1]:
        return ''

    git_revision = subprocess.Popen(
        'git rev-parse HEAD',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, cwd=base_dir, universal_newlines=True,
    )
    revision_info = git_revision.communicate()

    if revision_info[1]:
        return ''

    return revision_info[0].strip()[:8]
