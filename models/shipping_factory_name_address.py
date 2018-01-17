from openerp import models, fields

class ShippingFactoryNameAddress(models.Model):
    _name = 'shipping_factory_name_address.model' 


    name = fields.Char(required=True, string='Shipping Factory Name',size=250)
    address = fields.Text(required=True, string='Shipping Factory Address')
    date = fields.Date('Created date', required=True, default=fields.Date.today())
