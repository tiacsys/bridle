"""
Manifest Revisions Table
========================

This extension allows to render a table containing the revisions of the projects
present in a manifest file.

Usage
*****

This extension introduces a new directive: ``manifest-projects-table``. It can
be used in the code as::

    .. manifest-projects-table::
        :show-first: project1, project2
        :filter: active

where the ``:show-first:`` option can be used to specify which projects should
be shown first in the table and the ``:filter:`` option can have the following
values: ``active``, ``inactive``, or ``all``.

Options
*******

- ``manifest_projects_table_manifest``: Path to the manifest file.

Copyright (c) 2025 TiaC Systems
Copyright (c) 2023 Intel Corp
Copyright (c) 2022 Nordic Semiconductor ASA
SPDX-License-Identifier: Apache-2.0
"""

import re
from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.errors import ExtensionError
from sphinx.util.docutils import SphinxDirective
from west.manifest import Manifest

__version__ = "0.2.0"


class ManifestProjectsTable(SphinxDirective):
    """Manifest revisions table."""

    option_spec = {
        "filter": directives.unchanged,
        "show-first": directives.unchanged,
    }

    @staticmethod
    def rev_url(base_url: str, rev: str) -> str:
        """Return URL for a revision.

        Notes:
            Revision format is assumed to be a git hash or a tag. URL is
            formatted assuming a GitHub base URL.

        Args:
            base_url: Base URL of the repository.
            rev: Revision.

        Returns:
            URL for the revision.
        """

        if re.match(r"^[0-9a-f]{40}$", rev):
            return f"{base_url}/commit/{rev}"

        return f"{base_url}/releases/tag/{rev}"

    def run(self) -> list[nodes.Element]:
        # parse filter option
        active_filter = self.options.get("filter", None)

        # parse show-first option
        show_first_raw = self.options.get("show-first", None)
        show_first = (
            [entry.strip() for entry in show_first_raw.split(",")] if show_first_raw else []
        )

        if active_filter not in ["active", "inactive", "all"]:
            raise ExtensionError(f"Invalid filter option: {active_filter}")

        # sort manifest projects accounting for show-first
        manifest = Manifest.from_file(self.env.config.manifest_projects_table_manifest)
        projects = [None] * len(show_first)
        for project in manifest.projects:
            if project.name == "manifest":
                continue
            if (
                active_filter == "active"
                and manifest.is_active(project)
                or active_filter == "inactive"
                and not manifest.is_active(project)
                or active_filter == "all"
                or active_filter is None
            ):
                if project.name in show_first:
                    projects[show_first.index(project.name)] = project
                else:
                    projects.append(project)

        if not all(projects):
            raise ExtensionError(f"Invalid show-first option: {show_first_raw}")

        # build table
        table = nodes.table()

        tgroup = nodes.tgroup(cols=2)
        tgroup += nodes.colspec(colwidth=1)
        tgroup += nodes.colspec(colwidth=1)
        table += tgroup

        thead = nodes.thead()
        tgroup += thead

        row = nodes.row()
        thead.append(row)

        entry = nodes.entry()
        entry += nodes.paragraph(text="Project")
        row += entry
        entry = nodes.entry()
        entry += nodes.paragraph(text="Revision")
        row += entry

        rows = []
        for project in projects:
            row = nodes.row()
            rows.append(row)

            entry = nodes.entry()
            entry += nodes.paragraph(text=project.name)
            row += entry
            entry = nodes.entry()
            par = nodes.paragraph()
            par += nodes.reference(
                project.revision,
                project.revision,
                internal=False,
                refuri=ManifestProjectsTable.rev_url(project.url, project.revision),
            )
            entry += par
            row += entry

        tbody = nodes.tbody()
        tbody.extend(rows)
        tgroup += tbody

        return [table]


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value("manifest_projects_table_manifest", None, "env")

    directives.register_directive("manifest-projects-table", ManifestProjectsTable)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
