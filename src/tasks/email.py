""" Email tasks """

from flask import current_app, render_template_string
from flask.ext.mail import Mail, Message

from ..app import celery
from ..app.models.email import EmailTemplate


@celery.task
def send_event_run_email(event, owner, member):
    """ Send the email to members of a legacy on the day of email """

    content = render_template_string(
        EmailTemplate.get_content('event'),
        event=event,
        owner=owner,
        member=member,
        event_url='#'
    )

    send_email.delay(member['email'], 'Legacy of {} {}'.format(
        owner['first_name'],
        owner['last_name']
    ), content)


@celery.task
def send_welcome_email(person, **kwargs):
    """ Send the welcome email on person signup """

    content = render_template_string(
        EmailTemplate.get_content('welcome'),
        person=person,
        username=kwargs.get('username', '')
    )

    send_email.delay(person['email'], 'Welcome to Family Legacy', content)


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
    msg.html = body

    mail = Mail(current_app)
    mail.send(msg)
