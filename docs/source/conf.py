import os
import sys
docs_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(docs_dir, '../../')
sys.path.insert(0, src_dir)

# -- Project information -----------------------------------------------------

project = 'EchoArtistry'
copyright = '2024, Jurik-001'
author = 'Jurik-001'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.autodoc',
        'sphinx_rtd_theme',
        'sphinx.ext.napoleon',
        'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []

napoleon_google_docstring = True
napoleon_include_special_with_doc = True

myst_heading_anchors: 2
myst_highlight_code_blocks: True

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']