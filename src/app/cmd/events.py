""" Commands to run legacy events """

import datetime

from flask import current_app
from flask.ext.script import Command

from sqlalchemy import or_
from sqlalchemy.orm import aliased

from src.app.models import Event, Legacy, Person


class EventsCommand(Command):
    """ Execute scheduled legacy events for today """

    command = 'runevents'

    def run(self):
        """ run command """

        today = datetime.datetime.now()

        owner = aliased(Person)

        event_list = Event.query.join(Legacy).join(owner, Legacy.owner).filter(
            Event.status == 'ENABLED',
            Event.month == today.month,
            Event.day == today.day,
            Legacy.status == 'LEGEND',
            owner.status == 'DECEASED',
            or_(
                Event.last_run == None,
                Event.last_run < datetime.date.today()
            ),
            Event.run_count < current_app.config.get('EVENT_RUN_COUNT')
        ).limit(5).all()

        [e.run() for e in event_list]
