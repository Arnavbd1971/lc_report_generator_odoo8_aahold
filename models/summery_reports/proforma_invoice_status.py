from openerp import models, fields, api,_
from openerp import exceptions

class ProformaInvoiceStatus(models.Model):
    _name = 'proforma_invoice_status.model'

    name = fields.Char(string='Report No.')

    created_date = fields.Date(string='Created Date', default=fields.Date.today())
    
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')


    test = fields.Text(string='Test')


    def onchange_from_date(self, cr, uid, ids, from_date=False, context=None):

        res= {}
        ffrom_date = from_date
        if ffrom_date:
            res = {'value':{
                'from_date':ffrom_date,
                }}
        else:
            res = {'value':{
                'from_date':'',
                }}        
        return res

    def onchange_to_date(self, cr, uid, ids, from_date=False, to_date=False, context=None):
    # def onchange_to_date(self, cr, uid, ids, to_date=False):

        res= {}
        ffrom_date = from_date
        tto_date = to_date 
        if tto_date:

            # cr = self.env.cr
            cr.execute("SELECT id, name, proforma_invoice_created_date FROM proforma_invoice_model WHERE proforma_invoice_created_date BETWEEN %s AND %s ", (str(ffrom_date),str(tto_date)) )
            datas = cr.fetchall()

            res = {'value':{
                'test':datas,
                }}
        else:
            res = {'value':{
                'test':'',
                }}        
        return res      



    # def get_selection(self, cr, uid, context):
    #     res= {}
    #     cr = self.env.cr
    #     cr.execute("SELECT id,name FROM proforma_invoice_model WHERE proforma_invoice_created_date='2017-12-28' ")

    #     datas = cr.fetchall()

    #     if datas:
    #         res = {'value':{
    #             'test':datas,
    #             }}
    #     else:
    #         res= {}        

    #     return 