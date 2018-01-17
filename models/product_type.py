from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class Product_Type(models.Model):
    _name = 'product_type.model'


    name = fields.Text(required=True, string='Product Type')
    created_date = fields.Date('Created Dated', required=True, default=fields.Date.today())

