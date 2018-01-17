from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class BeneficiaryFullName(models.Model):
    _name = 'beneficiary_full_name.model'


    name = fields.Char(required=True, string='Beneficiary Full Name')
    erc_no = fields.Char(string='ERC No')
    created_date = fields.Date('Created Dated', required=True, default=fields.Date.today())

