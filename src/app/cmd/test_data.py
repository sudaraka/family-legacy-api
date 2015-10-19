""" Commands to wipe the DB and create test records """

import datetime
import os
import random

from flask import current_app
from flask.ext.script import Command

from src.app import db
from src.app.models import Person, Legacy, Event


class TestDataCommand(Command):
    """ Wipe entire database and create test data """

    command = 'testdata'

    dataset = [
        {'status': 'ACTIVE', 'first_name': 'OFN {}', 'last_name': 'OLN {}',
         'email': '{}@owner', 'username': 'owner{}', 'password': '123'}
        for _ in range(10)
    ]

    today = datetime.datetime.now()

    events = [
        {'status': 'ENABLED', 'month': today.month - 1, 'day': today.day},
        {'status': 'ENABLED', 'month': today.month, 'day': today.day - 1},
        {'status': 'ENABLED', 'month': today.month, 'day': today.day},
        {'status': 'ENABLED', 'month': today.month, 'day': today.day + 1},
        {'status': 'ENABLED', 'month': today.month + 1, 'day': today.day},

        {'status': 'DISABLED', 'month': today.month - 1, 'day': today.day},
        {'status': 'DISABLED', 'month': today.month, 'day': today.day - 1},
        {'status': 'DISABLED', 'month': today.month, 'day': today.day},
        {'status': 'DISABLED', 'month': today.month, 'day': today.day + 1},
        {'status': 'DISABLED', 'month': today.month + 1, 'day': today.day},
    ]

    def run(self):
        """ run command """

        if 'dev' != os.environ.get('FLASK_CONFIG'):
            return  # Not running in development environment

        if not current_app.config.get('DEBUG'):
            return  # Not running in debug mode

        print('\nRemoving all records...')

        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
            print('  ✔ {}'.format(table.name))

        print('\nCreate members...')

        _member = {'status': 'ACTIVE', 'first_name': 'MFN {}',
                   'last_name': 'MLN {}', 'email': '{}@member',
                   'username': 'member{}', 'password': '123'}

        member_list = [
            Person(**{n: _member.get(n).format(idx + 1) for n in _member})
            for idx in range(50)]

        [p.save() for p in member_list]

        print('\nCreate owners...')

        event_index = 0

        for idx, _p in enumerate(self.dataset):
            p = Person(**{n: _p.get(n).format(idx + 1) for n in _p})
            l = Legacy(owner=p, members=random.sample(member_list, 5))

            for _, _e in enumerate(self.events):
                _e['legacy'] = l
                _e['name'] = 'Event {}-{}'.format(
                    chr(65 + int(event_index / 26)),
                    chr(65 + (event_index % 26))
                )

                Event(**_e)

                event_index += 1

            p.save()

            print('  ✔ {} {} ({})'.format(p.first_name, p.last_name,
                                            p.username))

        db.session.commit()
