from openerp import models, fields, api, _


# Customer Invoice Model start

class CustomerInvoiceModel(models.Model):
    
    # _name = 'delivery.challan'
    _inherit = 'account.invoice'
    

    pi_no = fields.Char(string='P/I No')
    do_no = fields.Char(string='DO No')
    process = fields.Selection([('set_for_LC', 'set_for_LC'),('pandding', 'pandding')],'Process', default='pandding')
    process_status = fields.Char(string='Process', default='pandding')


    def create(self, cr, uid, vals, context=None):
        if vals.get('origin'):
            delivery_challan_no = vals.get('origin')
            if delivery_challan_no :
                stock_picking_ids = self.pool.get('stock.picking').search(cr, uid,[('name','=',delivery_challan_no),],context=context)
                pi_num_list = self.pool.get('stock.picking').read(cr, uid,stock_picking_ids,['origin','do_no'], context=context)
                if not pi_num_list:
                    pi_no = ''
                    vals['pi_no'] =   pi_no
                else:    
                    pi_no = self.split_from_list(pi_num_list,'origin')
                    vals['pi_no'] =   pi_no 

                    do_no = self.split_from_list(pi_num_list,'do_no')
                    vals['do_no'] =   do_no 

        new_id = super(CustomerInvoiceModel, self).create(cr, uid, vals, context=context)    
        return new_id

    def split_from_list(self,list_name,data_field):
        save = []
        for r in list_name:
            save.append(r[data_field])
            combine = '\n'.join([str(i) for i in save])
        return combine  

    def onchange_process(self, cr, uid, ids, process=False, context=None):    
        res= {}
        if process:
             res = {'value':{
                'process_status':process,
             }}
        else:
            res={}  
        return res     


# Customer Invoice Model end

# def create(self, cr, uid, vals, context=None):
#         if vals.get('origin'):
#             delivery_challan_no = vals.get('origin')

#             stock_picking_ids = self.pool.get('stock.picking').search(cr, uid,[('name','=',delivery_challan_no),],context=context)
#             if stock_picking_ids:
#                 pi_num_list = self.pool.get('stock.picking').read(cr, uid,stock_picking_ids,['origin'], context=context)

#                 if not pi_num_list:
#                      pi_no = None
#                     vals['pi_no'] =   pi_no
#                 else :    
#                     pi_no = self.split_from_list(pi_num_list)
#                     vals['pi_no'] =   pi_no 

#         new_id = super(CustomerInvoiceModel, self).create(cr, uid, vals, context=context)    
#         return new_id

#     def split_from_list(self,list_name,data_field):
#         save = []
#         for r in list_name:
#             save.append(r['origin'])
#             combine = '\n'.join([str(i) for i in save])
#         return combine