from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class LCinformations(models.Model):
    _name = 'bank_names.model'


    name = fields.Char(required=True, string='Bank Name')
    created_date = fields.Date('Created Dated', required=True, default=fields.Date.today())

