#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_qunjielong
=================================================
"""

import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="py3-qunjielong",
    version="1.1.0",
    description="The Python3 Qunjielong Library Developed By Guolei",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guolei19850528/py3_qunjielong",
    author="guolei",
    author_email="174000902@qq.com",
    license="MIT",
    keywors=["qunjielong", "群接龙", "团购", "guolei", "郭磊"],
    packages=setuptools.find_packages('./'),
    install_requires=[
        "py3-requests",
        "diskcache",
        "redis",
        "addict",
        "retrying",
        "jsonschema",
    ],
    python_requires='>=3.0',
    zip_safe=False
)
