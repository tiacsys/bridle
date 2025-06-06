# Copyright (c) 2021-2022 TiaC Systems
# Copyright (c) 2021 Nordic Semiconductor ASA
# Copyright (c) 2021 Li-Pro.Net
# Copyright (c) 2019 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0

# based on http://protips.readthedocs.io/link-roles.html

import re
import subprocess

from docutils import nodes

try:
    import west.manifest

    try:
        west_manifest = west.manifest.Manifest.from_file()
    except west.util.WestNotFound:
        west_manifest = None
except ImportError:
    west_manifest = None


def get_github_rev():
    try:
        output = subprocess.check_output(
            'git describe --exact-match', shell=True, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return 'main'

    return output.strip().decode('utf-8')


def setup(app):
    rev = get_github_rev()

    # Try to get the Bridle repository's GitHub URL from the manifest.
    #
    # This allows building the docs in downstream Bridle-based
    # software with forks of the Bridle repository, and getting
    # :bridle_file: / :bridle_raw: output that links to the fork,
    # instead of mainline Bridle.
    baseurl = None
    if west_manifest is not None:
        try:
            # This search tries to look up a project named 'bridle'.
            # If Bridle is the manifest repository, this raises
            # ValueError, since there isn't any such project.
            baseurl = west_manifest.get_projects(['bridle'], allow_paths=False)[0].url
            # Spot check that we have a non-empty URL.
            assert baseurl
        except ValueError:
            pass

    # If the search failed, fall back on the mainline URL.
    if baseurl is None:
        baseurl = 'https://github.com/tiacsys/bridle'

    app.add_role('bridle_file', autolink(f'{baseurl}/blob/{rev}/%s'))
    app.add_role('bridle_raw', autolink(f'{baseurl}/raw/{rev}/%s'))

    # The role just creates new nodes based on information in the
    # arguments; its behavior doesn't depend on any other documents.
    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


def autolink(pattern):
    def role(name, rawtext, text, lineno, inliner, options=None, content=None):
        if options is None:
            options = {}
        if content is None:
            content = []
        m = re.search(r'(.*)\s*<(.*)>', text)
        if m:
            link_text = m.group(1)
            link = m.group(2)
        else:
            link_text = text
            link = text
        url = pattern % (link,)
        node = nodes.reference(rawtext, link_text, refuri=url, **options)
        return [node], []

    return role
