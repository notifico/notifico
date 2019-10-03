import os
import base64
import hashlib
import datetime

from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy

from notifico.db import db


user_roles = db.Table(
    'user_roles',
    db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.key'))
)


class Role(db.Model):
    __tablename__ = 'role'

    key = db.Column(db.Unicode(15), primary_key=True)

    def __init__(self, key: str):
        self.key = key

    @classmethod
    def get_or_create(cls, key: str):
        role = cls.query.filter_by(key=key).first()
        return role if role else Role(key)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    salt = db.Column(db.String(8), nullable=False)
    joined = db.Column(db.TIMESTAMP(), default=datetime.datetime.utcnow)

    company = db.Column(db.String(255))
    website = db.Column(db.String(255))
    location = db.Column(db.String(255))

    _roles = db.relationship(
        'Role',
        secondary=user_roles,
        backref='users',
        collection_class=set
    )

    roles = association_proxy(
        '_roles',
        'key',
        creator=Role.get_or_create
    )

    def get_id(self):
        return str(self.id)

    @classmethod
    def new(cls, username, email, password):
        u = cls()
        u.email = email.lower().strip()
        u.password = password
        u.username = username.strip()
        return u

    @staticmethod
    def _create_salt():
        """
        Returns a new base64 salt.
        """
        return base64.b64encode(os.urandom(8))[:8]

    @staticmethod
    def _hash_password(password, salt):
        """
        Returns a hashed password from `password` and `salt`.
        """
        return hashlib.sha256(
            salt.encode('utf-8') + password.strip().encode('utf-8')
        ).hexdigest()

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self.salt = self._create_salt()
        self._password = self._hash_password(plaintext, self.salt)

    @classmethod
    def by_email(cls, email):
        return cls.query.filter_by(email=email.lower().strip()).first()

    @classmethod
    def email_exists(cls, email):
        return cls.query.filter_by(email=email.lower().strip()).count() >= 1

    @classmethod
    def by_username(cls, username):
        return cls.query.filter(
            func.lower(cls.username) == func.lower(username)
        ).first()

    @classmethod
    def username_exists(cls, username):
        return cls.query.filter(
            func.lower(cls.username) == func.lower(username)
        ).count() >= 1

    @classmethod
    def login(cls, username, password):
        """
        Returns a `User` object for which `username` and `password` are
        correct, otherwise ``None``.
        """
        u = cls.by_username(username)
        if u and u.password == cls._hash_password(password, u.salt):
            return u
        return None

    @hybrid_property
    def username_i(self):
        return self.username.lower()

    def active_projects(self, limit=5):
        """
        Return this users most active projets (by descending message count).
        """
        q = self.projects.order_by(False).order_by('-message_count')
        q = q.limit(limit)
        return q

    def in_group(self, name):
        # FIXME: Deprecated
        return False

    def export(self):
        """
        Exports the user, his projects, and his hooks for use in a
        private-ly hosted Notifico instance.
        """
        j = {
            'user': {
                'username': self.username,
                'email': self.email,
                'joined': self.joined.isoformat(),
                'company': self.company,
                'website': self.website,
                'location': self.location
            },
            'projects': [{
                'name': p.name,
                'created': p.created.isoformat(),
                'public': p.public,
                'website': p.website,
                'message_count': p.message_count,
                'channels': [{
                    'created': c.created.isoformat(),
                    'channel': c.channel,
                    'host': c.host,
                    'port': c.port,
                    'ssl': c.ssl,
                    'public': c.public
                } for c in p.channels],
                'hooks': [{
                    'created': h.created.isoformat(),
                    'key': h.key,
                    'service_id': h.service_id,
                    'message_count': h.message_count,
                    'config': h.config
                } for h in p.hooks]
            } for p in self.projects]
        }

        return j
