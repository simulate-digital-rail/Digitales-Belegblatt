from setuptools import setup
from digitales_belegblatt import __version__

setup(name='digitales-belegblatt',
      version=__version__,
      description='Implementation of Digitales Belegblatt.',
      long_description=open('README.md', encoding="UTF-8").read(),
      long_description_content_type='text/markdown',
      url='https://github.com/simulate-digital-rail/Digitales-Belegblatt.git',
      author='Dirk Friedenberger',
      author_email='projekte@frittenburger.de',
      license='GPLv3',
      packages=['digitales_belegblatt'],
      install_requires=["svgwrite"],
      zip_safe=False)
