
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Music Reco',
    'author': 'Puneet Girdhar',
    'url': 'http://www.google.com',
    'download_url': 'http://www.google.com',
    'author_email': 'puneetgirdhar.in@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['MusicReco'],
    'scripts': [],
    'name': 'MusicReco'
}

setup(**config)
