"""In-tree PEP 517 build backend for PeachPy.

The x86-64 instruction modules (peachpy/x86_64/{generic,mmxsse,avx,fma,crypto,
mask,amd}.py) are generated at build time from the Opcodes package by
codegen/x86_64.py. This backend wraps setuptools.build_meta and runs that code
generation before building a wheel or an editable install, so the generated
modules are present both in the built wheel and in an editable source tree.

Opcodes and setuptools are provided by [build-system].requires in pyproject.toml.
setuptools is pinned <81 there because Opcodes still imports pkg_resources.
"""

import os

from setuptools import build_meta as _bm
# Re-export the hooks we do not override (get_requires_for_*,
# prepare_metadata_for_*) so this module is a complete PEP 517 backend.
from setuptools.build_meta import *  # noqa: F401,F403


def _run_codegen():
    import codegen.x86_64
    codegen.x86_64.main(os.path.dirname(os.path.abspath(__file__)))


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    _run_codegen()
    return _bm.build_wheel(wheel_directory, config_settings, metadata_directory)


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    _run_codegen()
    return _bm.build_editable(wheel_directory, config_settings, metadata_directory)


def build_sdist(sdist_directory, config_settings=None):
    # The sdist ships the codegen inputs (codegen/*.py, codegen/x86_64.json); the
    # downstream wheel build regenerates. No need to generate into the sdist.
    return _bm.build_sdist(sdist_directory, config_settings)
