from openerp import models, fields

class CustomerFactoryNameAddress(models.Model):
    _name = 'customer_factory_name_address.model' 


    name = fields.Char(required=True, string='Customer Factory Name',size=250)
    address = fields.Text(required=True, string='Customer Factory Address')
    date = fields.Date('Created date', required=True, default=fields.Date.today())
