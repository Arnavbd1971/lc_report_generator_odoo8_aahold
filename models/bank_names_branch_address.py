from openerp import models, fields, api

class bank_branch_address(models.Model):
    _name = 'bank_names_branch_address.model'


    name = fields.Char(compute='concatenate_custom_fields',store=True,string='Name')
    # bank_name = fields.Many2one('bank_names.model',required=True, string='Bank Name')
    bank_name = fields.Char(required=True, string='Bank Name')
    bank_branch = fields.Char(required=True, string='Bank Branch')
    bank_address = fields.Text(required=True, string='Bank Address')
    created_date = fields.Date('Created Dated', required=True, default=fields.Date.today())
    s_code = fields.Char(string='Swift Code')

    @api.depends('bank_name','bank_branch')
    def concatenate_custom_fields(self):
        self.name = str(self.bank_name) + ', ' + str(self.bank_branch) + ' '
    

