from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class LCinformations(models.Model):
    _name = 'bank_names_branch_address.model'


    name = fields.Many2one('bank_names.model',required=True, string='Bank Name')
    branch = fields.Many2one('bank_branch.model',required=True, string='Bank Branch')
    address = fields.Text(required=True, string='Bank Address')
    created_date = fields.Date('Created Dated', required=True, default=fields.Date.today())

