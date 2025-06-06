#
# Zephyr documentation build configuration file.
#
# DERIVE and OVERRIDE AS NEEDED from:
# https://github.com/zephyrproject-rtos/zephyr/raw/zephyr-v2.6.0/doc/conf.py
#
# pylint: skip-file
#

import os
import re
import sys
from pathlib import Path

import sphinx
from sphinx.config import eval_config_file

# Paths ------------------------------------------------------------------------

BRIDLE_BASE = Path(__file__).absolute().parents[2]

# Add the '_extensions' directory to sys.path, to enable finding Bridle's
# utilities for Sphinx configuration within.
sys.path.insert(0, str(BRIDLE_BASE / 'doc' / '_utils'))
import utils  # noqa: E402

ZEPHYR_BASE = utils.get_projdir('zephyr')
ZEPHYR_WORKD = utils.get_builddir() / 'zephyr'

# Add the '_extensions' directory to sys.path, to enable finding Bridle's
# Sphinx extensions within.
sys.path.insert(0, str(BRIDLE_BASE / 'doc' / '_extensions'))

# Import all Zephyr configuration, override as needed later
conf = eval_config_file(str(ZEPHYR_BASE / 'doc' / 'conf.py'), tags)  # noqa: F821
locals().update(conf)

# Export ZEPHYR_BASE as environment variable to make autodoc for the
# pytest-twister-harness happy.
os.environ['ZEPHYR_BASE'] = str(ZEPHYR_BASE)

# pylint: disable=undefined-variable

# Project ----------------------------------------------------------------------

# General information about the project.
project = utils.get_projname('zephyr')

# parse Bridle version from 'VERSION' file
with open(BRIDLE_BASE / 'VERSION') as f:
    m = re.match(
        (
            r'^VERSION_MAJOR\s*=\s*(\d+)$\n'
            + r'^VERSION_MINOR\s*=\s*(\d+)$\n'
            + r'^PATCHLEVEL\s*=\s*(\d+)$\n'
            + r'^VERSION_TWEAK\s*=\s*(\d+)$\n'
            + r'^EXTRAVERSION\s*=\s*(.*)$'
        ),
        f.read(),
        re.MULTILINE,
    )

    if not m:
        sys.stderr.write('Warning: Could not extract Bridle version.\n')
        bridle_version = bridle_longversion = 'Unknown'
    else:
        major, minor, patch, tweak, extra = m.groups(1)
        bridle_release = bridle_version = bridle_longversion = ".".join((major, minor, patch))
        if tweak:
            bridle_longversion += "." + tweak
        if extra:
            bridle_release += "-" + extra

# Overview ---------------------------------------------------------------------

logcfg = sphinx.util.logging.getLogger(__name__)
logcfg.info(project + ' ' + release, color='yellow')  # noqa: F821
logcfg.info(f'From Bridle {bridle_release} ({bridle_longversion})', color='green')
logcfg.info('Build with tags: ' + ':'.join(map(str, tags)), color='red')  # noqa: F821
logcfg.info(f'BRIDLE_BASE is: "{BRIDLE_BASE}"', color='green')
logcfg.info(f'ZEPHYR_BASE is: "{ZEPHYR_BASE}"', color='green')
logcfg.info(f'ZEPHYR_WORKD is: "{ZEPHYR_WORKD}"', color='yellow')
logcfg.info(f'ZEPHYR_BUILD is: "{ZEPHYR_BUILD}"', color='yellow')  # noqa: F821

# General ----------------------------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '8.2'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones. Extensions that interfere should also removed here.
extensions.extend(  # noqa: F821
    [
        'sphinx.ext.intersphinx',
        'bridle.inventory_builder',
        'bridle.warnings_filter',
    ]
)

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If this is True, todo and todolist produce output, else they produce nothing.
# The default is False.
todo_include_todos = False

# Options for HTML output ------------------------------------------------------

