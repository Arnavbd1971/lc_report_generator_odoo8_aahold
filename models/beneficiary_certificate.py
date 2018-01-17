from openerp import models, fields, api,_
import datetime

# packing list Model start

class BeneficiaryCertificateModel(models.Model):
    _name = 'beneficiary_certificate.model'


    commercial_invoice_id = fields.Many2one('commercial_invoice.model',string='Commercial Invoice No.', required=True)
    name = fields.Char(string='Ref.No', required=True)
    date = fields.Date(string=' Created Date',default=fields.Date.today(), required=True)

    ordered_products_total_quantity = fields.Char(string='ordered_products_total_quantity', required=True)
    commodity = fields.Char(string='commodity', required=True)
    customer_name = fields.Char(string='Buyer', required=True) 
    customer_full_address = fields.Char(string='Buyer Address', required=True) 
    commercial_invoice_no = fields.Char(string='Commercial Invoice no', required=True)
    commercial_invoice_created_date = fields.Date(string='commercial_invoice_created_date', required=True)
    proforma_invoice_no = fields.Char(string='proforma_invoice_no', required=True)
    proforma_invoice_created_date = fields.Date(string='proforma_invoice_created_date', required=True)

    truck_receipt_no = fields.Char(string='Truck Receipt No', required=True) 
    truck_challan_created_date = fields.Date(string='truck_challan_created_date', required=True)

    delivery_challan_no = fields.Char(string='Delivery Challan No.', required=True)
    delivery_challan_created_date = fields.Date(string='delivery_challan_created_date', required=True)

    lc_num = fields.Char(string='L/C No.', required=True)
    lc_date = fields.Date(string='lc_date', required=True)
    contact_no = fields.Char(string='contact_no', required=True)
    contact_no_date = fields.Date(string='contact_no_date', required=True)
    dealer_factory_name = fields.Char(string='Delivery From', required=True)



    



    # This function is for load data automatically in the existing field from another table
    def onchange_commercial_invoice_id(self, cr, uid, ids, commercial_invoice_id=False, context=None):
        res= {}
        if commercial_invoice_id:
            all_data_of_commercial_invoice = self.pool.get('commercial_invoice.model').browse(cr, uid, commercial_invoice_id,context=context)
            cus_invoice_id = all_data_of_commercial_invoice.customer_invoice_id
            cus_name = all_data_of_commercial_invoice.customer_name
            customer_full_address = all_data_of_commercial_invoice.customer_full_address
            commercial_invoice_no = all_data_of_commercial_invoice.name
            commercial_invoice_created_date = all_data_of_commercial_invoice.commercial_invoice_created_date
            proforma_invoice_no = all_data_of_commercial_invoice.proforma_invoice_id2
            proforma_invoice_created_date = all_data_of_commercial_invoice.proforma_invoice_created_date
            contact_no = all_data_of_commercial_invoice.contact_no
            contact_no_date = all_data_of_commercial_invoice.contact_no_date
            only_seq_num = all_data_of_commercial_invoice.only_seq_num
            supplier_factory_address= all_data_of_commercial_invoice.supplier_factory_address



            lc_num = all_data_of_commercial_invoice.lc_num
            all_data_obj_of_LC = self.pool.get('lc_informations.model').browse(cr, uid,lc_num.id,context=context)
            lc_num = all_data_obj_of_LC.name
            lc_date = all_data_obj_of_LC.created_date
            


            invoice_line_pool_ids = self.pool.get('account.invoice.line').search(cr, uid,[('invoice_id','=',cus_invoice_id),],context=context)

            invoice_lines_product_name = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['name'], context=context)

            invoice_lines_product_quantity = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['quantity'], context=context)

            ordered_products_total_quantity = self.products_total_quantity(invoice_lines_product_quantity)




            packing_list_pool_ids = self.pool.get('packing_list.model').search(cr, uid,[('commercial_invoice_no','=',commercial_invoice_no),],context=context)

            commodity_names = self.pool.get('packing_list.model').read(cr, uid,packing_list_pool_ids, ['commodity'], context=context)

            commodity = self.split_commodity(commodity_names)


            truck_challan_datas = self.pool.get('truck_challan.model').search(cr, uid,[('commercial_invoice_id','=',commercial_invoice_id),],context=context)

            dates = self.pool.get('truck_challan.model').read(cr, uid,truck_challan_datas, ['truck_challan_created_date'], context=context)

            truck_challan_created_date = self.split_truck_challan_created_date(dates)


            delivery_challan_datas = self.pool.get('delivery_challan.model').search(cr, uid,[('commercial_invoice_id','=',commercial_invoice_id),],context=context)

            dates = self.pool.get('delivery_challan.model').read(cr, uid,delivery_challan_datas, ['delivery_challan_created_date'], context=context)

            delivery_challan_created_date = self.split_delivery_challan_created_date(dates)


            now = datetime.datetime.now()
            uniq_num = 'AAYML-CERT/'+str(now.year)





            res = {'value':{
                'name': uniq_num,
                'ordered_products_total_quantity':ordered_products_total_quantity,
                'customer_name':cus_name, 
                'customer_full_address':customer_full_address, 
                'commercial_invoice_no':commercial_invoice_no,  
                'commercial_invoice_created_date':commercial_invoice_created_date,
                'proforma_invoice_no':proforma_invoice_no,
                'proforma_invoice_created_date':proforma_invoice_created_date,
                'lc_num':lc_num,
                'lc_date':lc_date,
                'contact_no':contact_no, 
                'contact_no_date':contact_no_date,
                'commodity':commodity,
                'truck_receipt_no':only_seq_num,
                'truck_challan_created_date':truck_challan_created_date,
                'delivery_challan_no':only_seq_num, 
                'delivery_challan_created_date':delivery_challan_created_date,
                'dealer_factory_name':supplier_factory_address,
            }}

        else:
            res={}  
        return res  


    def products_total_quantity(self,invoice_lines_product_quantity):
        total_quantity= []
        idx = 0
        for r in invoice_lines_product_quantity:
            total_quantity.append(r['quantity'])
            in_com = sum(total_quantity)
            combine = int(in_com)
        return combine           

    def split_commodity(self,commodity_names):
        names= []
        idx = 0
        for r in commodity_names:
            names.append(r['commodity'])
            combine = '\n \n'.join([str(i) for i in names])  
        return combine

    def split_truck_challan_created_date(self,dates):
        names= []
        idx = 0
        for r in dates:
            names.append(r['truck_challan_created_date'])
            combine = '\n \n'.join([str(i) for i in names])  
        return combine

    def split_delivery_challan_created_date(self,dates):
        names= []
        idx = 0
        for r in dates:
            names.append(r['delivery_challan_created_date'])
            combine = '\n \n'.join([str(i) for i in names])  
        return combine

    # def generateRefNo(self):

