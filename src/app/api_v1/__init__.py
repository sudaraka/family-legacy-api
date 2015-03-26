""" API v1 Blueprint """

from flask import Blueprint


api = Blueprint('api', __name__)


from . import errors, persons
