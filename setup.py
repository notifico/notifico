"""
Notifico is my personal open source MIT replacement to the
now-defunct http://cia.vc service with my own little spin on things.
"""
from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='Notifico',
        version='1.0.0',
        long_description=__doc__,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'flask',
            'Flask-WTF',
            'Flask-Gravatar',
            'Flask-SQLAlchemy',
            'flask-xml-rpc-re',
            'Flask-Mail',
            'Flask-Caching',
            'sqlalchemy',
            'oauth2',
            'redis',
            'gunicorn',
            'requests',
            'pygithub',
            'xmltodict',
            'unidecode',
            'raven',
            'docopt',
            'celery'
        ]
    )
