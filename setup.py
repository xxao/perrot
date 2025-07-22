#  Created by Martin Strohalm

from setuptools import setup, find_packages

# get version
version = "0.24.0"

# get description
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

# include additional files
package_data = {}

# set classifiers
classifiers = [
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3 :: Only',
    'Operating System :: OS Independent',
    'Topic :: Multimedia :: Graphics :: Presentation',
    'Topic :: Scientific/Engineering',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research']

# main setup
setup(
    name = 'perrot',
    version = version,
    description = 'Draw simple plots using Pero drawing library',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/xxao/perrot',
    author = 'Martin Strohalm',
    author_email = '',
    license = 'MIT',
    packages = find_packages(),
    package_data = package_data,
    classifiers = classifiers,
    install_requires = ['numpy', 'pero'],
    zip_safe = False)
