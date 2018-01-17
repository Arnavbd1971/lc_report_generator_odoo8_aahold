from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class Commodity(models.Model):
    _name = 'commodity.model'


    name = fields.Text(required=True, string='Commodity')
    created_date = fields.Date('Created Dated', required=True, default=fields.Date.today())

