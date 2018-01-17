from openerp import models, fields

class SupplierFactoryNameAddress(models.Model):
    _name = 'supplier_factory_name_address.model' 


    name = fields.Char(required=True, string='Supplier Factory Name',size=250)
    address = fields.Text(required=True, string='Supplier Factory Address')
    date = fields.Date('Created date', required=True, default=fields.Date.today())
