from openerp import models, fields, api,_

# packing list Model start

class PackingListModel(models.Model):
    _name = 'delivery_challan.model'

    name = fields.Char(string='Delivery Challan No.', required=True)
    delivery_challan_created_date = fields.Date(string='Created Date', required=True,default=fields.Date.today())

    commercial_invoice_id = fields.Many2one('commercial_invoice.model',string='Commercial Invoice No.', required=True)

    customer_name = fields.Char(string='Buyer',required=True)
    customer_full_address = fields.Text(string='Buyer Address',required=True)

    ordered_products_name = fields.Text(string='ordered_products_name') 
    ordered_products_number_of_bags = fields.Text(string='ordered_products_number_of_bags') 
    ordered_products_quantity = fields.Text(string='ordered_products_quantity')
    total_bags = fields.Char(string='Total bags')
    ordered_products_total_quantity = fields.Char(string='Products total quantity') 
    delivery_order_no = fields.Char(string='Delivery Order No', required=True)
    do_date = fields.Date(string='D/O date', required=True)

    gross_weight = fields.Char(string='Gross weight',required=True)
    total_bags2 = fields.Char(string='total_bags', required=True)
    proforma_invoice_uniq_id = fields.Char(string='proforma_invoice_uniq_id', required=True)
    proforma_invoice_created_date = fields.Char(string='proforma_invoice_created_date', required=True)
    lc_num = fields.Char(string='L/C No.', required=True)
    lc_date = fields.Date(string='L/C Dated', required=True)
    contact_no = fields.Char(string='contact no', required=True)


    # This function is for load data automatically in the existing field from another table
    def onchange_commercial_invoice_id(self, cr, uid, ids, name=False, context=None):
        res= {}
        if name:

            all_data_of_commercial_invoice = self.pool.get('commercial_invoice.model').browse(cr, uid, name,context=context)
            cus_invoice_id = all_data_of_commercial_invoice.customer_invoice_id
            seq_num = all_data_of_commercial_invoice.only_seq_num
            proforma_invoice_id = all_data_of_commercial_invoice.pi_id
            proforma_invoice_uniq_id = all_data_of_commercial_invoice.proforma_invoice_id
            proforma_invoice_created_date= all_data_of_commercial_invoice.proforma_invoice_created_date
            contact_no= all_data_of_commercial_invoice.contact_no
            delivery_order_num= all_data_of_commercial_invoice.delivery_order_num
            delivery_challan_num= all_data_of_commercial_invoice.delivery_challan_num
            delivery_order_created_date= all_data_of_commercial_invoice.delivery_order_created_date
            num_of_bags = all_data_of_commercial_invoice.num_of_bags 

            service_obj= self.pool.get('sale.order').browse(cr, uid,proforma_invoice_id.id,context=context)
            lc_id = service_obj.lc_num_id
            lc_info_pool_ids = self.pool.get('lc_informations.model').browse(cr, uid,lc_id.id,context=context)
            lc_num = lc_info_pool_ids.name
            lc_date = lc_info_pool_ids.created_date

            service_obj2= self.pool.get('res.partner').browse(cr, uid,service_obj.partner_id.id,context=context)
            service_obj3= self.pool.get('res.country').browse(cr, uid,service_obj2.country_id.id,context=context)
            currency_symbol= self.pool.get('res.currency').browse(cr, uid,service_obj.currency_id.id,context=context)
            cus_name = service_obj2.name
            cus_full_address = str(service_obj2.street) + " , " + str(service_obj2.street2) + " , " + str(service_obj2.city)+ " - " + str(service_obj2.zip) + " , " + str(service_obj3.name)

            account_invoice_ids = self.pool.get('account.invoice').search(cr, uid,[('pi_no','=',service_obj.name),('process','=','set_for_LC')],context=context)
            if not account_invoice_ids:
                # print('Account invoice list is empty.')
                raise Warning(_('Account invoice list is empty.'))
            else:
                invoice_line_pool_ids = self.pool.get('account.invoice.line').search(cr, uid,[('invoice_id','=',account_invoice_ids),],context=context)
                invoice_lines_product_name = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['name'], context=context)
                invoice_lines_product_quantity = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['quantity','name'], context=context)
                
                ordered_products_names = self.split_products_names(invoice_lines_product_name) 

                ordered_products_number_of_bags = self.split_products_number_of_bags(invoice_lines_product_quantity,num_of_bags)

                ordered_products_quantity = self.split_products_quantity(invoice_lines_product_quantity)

                total_bags = self.total_bags_in_quantity(invoice_lines_product_quantity,num_of_bags)

                ordered_products_total_quantity = self.products_total_quantity(invoice_lines_product_quantity)

                total_gross_weight = self.calculation_of_total_gross_weight(invoice_lines_product_quantity)



            res = {'value':{
                'name': seq_num,
                # 'name': delivery_challan_num,
                'customer_name':cus_name, 
                'customer_full_address':cus_full_address,
                'ordered_products_name':ordered_products_names,
                'ordered_products_number_of_bags':ordered_products_number_of_bags, 
                'ordered_products_quantity':ordered_products_quantity, 
                'total_bags':"{:,}".format( total_bags ),
                'ordered_products_total_quantity':"{:,}".format( ordered_products_total_quantity ),
                'gross_weight':total_gross_weight,
                'total_bags2':"{:,}".format( total_bags ),
                'proforma_invoice_uniq_id':proforma_invoice_uniq_id,
                'proforma_invoice_created_date':proforma_invoice_created_date,
                'lc_num':lc_num,
                'lc_date':lc_date,
                'contact_no':contact_no,
                'delivery_order_no':delivery_order_num,
                'do_date':delivery_order_created_date,
            }}
        else:
            res={}  
        return res     




    def split_products_names(self,invoice_lines_product_name):
        seen = set()
        answer = []
        names= []
        for r in invoice_lines_product_name:
            names.append(r['name'])
            combine_names = '\n'.join([str(i) for i in names])
            for line in combine_names.splitlines():
                if line not in seen:
                    seen.add(line)
                    answer.append(line)
                    combine = '\n'.join(answer)
        return combine

    def split_products_number_of_bags(self,invoice_lines_product_quantity,num_of_bags):
        number_of_bags= []
        bags = int(num_of_bags)
        testListDict = {}
        for item in invoice_lines_product_quantity:
            try:
                d=item['name']
                testListDict[d] += int(item['quantity'] / bags)
            except:
                d=item['name']
                testListDict[d] = int(item['quantity'] / bags)
        
        for the_key, the_value in testListDict.iteritems():
            number_of_bags.append(the_value)
            combine = '\n \n'.join([str(i) for i in number_of_bags])
        return combine

    def total_bags_in_quantity(self,invoice_lines_product_quantity,num_of_bags):
        number_of_bags= []
        testListDict = {}
        bags = int(num_of_bags)
        for item in invoice_lines_product_quantity:
            try:
                d=item['name']
                testListDict[d] += int(item['quantity']) 
            except:
                d=item['name']
                testListDict[d] = int(item['quantity'])
        for the_key, the_value in testListDict.iteritems():
            number_of_bags.append(int(the_value / bags)) 
            total = sum(number_of_bags)
        return total     

    def split_products_quantity(self,invoice_lines_product_quantity):
        quantity= []
        testListDict = {}
        for item in invoice_lines_product_quantity:
            try:
                d=item['name']
                testListDict[d] += int(item['quantity']) 
            except:
                d=item['name']
                testListDict[d] = int(item['quantity'])

        for the_key, the_value in testListDict.iteritems():
            quantity.append(the_value)
            combine = '\n \n'.join([str(i) for i in quantity])
        return combine

    def products_total_quantity(self,invoice_lines_product_quantity):
        total_quantity= []
        for r in invoice_lines_product_quantity:
            total_quantity.append(r['quantity'])
            in_com = sum(total_quantity)
            combine = int(in_com)
        return combine 

    def calculation_of_total_gross_weight(self,invoice_lines_product_quantity):
        squantity = []
        testListDict = {}
        into = 1.04
        for item in invoice_lines_product_quantity:
            try:
                d=item['name']
                testListDict[d] += int(item['quantity']) 
            except:
                d=item['name']
                testListDict[d] = int(item['quantity'])
        for the_key, the_value in testListDict.iteritems():
            squantity.append(the_value)
            result = [ x * into for x in squantity]
            gross = int(sum(result))    

        return gross