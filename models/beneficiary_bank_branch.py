from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class BeneficiaryBankBranch(models.Model):
    _name = 'beneficiary_bank_branch.model'


    name = fields.Char(required=True, string='Beneficiary Bank Name',size=100)
    bank_branch = fields.Text('Beneficiary Bank Brunch')
    bank_address = fields.Text('Beneficiary Bank Address')
    swift_code = fields.Text('Swift Code')
    date = fields.Date('Created Dated', required=True, default=fields.Date.today())