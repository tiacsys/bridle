# Copyright (c) 2021 Nordic Semiconductor ASA

from os import PathLike
from pathlib import Path
from typing import Dict, Tuple, Optional

from sphinx.cmd.build import get_parser
from west.manifest import Manifest


_BRIDLE_BASE = Path(__file__).parents[2]
"""Bridle Repository root"""

_MANIFEST = Manifest.from_file(_BRIDLE_BASE / "west.yml")
"""Manifest instance"""

ALL_DOCSETS = {  # first entry is default docset
    "bridle": ("Bridle", "index", "manifest"),
    "zephyr": ("Zephyr Project", "index", "zephyr"),
    "kconfig": ("Kconfig Reference", "index", None),
    "devicetree": ("Devicetree Bindings", "index", None),
}
"""All supported docsets (name: title, home page, manifest project name)."""


def get_default_docset() -> str:
    """Optain default docset name.

    Args:

    Returns:
        String of docset name.
    """
    docsets = ALL_DOCSETS.copy()
    return list(docsets.keys())[0]

def get_docsets(docset: str) -> Dict[str, str]:
    """Obtain all docsets that should be displayed.

    Args:
        docset: Target docset.

    Returns:
        Dictionary of docsets.
    """
    docsets = ALL_DOCSETS.copy()
    del docsets[docset]
    return docsets


def get_projdir(docset: str) -> Path:
    """Obtain the project directory for the given docset.

    Args:
        docset: Target docset.

    Returns:
        Project path for the given docset.
    """

    name = ALL_DOCSETS[docset][2]
    if not name:
        raise ValueError("Given docset has no associated project")

    p = next((p for p in _MANIFEST.projects if p.name == name), None)
    assert p, f"Project {name} not in manifest"

    return Path(p.topdir) / Path(p.path)


def get_builddir() -> PathLike:
    """Obtain Sphinx base build directory for a given docset.

    Returns:
        Base build path.
    """
    parser = get_parser()
    args = parser.parse_args()
    return (Path(args.outputdir) / ".." / "..").resolve()


def get_outputdir(docset: str) -> PathLike:
    """Obtain Sphinx output directory for a given docset.

    Args:
        docset: Target docset.

    Returns:
        Build path of the given docset.
    """

    return get_builddir() / "html" / docset


def get_srcdir(docset: str) -> PathLike:
    """Obtain sources directory for a given docset.

    Args:
        docset: Target docset.

    Returns:
        Sources directory of the given docset.
    """

    return get_builddir() / docset / "src"


def get_intersphinx_mapping(docset: str) -> Optional[Tuple[str, str]]:
    """Obtain intersphinx configuration for a given docset.

    Args:
        docset: Target docset.

    Notes:
        Relative links are used for URL prefix.

    Returns:
        Intersphinx configuration if available.
    """

    outputdir = get_outputdir(docset)
    inventory = outputdir / "objects.inv"
    if not inventory.exists():
        return

    return (str(Path("..") / docset), str(inventory))
