from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class BankBranch(models.Model):
    _name = 'bank_branch.model'


    name = fields.Char(required=True, string='Branch Name')
    created_date = fields.Date('Created Dated', required=True, default=fields.Date.today())

