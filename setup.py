#!/usr/bin/env python3
"""
Legacy setup.py for backward compatibility.

Modern installation should use pyproject.toml:
    pip install .
    pip install -e .  # for development
"""

from setuptools import setup

# All configuration is in pyproject.toml
# This file exists only for backward compatibility with older pip versions
setup()
