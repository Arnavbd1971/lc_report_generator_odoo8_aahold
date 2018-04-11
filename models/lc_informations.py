from openerp import models, fields, api, _
# from openerp.exceptions import ValidationError

class LCinformations(models.Model):
    _name = 'lc_informations.model'


    name = fields.Char(required=True, string='L/C No.')
    pi_no_id = fields.Many2one('sale.order',string='P/I No')
    pi_no = fields.Char(string='P/I No')
    created_date = fields.Date('L/C Created Dated', required=True, default=fields.Date.today())
    bank_name = fields.Many2one('bank_names_branch_address.model',required=True, string='LC Bank Name')
    bank_name2 = fields.Char(required=True, string='LC Bank Name')
    bank_branch = fields.Char(required=True, string='LC Bank Branch')
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


   
    def onchange_bank_name_branch(self, cr, uid, ids, bank_name, context=None):
        bank_name_id = bank_name
        if bank_name_id :
            service_obj = self.pool.get('bank_names_branch_address.model').browse(cr, uid,bank_name_id,context=context)
            lc_bank_name = service_obj.bank_name
            lc_bank_branch = service_obj.bank_branch
            lc_bank_address = service_obj.bank_address
            if lc_bank_branch and lc_bank_address:
                res = {
                    'value': {
                        'bank_name2': lc_bank_name,
                        'bank_branch': lc_bank_branch,
                        'bank_address': lc_bank_address,
                    }
                }
            else :
                res = {
                    'value': {
                        'bank_name2': '',
                        'bank_branch': '',
                        'bank_address': ''
                    }
                }
        else:
            res = {}
        return res

    def onchange_pi_no_id(self, cr, uid, ids, pi_no_id, context=None):   
        pi_no_id = pi_no_id
        if pi_no_id:
            service_obj = self.pool.get('sale.order').browse(cr, uid,pi_no_id,context=context)
            pi_no = service_obj.name
            if pi_no:
                res = {
                    'value': {
                        'pi_no': pi_no,
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

       