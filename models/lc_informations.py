from openerp import models, fields, api, _
# from openerp.exceptions import ValidationError

class LCinformations(models.Model):
    _name = 'lc_informations.model'


    name = fields.Char(required=True, string='L/C No.',size=100)
    created_date = fields.Date('L/C Created Dated', required=True, default=fields.Date.today())
    bank_name = fields.Many2one('bank_names.model',required=True, string='LC Bank Name')
    bank_branch = fields.Many2one('bank_branch.model',required=True, string='LC Bank Branch')
    bank_address = fields.Text('Bank Address',required=True,)
    vat_no = fields.Char('VAT No.')
    irc_no = fields.Char('IRC No.')
    bin_no = fields.Char('BIN No.')
    tin_no = fields.Char('TIN No.')
    shipment_last_date = fields.Date('Last Date Of Shipment')
    amend_no = fields.Char('Amend No.')
    amend_date = fields.Date('Amend Date')
    



    # @api.one 
    # @api.constrains('created_date')
    # def _check_lc_date(self):
    #     if self.created_date > fields.Date.today():
    #         raise ValidationError(_("L/C Date can't be greater than current date!"))



    # @api.onchange('bank_name','bank_branch')        
    def onchange_bank_name_branch(self, cr, uid, ids, bank_name,bank_branch, context=None):
        bank_name_id = bank_name
        bank_branch_id = bank_branch
        if bank_name_id and bank_branch_id :
            service_obj= self.pool.get('bank_names_branch_address.model').search(cr, uid,[('name','=',bank_name_id),('branch','=',bank_branch_id),],context=context)
            bank_address_in_list = self.pool.get('bank_names_branch_address.model').read(cr, uid,service_obj,['address'], context=context)
            if len(bank_address_in_list) != 0:
                bank_address = self.split_bank_address(bank_address_in_list)
                res = {
                    'value': {
                        'bank_address': bank_address
                    }
                }
            else :
                res = {
                    'value': {
                        'bank_address': ''
                    }
                }
        else:
            res = {}
        return res
    
    def split_bank_address(self,bank_address_in_list):
        address= []
        idx = 0
        for r in bank_address_in_list:
            address.append(r['address']) 
            combine = '\n \n \n'.join([str(i) for i in address])
        return combine

       