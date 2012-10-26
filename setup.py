
import os
import sys

from setuptools import setup, find_packages

version = '0.1'

here = os.path.abspath(os.path.dirname(__file__))
tests_dir = os.path.join(here, 'src/paulla/checkplanetdiff/tests/')
try:
    README = open(os.path.join(here, 'README.rst')).read()
    TESTS = open(os.path.join(tests_dir, 'test_checkplanetdiff.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
    CONTRIBUTORS = open(os.path.join(here, 'CONTRIBUTORS.txt')).read()
except IOError:
    README = CHANGES = CONTRIBUTORS = ''

long_description = README + '\n\n' + TESTS + '\n\n' + CHANGES \
                   + '\n\n'+ CONTRIBUTORS

install_requires=['setuptools', 'pynagios >= 0.1.1']

if sys.version_info[:2] < (2, 7):
    raise RuntimeError('Requires Python 2.7')

setup(name='paulla.checkplanetdiff',
      version=version,
      description=('A nagios|icinga plugin to check diff delay '
                   'with the official OpenStreetMap Planet.'
                   ),
      long_description=long_description,
      platforms = ["any"],
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        ],
      keywords='Nagios Icinga OSM',
      author='Jean-Philippe Camguilhem',
      author_email='jp.camguilhem+eggs@gmail.com',
      url='http://www.paulla.asso.fr',
      license='bsd',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['paulla'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      test_suite="paulla.checkplanetdiff.tests",
      entry_points="""
      [console_scripts]
      check_planetdiff = paulla.checkplanetdiff.check:run
      test_check_planetdiff = paulla.checkplanetdiff.check:test
      """,
      )
