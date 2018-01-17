from openerp import models, fields, api,_
import datetime

# packing list Model start

class BeneficiaryCertificateModel(models.Model):
    _name = 'certificate_of_origin.model'

    commercial_invoice_id = fields.Many2one('commercial_invoice.model',string='Commercial Invoice No.', required=True)
    name = fields.Char(string='Ref.No', required=True)
    date = fields.Date(string='Created Date', required=True,default=fields.Date.today())

    supplied_product = fields.Char(string='Supplied Product', required=True)
    lc_num = fields.Char(string='L/C No.', required=True)
    lc_date = fields.Date(string='lc_date', required=True)
    contact_no = fields.Char(string='contact_no', required=True)
    commercial_invoice_no = fields.Char(string='Commercial Invoice no', required=True)
    commercial_invoice_created_date = fields.Date(string='commercial_invoice_created_date', required=True)
    delivery_challan_no = fields.Char(string='Delivery Challan No.', required=True)
    delivery_challan_created_date = fields.Date(string='delivery_challan_created_date', required=True)
    country_of_origin = fields.Char(string='Country Of Origin', required=True)
    dealer_factory_name = fields.Char(string='Delivery From', required=True)



    # This function is for load data automatically in the existing field from another table
    def onchange_commercial_invoice_id(self, cr, uid, ids, commercial_invoice_id=False, context=None):
        res= {}
        if commercial_invoice_id:

            all_data_of_commercial_invoice = self.pool.get('commercial_invoice.model').browse(cr, uid, commercial_invoice_id,context=context)
            cus_invoice_id = all_data_of_commercial_invoice.customer_invoice_id
            contact_no = all_data_of_commercial_invoice.contact_no
            commercial_invoice_no = all_data_of_commercial_invoice.name
            commercial_invoice_created_date = all_data_of_commercial_invoice.commercial_invoice_created_date
            delivery_challan_no = all_data_of_commercial_invoice.only_seq_num
            country_of_origin = all_data_of_commercial_invoice.country_of_origin2
            supplier_factory_address= all_data_of_commercial_invoice.supplier_factory_address

            lc_num = all_data_of_commercial_invoice.lc_num
            all_data_obj_of_LC = self.pool.get('lc_informations.model').browse(cr, uid,lc_num.id,context=context)
            lc_num = all_data_obj_of_LC.name
            lc_date = all_data_obj_of_LC.created_date


            delivery_challan_datas = self.pool.get('delivery_challan.model').search(cr, uid,[('commercial_invoice_id','=',commercial_invoice_id),],context=context)

            dates = self.pool.get('delivery_challan.model').read(cr, uid,delivery_challan_datas, ['delivery_challan_created_date'], context=context)

            if dates: 
                delivery_challan_created_date = self.split_delivery_challan_created_date(dates)
            else:
                delivery_challan_created_date = ''    


            now = datetime.datetime.now()
            uniq_num = 'AAYML-CO/'+str(now.year)

            res = {'value':{
                'name': uniq_num,
                'lc_num':lc_num,
                'lc_date':lc_date,
                'contact_no':contact_no, 
                'commercial_invoice_no':commercial_invoice_no,  
                'commercial_invoice_created_date':commercial_invoice_created_date,
                'delivery_challan_no':delivery_challan_no,  
                'delivery_challan_created_date':delivery_challan_created_date,
                'country_of_origin':country_of_origin,
                'dealer_factory_name':supplier_factory_address,
            }}


        else:
            res={}  
        return res        


    def split_delivery_challan_created_date(self,dates):
        names= []
        idx = 0
        for r in dates:
            names.append(r['delivery_challan_created_date'])
            combine = '\n \n'.join([str(i) for i in names])  
        return combine