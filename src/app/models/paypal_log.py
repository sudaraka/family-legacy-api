""" PayPal log data model """

from .. import db


class PayPalLog(db.Model):
    """
    PayPal log

    Successful transaction records
    """

    __tablename__ = 'flapi_paypalsuccess'

    id = db.Column(db.Integer, primary_key=True)
    payment_datetime = db.Column(db.DateTime, name='servertime')
    amt = db.Column(db.Numeric)

    flapi_id = db.Column(db.Integer, db.ForeignKey('flapi_persons.id'),
                         index=True)
    person = db.relationship('Person', foreign_keys=[flapi_id])
