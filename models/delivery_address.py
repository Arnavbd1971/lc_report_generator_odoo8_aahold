from openerp import models, fields

class DeliveryAddress(models.Model):
    _name = 'delivery_address.model'


    name = fields.Text(required=True, string='Delivery From Address')
    date = fields.Date('Created date', required=True, default=fields.Date.today())
