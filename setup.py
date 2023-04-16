from setuptools import setup
from rdf2puml import __version__

setup(name='digitales_belegblatt',
      version=__version__,
      description='Implementation of Digitales Belegblatt.',
      url='git@gitlab.hpi.de:osm/flexidug/digitales-belegblatt.git',
      author='Dirk Friedenberger',
      author_email='projekte@frittenburger.de',
      license='GPLv3',
      packages=['digitales_belegblatt'],
      install_requires=[],
      zip_safe=False)
