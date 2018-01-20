from openerp import models, fields, api,_

# packing list Model start

class PackingListModel(models.Model):
    _name = 'packing_list.model'


    name = fields.Many2one('commercial_invoice.model',string='Commercial Invoice No.', required=True)
    commercial_invoice_no = fields.Char(string='commercial_invoice_no')
    packing_list_created_date = fields.Date(string='Created Date', default=fields.Date.today(), required=True)
    customer_name = fields.Char(string='Buyer', required=True)
    customer_name2 = fields.Char(string='Buyer', required=True)
    customer_full_address = fields.Text(string='Buyer Address', required=True)
    commodity = fields.Char(string='Commodity', required=True)

    delivery_form = fields.Text(string='Delivery From', required=True)
    

    ordered_products_name = fields.Text(string='ordered_products_name') 
    ordered_products_number_of_bags = fields.Text(string='ordered_products_number_of_bags') 
    ordered_products_quantity = fields.Text(string='ordered_products_quantity')
    gross_weights = fields.Text(string='gross weights')
    total_gross_weight = fields.Char(string='gross weight')
    total_gross_weight2 = fields.Char(string='gross weight', required=True)
    total_bags = fields.Char(string='Total Bags')
    total_bags2 = fields.Char(string='Total Bags', required=True)


    num_of_bags = fields.Integer(string='Number of bags', required=True) 
    proforma_invoice_uniq_id = fields.Char(string='Proforma Invoice No.', required=True)
    proforma_invoice_created_date = fields.Date(string='proforma_invoice_created_date', required=True)
    lc_num = fields.Char(string='L/C No.', required=True)
    lc_num2 = fields.Char(string='L/C No.', required=True)
    lc_date = fields.Date(string='L/C Dated', required=True)
    lc_date2 = fields.Date(string='L/C Dated', required=True)

    contact_no = fields.Char(string='contact no', required=True)
    



    # This function is for load data automatically in the existing field from another table
    def onchange_commercial_invoice_id(self, cr, uid, ids, name=False, context=None):
        res= {}
        if name:
            all_data_of_commercial_invoice = self.pool.get('commercial_invoice.model').browse(cr, uid, name,context=context)

            cus_invoice_id = all_data_of_commercial_invoice.customer_invoice_id
            commercial_invoice_no = all_data_of_commercial_invoice.name
            proforma_invoice_id = all_data_of_commercial_invoice.proforma_invoice_id
            proforma_invoice_uniq_id = all_data_of_commercial_invoice.proforma_invoice_id
            proforma_invoice_created_date= all_data_of_commercial_invoice.proforma_invoice_created_date
            lc_info_id= all_data_of_commercial_invoice.lc_num   
            contact_no= all_data_of_commercial_invoice.contact_no
            supplier_factory_address= all_data_of_commercial_invoice.supplier_factory_address
            num_of_bags = all_data_of_commercial_invoice.num_of_bags  


            lc_info_pool_ids = self.pool.get('lc_informations.model').browse(cr, uid,lc_info_id.id,context=context)
            lc_num = lc_info_pool_ids.name
            lc_date = lc_info_pool_ids.created_date


            service_obj= self.pool.get('account.invoice').browse(cr, uid,cus_invoice_id.id,context=context)
            service_obj2= self.pool.get('res.partner').browse(cr, uid,service_obj.partner_id.id,context=context)
            service_obj3= self.pool.get('res.country').browse(cr, uid,service_obj2.country_id.id,context=context)
            currency_symbol= self.pool.get('res.currency').browse(cr, uid,service_obj.currency_id.id,context=context)

            cus_name = service_obj2.name
            cus_full_address = str(service_obj2.street) + " , " + str(service_obj2.street2) + " , " + str(service_obj2.city)+ " - " + str(service_obj2.zip) + " , " + str(service_obj3.name)



            invoice_line_pool_ids = self.pool.get('account.invoice.line').search(cr, uid,[('invoice_id','=',cus_invoice_id.id),],context=context)

            invoice_lines_product_name = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['name'], context=context)

            invoice_lines_product_quantity = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['quantity'], context=context)

            invoice_lines_product_price_of_unit = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_unit'], context=context)

            invoice_lines_product_amount = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_subtotal'], context=context)


            ordered_products_names = self.split_products_names(invoice_lines_product_name) 

            ordered_products_number_of_bags = self.split_products_number_of_bags(invoice_lines_product_quantity,num_of_bags)

            ordered_products_quantity = self.split_products_quantity(invoice_lines_product_quantity)

            gross_weights = self.calculation_of_gross_weights(invoice_lines_product_quantity)

            total_gross_weight = self.calculation_of_total_gross_weight(invoice_lines_product_quantity)

            total_bags = self.total_bags_in_quantity(invoice_lines_product_quantity,num_of_bags)





            res = {'value':{
                'commercial_invoice_no':commercial_invoice_no,
                'customer_name' : cus_name,
                'customer_name2' : cus_name,
                'customer_full_address' : cus_full_address,
                'ordered_products_name':ordered_products_names,
                'ordered_products_number_of_bags':ordered_products_number_of_bags,
                'ordered_products_quantity':ordered_products_quantity,
                'gross_weights':gross_weights,
                'total_gross_weight':"{:,}".format( total_gross_weight ),
                'total_gross_weight2':"{:,}".format( total_gross_weight ),
                'total_bags':"{:,}".format( total_bags ),
                'total_bags2':"{:,}".format( total_bags ),
                'num_of_bags':num_of_bags,
                'proforma_invoice_uniq_id':proforma_invoice_uniq_id,
                'proforma_invoice_created_date':proforma_invoice_created_date,
                'lc_num':lc_num,
                'lc_num2':lc_num,
                'lc_date':lc_date, 
                'lc_date2':lc_date,
                'contact_no':contact_no, 
                'delivery_form':supplier_factory_address,
            }} 
        else:
            res={}  
        return res    



    def split_products_names(self,invoice_lines_product_name):
        names= []
        idx = 0
        for r in invoice_lines_product_name:
            names.append(r['name'])
            combine = '\n'.join([str(i) for i in names])  
        return combine

    def split_products_number_of_bags(self,invoice_lines_product_quantity,num_of_bags):
        number_of_bags= []
        idx = 0
        bags = int(num_of_bags)
        for r in invoice_lines_product_quantity:
            number_of_bags.append("{:,}".format( int(r['quantity'] / bags)) )
            combine = '\n \n'.join([str(i) for i in number_of_bags])
        return combine

    def total_bags_in_quantity(self,invoice_lines_product_quantity,num_of_bags):
        number_of_bags= []
        idx = 0
        bags = int(num_of_bags)
        for r in invoice_lines_product_quantity:
            number_of_bags.append(int(r['quantity'] / bags)) 
            total = sum(number_of_bags)
        return total    

    def split_products_quantity(self,invoice_lines_product_quantity):
        quantity= []
        idx = 0
        for r in invoice_lines_product_quantity:
            quantity.append("{:,}".format( int(r['quantity'])) )
            combine = '\n \n'.join([str(i) for i in quantity])
        return combine


    def calculation_of_gross_weights(self,invoice_lines_product_quantity):
        gross_weights = []
        into = 1.04
        for r in invoice_lines_product_quantity:
            gross_weights.append(r['quantity'])
            result = [ "{:,}".format( int(x * into) ) for x in gross_weights]
            # gross = int(result) 
            combine = '\n \n'.join([str(i) for i in result])   

        return combine

    def calculation_of_total_gross_weight(self,invoice_lines_product_quantity):
        squantity = []
        into = 1.04
        idx = 0
        for r in invoice_lines_product_quantity:
            squantity.append(r['quantity'])
            result = [ x * into for x in squantity]
            gross = int(sum(result))    

        return gross

    # def onchange_expected_delivery_date(self, cr, uid, ids, expected_delivery_date, context=None):

    #     expected_delivery_date = expected_delivery_date

    #     res = {}

    #     if expected_delivery_date :
    #         res = {
    #             'value': {
    #                     'expected_delivery_date2' : expected_delivery_date
    #                 }
    #         }
    #     else:
    #         res = {
    #             'value': {
    #                     'expected_delivery_date2' : ''
    #                 }
    #         }

    #     return res  

    # def onchange_supplier_factory_name(self, cr, uid, ids, supplier_factory_name=False, context=None):
    #     res= {}
    #     if supplier_factory_name:
    #         service_obj= self.pool.get('supplier_factory_name_address.model')
    #         rec = service_obj.browse(cr, uid, supplier_factory_name)
    #         res = {'value':{
    #             'supplier_factory_address':rec.address
    #             }}
    #     else:
    #         res={}  
    #     return res      