#!/usr/bin/env python
"""
manage.py: run application related commands
"""

import inspect
import os
import sys

sys.path.append(os.path.dirname('..'))

if os.path.exists('.env'):
    print('Importing environment from .env')  # pylint: disable=I0011,C0325

    for line in open('.env'):
        var = line.strip().split('=')
        if 2 == len(var):
            os.environ[var[0]] = var[1]

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from src.app import create_app, db, models, cmd


app = create_app(os.environ.get('FLASK_CONFIG', 'prod'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


for c in [c for (_, c) in inspect.getmembers(cmd) if inspect.isclass(c)]:
    manager.add_command(c.command, c)


@manager.shell
def shell_context():
    """
    Return a cusom context for shell with application object, database and
    models
    """

    return dict(app=app, db=db, models=models)


@manager.command
def person(username=None):
    """ Create new or update existing person """

    def get_value(prompt, default):
        """ Prompt for user for input """

        new_value = input('{0} [{1}]: '.format(prompt, default))

        if new_value is None or 1 > len(new_value):
            return default

        return new_value

    p = models.Person.query.filter_by(username=username).first()

    if p is None:
        p = models.Person()
        p.username = username

        # pylint: disable=I0011,C0325
        print('Creating new person record.\n')
    else:
        # pylint: disable=I0011,C0325
        print('Updating person record (id: {0}).\n'.format(p.id))

    from getpass import getpass

    p.username = get_value('Username', p.username)

    new_pw = getpass()
    if 0 < len(new_pw):
        p.password = new_pw

    p.first_name = get_value('First name', p.first_name)
    p.last_name = get_value('Last name', p.last_name)
    p.email = get_value('Email address', p.email)

    try:
        p.save()
    except:  # pylint: disable=I0011,W0702,C0325
        print('\nFailed to update person record')

        return

    # pylint: disable=I0011,C0325
    print('\nPerson (id: {0}) updated.'.format(p.id))


if '__main__' == __name__:
    manager.run()
