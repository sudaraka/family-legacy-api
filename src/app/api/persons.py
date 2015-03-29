""" persons API resource """

from . import api
from ..models import Person
from ..decorators import json


@api.route('/persons/<int:id>', methods=['GET'])
@json
def get_person(id):  # pylint: disable=I0011,W0622
    """ Return single person record """

    return Person.query.get_or_404(id)
