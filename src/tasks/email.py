""" Email tasks """

from flask import current_app
from flask.ext.mail import Mail, Message

from ..app import celery


@celery.task
def send_welcome_email(person):
    """ Send the welcome email on person signup """

    send_email.delay(person['email'], 'Hi ' + person['first_name'],
                     'WELCOME!!!')


@celery.task
def send_email(to, subject, body, sender=None):
    """ Send email email message """

    if not isinstance(to, list):
        to = [to]

    if sender is None:
        sender = current_app.config.get('MAIL_SENDER',
                                        'noreplay@ourfamilylegacy.org')

    msg = Message(subject, sender=sender, recipients=to)
    msg.body = body

    mail = Mail(current_app)
    mail.send(msg)
