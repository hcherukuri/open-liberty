# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
import datetime
import os
import sys

sys.path.insert(0, os.path.abspath('../plugins/module_utils/'))

project = 'Open Liberty Ansible Collection'
copyright = '{y}, Red Hat, Inc.'.format(y=datetime.date.today().year)
author = 'Red Hat, Inc.'

version = ''
release = ''

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx_antsibull_ext',
    'ansible_basic_sphinx_ext',
]

templates_path = ['_templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.tmp']
pygments_style = 'ansible'
highlight_language = 'YAML+Jinja'

html_theme_path = ['_themes']
html_theme = 'sphinx_rtd_theme'
html_static_path = []
