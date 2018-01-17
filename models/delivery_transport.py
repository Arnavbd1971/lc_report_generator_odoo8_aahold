from openerp import models, fields

class DeliveryTransport(models.Model):
    _name = 'delivery_transport.model'


    name = fields.Char(required=True, string='Transport name',size=64)
    date = fields.Date('Created date', required=True, default=fields.Date.today())
