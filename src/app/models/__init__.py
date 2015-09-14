""" Data Models """

from importlib import import_module
from flask import current_app
from sqlalchemy.exc import IntegrityError
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .. import db
from ..exceptions import NoData, IncompleteData


class APIModel(object):
    """
    Shared methods for API models that can convert them-self from/to Python
    dictionary
    """

    def from_dict(self, data):
        """
        Initialize object instance with data in the given dictionary
        """

        try:
            for field, value in data.items():
                if 'id' == field:  # Ignore id fields (primary key)
                    continue

                setattr(self, field, value)
        except AttributeError:
            raise NoData('No data given to create ' + self.__class__.__name__)

    def to_dict(self):
        """ Return current instance converted to Python a dictionary """

        def url_or(obj):
            """ Return result of obj.url() or the given attribute """

            if hasattr(obj, 'url') and callable(getattr(obj, 'url')):
                return obj.url()

            return None  # pragma: no cover

        def serialize_value(value):
            """
            Convert given value into representable format in the reseting
            dictionary
            """

            if isinstance(value, APIModel):
                return url_or(value)

            if isinstance(value, list):
                return [serialize_value(v) for v in value]

            return value

        result = {
            k: serialize_value(v)
            for k, v in self.__dict__.items()
            if k[0] != '_' and 'id' != k}

        self_url = url_or(self)
        if self_url:
            result['_links'] = {
                'self': self_url
            }

        return result

    def save(self):
        """ Save/commit changed of current instance to DB """

        try:
            db.session.add(self)
            db.session.commit()

            if current_app.config['TESTING']:
                # Refresh saved modal when in testing mode

                db.session.refresh(self)

        except IntegrityError as e:
            raise IncompleteData('Unable to save ' + self.__class__.__name__ +
                                 ': ' + e.args[0])


class APITokenModel(APIModel):
    """ Shared methods for API models that can generate access tokens """

    def get_token(self, ttl=3600):
        """ Create token based on the current instance """

        s = Serializer(current_app.config['SECRET_KEY'], expires_in=ttl)

        return s.dumps({
            'id': self.id,
            'uri': self.__class__.__module__ + '.' + self.__class__.__name__
        }).decode('utf-8')

    @staticmethod
    def verify_token(token):  # pragma: no cover
        """
        Verify given token and return a new instance of the modal if valid
        """

        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            token_data = s.loads(token)

            _module = token_data['uri'].split('.')
            _class = _module.pop()
            _module = import_module('.'.join(_module))

            return getattr(_module, _class).query.get(token_data['id'])
        except:  # pylint: disable=I0011,W0702
            return None


from .person import Person
from .legacy import Legacy
from .event import Event
from .attachment import Attachment
from .email import EmailTemplate
from .paypal_log import PayPalLog
