"""Get app version and git changeset"""

import os
import subprocess

from django.utils.lru_cache import lru_cache


@lru_cache()
def get_version(version, path=None):
    """Return a PEP 440-compliant version number from VERSION and git."""
    version = get_complete_version(version)

    # Now build the two parts of the version number:
    # main = X.Y.Z
    # sub = +rev - for git revisions
    #     | {a|b|rc}N - for alpha, beta, and rc releases

    main = get_main_version(version)

    sub = ''
    if path:
        git_changeset = get_git_changeset(path)
        if git_changeset:
            sub = '+%s' % git_changeset

    elif version[3] != 'final' and version[4] != 0:
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'rc'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub


def get_main_version(version=None):
    """Return main version (X.Y.Z) from VERSION."""
    version = get_complete_version(version)
    return '.'.join(str(x) for x in version[:3])


def get_complete_version(version=None):
    """
    Return a tuple of the version. If version argument is non-empty,
    check for correctness of the tuple provided.
    """
    if version is None:
        from joda import VERSION as version
    else:
        assert len(version) == 5
        assert version[3] in ('alpha', 'beta', 'rc', 'final')

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
