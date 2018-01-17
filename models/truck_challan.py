from openerp import models, fields, api,_

# packing list Model start

class TruckChallanModel(models.Model):
    _name = 'truck_challan.model'

    name = fields.Char(string='Truck Receipt No.', required=True)

    commercial_invoice_id = fields.Many2one('commercial_invoice.model',string='Commercial Invoice No.', required=True)

    truck_challan_created_date = fields.Date(string='Created Date',default=fields.Date.today(), required=True)
    supplier_name = fields.Char(string='Supplier Name', required=True)
    supplier_address = fields.Text(string='Supplier Address', required=True)
    # supplier_address = fields.Many2one('delivery_address.model',string='Supplier Address', required=True)

    bank_name = fields.Char(string='Bank Name', required=True)
    bank_brunch = fields.Char(string='Bank Brunch', required=True)
    bank_addr = fields.Text(string='Bank Address', required=True)

    customer_name = fields.Char(string='Buyer Name', required=True)
    customer_full_address = fields.Text(string='Buyer Address', required=True)


    ordered_products_name = fields.Text(string='ordered_products_name') 
    ordered_products_number_of_bags = fields.Text(string='ordered_products_number_of_bags') 
    ordered_products_quantity = fields.Text(string='ordered_products_quantity')
    # expected_delivery_date = fields.Date(string='date', required=True)
    truck_no = fields.Char(string='Truck No.', required=True)
    total_bags = fields.Char(string='Total Bags')
    total_bags2 = fields.Char(string='Total Bags', required=True)
    ordered_products_total_quantity = fields.Char(string='ordered_products_total_quantity')

    gross_weight = fields.Char(string='Gross Weight', required=True)
    proforma_invoice_uniq_id = fields.Char(string='proforma_invoice_uniq_id', required=True)
    proforma_invoice_created_date = fields.Char(string='proforma_invoice_created_date', required=True)
    lc_num = fields.Char(string='L/C No.', required=True)
    lc_date = fields.Date(string='L/C Dated', required=True)
    contact_no = fields.Char(string='contact no', required=True)
    contact_no_date = fields.Date(string='contact_no_date', required=True)
    freight = fields.Char(string='Freight', required=True)



    
    # This function is for load data automatically in the existing field from another table
    def onchange_commercial_invoice_id(self, cr, uid, ids, commercial_invoice_id=False, context=None):
        res= {}
        if commercial_invoice_id:
            all_data_of_commercial_invoice = self.pool.get('commercial_invoice.model').browse(cr, uid, commercial_invoice_id,context=context)
            cus_invoice_id = all_data_of_commercial_invoice.customer_invoice_id
            proforma_invoice_id = all_data_of_commercial_invoice.proforma_invoice_id
            proforma_invoice_uniq_id = all_data_of_commercial_invoice.proforma_invoice_id2
            proforma_invoice_created_date= all_data_of_commercial_invoice.proforma_invoice_created_date
            seq_num = all_data_of_commercial_invoice.only_seq_num
            lc_info_id= all_data_of_commercial_invoice.lc_num   
            contact_no= all_data_of_commercial_invoice.contact_no
            contact_no_date= all_data_of_commercial_invoice.contact_no_date
            commercial_invoice_no= all_data_of_commercial_invoice.name

            supplier_factory_name_id = all_data_of_commercial_invoice.supplier_factory_name
            supplier_factory_datas = self.pool.get('supplier_factory_name_address.model').browse(cr, uid,supplier_factory_name_id.id,context=context)
            supplier_factory_name = supplier_factory_datas.name
            supplier_factory_address= all_data_of_commercial_invoice.supplier_factory_address




            lc_info_pool_ids = self.pool.get('lc_informations.model').browse(cr, uid,lc_info_id.id,context=context)
            lc_num = lc_info_pool_ids.name
            lc_date = lc_info_pool_ids.created_date
            bank_name_id = lc_info_pool_ids.bank_name
            all_data_obj_of_bank_names = self.pool.get('bank_names.model').browse(cr, uid,bank_name_id.id,context=context)
            bank_name = all_data_obj_of_bank_names.name
            bank_branch_id = lc_info_pool_ids.bank_branch
            all_data_obj_of_bank_branch = self.pool.get('bank_branch.model').browse(cr, uid,bank_branch_id.id,context=context)
            bank_branch = all_data_obj_of_bank_branch.name
            bank_addr = lc_info_pool_ids.bank_address





            all_data_obj_of_PI = self.pool.get('proforma_invoice.model').browse(cr, uid,proforma_invoice_id.id,context=context)
            num_of_bags = all_data_obj_of_PI.bags_of_packing

            service_obj= self.pool.get('account.invoice').browse(cr, uid,cus_invoice_id,context=context)
            service_obj2= self.pool.get('res.partner').browse(cr, uid,service_obj.partner_id.id,context=context)
            service_obj3= self.pool.get('res.country').browse(cr, uid,service_obj2.country_id.id,context=context)
            currency_symbol= self.pool.get('res.currency').browse(cr, uid,service_obj.currency_id.id,context=context)

            cus_name = service_obj2.name
            cus_full_address = str(service_obj2.street) + " , " + str(service_obj2.street2) + " , " + str(service_obj2.city)+ " - " + str(service_obj2.zip) + " , " + str(service_obj3.name)


            invoice_line_pool_ids = self.pool.get('account.invoice.line').search(cr, uid,[('invoice_id','=',cus_invoice_id),],context=context)

            invoice_lines_product_name = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['name'], context=context)

            invoice_lines_product_quantity = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['quantity'], context=context)


            expected_date_from_packing_list_ids = self.pool.get('packing_list.model').search(cr, uid,[('commercial_invoice_no','=',commercial_invoice_no),],context=context)

            # expected_date_data = self.pool.get('packing_list.model').read(cr, uid,expected_date_from_packing_list_ids,['expected_delivery_date'], context=context)


            ordered_products_names = self.split_products_names(invoice_lines_product_name) 

            ordered_products_number_of_bags = self.split_products_number_of_bags(invoice_lines_product_quantity,num_of_bags)

            ordered_products_quantity = self.split_products_quantity(invoice_lines_product_quantity)

            total_bags = self.total_bags_in_quantity(invoice_lines_product_quantity,num_of_bags)

            ordered_products_total_quantity = self.products_total_quantity(invoice_lines_product_quantity)

            gross_weight = self.calculation_of_gross_weight(invoice_lines_product_quantity)

            # expected_delivery_date = self.split_expected_delivery_date(expected_date_data)


            res = {'value':{
                'name' : seq_num,
                'bank_name':bank_name,
                'bank_brunch':bank_branch, 
                'bank_addr':bank_addr,
                'customer_name':cus_name, 
                'customer_full_address':cus_full_address,
                'ordered_products_name':ordered_products_names,
                'ordered_products_number_of_bags':ordered_products_number_of_bags, 
                'ordered_products_quantity':ordered_products_quantity, 
                'total_bags':"{:,}".format( total_bags ),
                'total_bags2':"{:,}".format( total_bags ),
                'ordered_products_total_quantity':"{:,}".format( ordered_products_total_quantity ),
                'gross_weight':gross_weight,
                'proforma_invoice_uniq_id':proforma_invoice_uniq_id,
                'proforma_invoice_created_date':proforma_invoice_created_date,
                'lc_num':lc_num,
                'lc_date':lc_date,
                'contact_no':contact_no, 
                'contact_no_date':contact_no_date, 
                'supplier_name':supplier_factory_name,  
                'supplier_address':supplier_factory_address,
                # 'expected_delivery_date':expected_delivery_date,
            }} 
        else:
            res={}  
        return res    



    def split_products_names(self,invoice_lines_product_name):
        names= []
        idx = 0
        for r in invoice_lines_product_name:
            names.append(r['name'])
            combine = '\n \n'.join([str(i) for i in names])  
        return combine

    def split_products_number_of_bags(self,invoice_lines_product_quantity,num_of_bags):
        number_of_bags= []
        idx = 0
        bags = int(num_of_bags)
        for r in invoice_lines_product_quantity:
            number_of_bags.append(int(r['quantity'] / bags))
            combine = '\n \n \n'.join([str(i) for i in number_of_bags])
        return combine

    def total_bags_in_quantity(self,invoice_lines_product_quantity,num_of_bags):
        number_of_bags= []
        idx = 0
        bags = int(num_of_bags)
        for r in invoice_lines_product_quantity:
            number_of_bags.append( int(r['quantity'] / bags)) 
            total = sum(number_of_bags)
        return total    

    

    def split_products_quantity(self,invoice_lines_product_quantity):
        quantity= []
        idx = 0
        for r in invoice_lines_product_quantity:
            quantity.append("{:,}".format( int(r['quantity'])) )
            combine = '\n \n \n'.join([str(i) for i in quantity])
        return combine

    # def split_expected_delivery_date(self,expected_delivery_date):
    #     date= []
    #     for r in expected_delivery_date:
    #         date.append(r['expected_delivery_date'])
    #         combine = '\n'.join([str(i) for i in date])
    #     return combine

    def products_total_quantity(self,invoice_lines_product_quantity):
        total_quantity= []
        idx = 0
        for r in invoice_lines_product_quantity:
            total_quantity.append(r['quantity'])
            in_com = sum(total_quantity)
            combine = int(in_com)
        return combine 

    def calculation_of_gross_weight(self,invoice_lines_product_quantity):
        squantity = []
        into = 1.04
        idx = 0
        for r in invoice_lines_product_quantity:
            squantity.append(r['quantity'])
            result = [  x * into  for x in squantity]
            # in_com = float(int(squantity))
            gross = "{:,}".format( int(sum(result)) )    

        return gross