# The theme that the HTML output should use.
html_theme = 'sphinx_tsn_theme'
html_theme_path = []

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [f'{BRIDLE_BASE}/doc/_static', f'{ZEPHYR_BASE}/doc/_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = True

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, license is shown in the HTML footer. Default is True.
html_show_license = True

# If given, this must be the name of an image file that is the logo of the
# docs, or URL that points an image file for the logo.
html_logo = None

html_theme_options = {
    'docsets': utils.get_docsets('zephyr'),
    'default_docset': utils.get_default_docset(),
}

# Disable Google search engine.
del html_context["google_searchengine_id"]  # noqa: F821
del html_additional_pages["gsearch"]  # noqa: F821

# Options for intersphinx ------------------------------------------------------

intersphinx_mapping = dict()

kconfig_mapping = utils.get_intersphinx_mapping('kconfig')
if kconfig_mapping:
    intersphinx_mapping['kconfig'] = kconfig_mapping

devicetree_mapping = utils.get_intersphinx_mapping('devicetree')
if devicetree_mapping:
    intersphinx_mapping['devicetree'] = devicetree_mapping

# Options for zephyr.doxyrunner plugin -----------------------------------------

doxyrunner_doxygen = os.environ.get('DOXYGEN_EXECUTABLE', 'doxygen')
doxyrunner_doxydir = os.environ.get('DOCSET_DOXY_PRJ', str(ZEPHYR_BASE / 'doc' / '_doxygen'))
doxyrunner_doxyfile = os.environ.get(
    'DOCSET_DOXY_IN', str(BRIDLE_BASE / 'doc' / '_doxygen' / 'doxyfile-zephyr.in')
)

doxyrunner_silent = True
doxyrunner_projects = {
    'zephyr': {
        'doxyfile': Path(doxyrunner_doxyfile).absolute(),
        'outdir': ZEPHYR_BUILD / 'doxygen',  # noqa: F821
        'outdir_var': 'DOXY_OUT',
        'fmt': True,
        'fmt_pattern': '@{}@',
        'fmt_vars': {
            'DOXY_SET': 'zephyr',
            'DOXY_IN': str(Path(doxyrunner_doxyfile).absolute().parent),
            'DOXY_LAYOUT': 'zephyr-doxyrunner',
            'DOXY_LOGOUT': str(Path(ZEPHYR_WORKD).absolute()),
            'DOXY_LOGWRN': 'doxygen-warnings.txt',
            'PROJECT_DOXY': str(Path(doxyrunner_doxydir).absolute()),
            'PROJECT_BASE': str(ZEPHYR_BASE),
            'PROJECT_NAME': project,
            'PROJECT_VERSION': version,  # noqa: F821
            'PROJECT_BRIEF': str(os.environ.get('DOCSET_BRIEF', 'Unknown project brief!')),
        },
    },
}

# -- Options for zephyr.kconfig ------------------------------------------------

# Disable Kconfig database generation, Bridle provides its own kconfig docset.
kconfig_generate_db = False
kconfig_ext_paths.clear()  # noqa: F821

# Options for zephyr.warnings_filter -------------------------------------------

warnings_filter_config = str(ZEPHYR_WORKD / 'known-warnings.txt')
warnings_filter_silent = True

# -- Options for notfound.extension --------------------------------------------

notfound_urls_prefix = '/doc/{}/zephyr/'.format(bridle_version if is_release else 'latest')  # noqa: F821

# Options for zephyr.external_content ------------------------------------------

# Copies additional required artifacts that Bridle wants to include as content.
external_content_contents.extend(  # noqa: F821
    [
        (ZEPHYR_BASE, "samples/**/*.html"),
        (ZEPHYR_BASE, "samples/**/*.html.bin"),
    ]
)

# Clear external content keeping, Bridle provides its own docsets for that.
external_content_keep.clear()  # noqa: F821

# Linkcheck options ------------------------------------------------------------

linkcheck_ignore = [
    # intersphinx links
    r'(\.\.(\\|/))+(bridle|kconfig|devicetree)',
    # redirecting and used in release notes
    'https://github.com/zephyrproject-rtos/zephyr',
    # link to access local documentation
    'http://localhost:4711/latest/index.html',
    'http://localhost:8000/latest/index.html',
    'http://localhost:8080/latest/index.html',
]

linkcheck_timeout = 30
linkcheck_workers = 10
linkcheck_anchors = True
linkcheck_anchors_ignore = [r'page=']

# pylint: enable=undefined-variable,used-before-assignment


# This function will update the zephyr.warnings_filter setup in case of
# the inventory builder to be more tolerant against missing references.
def update_inventory_warnings_filter_config(app):
    # Check if the value was provided by the original configuration.
    if "warnings_filter_config" in app.config:
        # Update the warnings_filter_config value.
        app.config.warnings_filter_config = str(ZEPHYR_WORKD / 'known-warnings-inventory.txt')


def update_config(app):
    # Check if a specific builder was initialized by the user.
    if app.builder.name == "inventory":
        update_inventory_warnings_filter_config(app)

    logcfg.info(f'Warnings filter from: "{app.config.warnings_filter_config}"', color='yellow')


def setup(app):
    app.connect("builder-inited", update_config, 0)
    app.add_css_file('css/common.css')
    app.add_css_file('css/zephyr.css')
