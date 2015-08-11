""" Email template data model """

import os

from flask import current_app

from .. import db, app_dir


class EmailTemplate(db.Model):
    """ Email template data model declarations """

    __tablename__ = 'flapi_email_templates'

    id = db.Column(db.String(32), primary_key=True)
    content = db.Column(db.Text())

    @classmethod
    def get_content(cls, key):
        """
        Return the email content for the given key, either from database or from
        the template file.

        If key exists in the database:
            - Fetch content from database and return it

        If key does not exists in the database:
            - Load content from the template
            - Save content to the database
            - Return the content

        If content associated with the key in database is empty, treat it as non
        existing key.
        """

        email = cls().query.get(key)

        if email is not None and 1 < len(email.content):
            # Non-empty email content found in DB

            return email.content

        # Load email content from HTML template file via Flask
        template_file = os.path.join(app_dir, current_app.template_folder,
                                     'emails/{}.html'.format(key))
        content = ''

        try:
            with open(template_file) as tf:
                content = tf.read()

            if 1 < len(content):
                email = cls(id=key, content=content)
                db.session.add(email)
                db.session.commit()
        except FileNotFoundError:
            content = 'No content for email message "{}"'.format(key)

        return content
