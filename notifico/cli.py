import click
from flask.cli import FlaskGroup

from notifico.db import db
from notifico.app import create_app
from notifico.models import ALL_CORE_TABLES

BAD = click.style('✗', fg='red')
OK = click.style('✓', fg='green')


@click.group(cls=FlaskGroup, create_app=lambda info: create_app())
def cli():
    """Notifico management interface."""


@cli.group(name='db_core')
def db_group():
    """Database management."""


@db_group.command(name='init')
def db_init():
    for table in ALL_CORE_TABLES:
        click.echo(f'[{OK}] Verifying table {table.name}')
        table.create(db.engine, checkfirst=True)
