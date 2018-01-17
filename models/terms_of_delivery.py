from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class Product_Type(models.Model):
    _name = 'terms_of_delivery.model'


    name = fields.Text(required=True, string='Terms Of Delivery')
    created_date = fields.Date('Created Dated', required=True, default=fields.Date.today())

