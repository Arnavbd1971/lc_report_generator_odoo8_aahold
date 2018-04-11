from openerp import models, fields, api, _


class CustomerInvoiceModel(models.Model):

    _inherit = 'account.invoice'

    pi_no = fields.Char(string='P/I No')

    # def create(self, cr, uid, vals, context=None):
    #     if vals.get('origin'):
    #         delivery_challan_no = vals.get('origin')
    #         if delivery_challan_no :
    #             stock_picking_ids = self.pool.get('stock.picking').search(cr, uid,[('name','=',delivery_challan_no),],context=context)
    #             pi_num_list = self.pool.get('stock.picking').read(cr, uid,stock_picking_ids,['origin'], context=context)
    #             if not pi_num_list:
    #                 pi_no = ''
    #                 vals['pi_no'] =   pi_no
    #             else:    
    #                 pi_no = self.split_from_list(pi_num_list)
    #                 vals['pi_no'] =   pi_no  

    #     new_id = super(CustomerInvoiceModel, self).create(cr, uid, vals, context=context)    
    #     return new_id

    # def split_from_list(self,list_name):
    #     save = []
    #     for r in list_name:
    #         save.append(r['origin'])
    #         combine = '\n'.join([str(i) for i in save])
    #     return combine      
