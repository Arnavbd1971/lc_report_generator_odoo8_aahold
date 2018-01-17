from openerp import models, fields, api,_
import datetime

# packing list Model start

class ForwardingLetterModel(models.Model):
    _name = 'forwarding_letter.model'

    commercial_invoice_id = fields.Many2one('commercial_invoice.model',string='Commercial Invoice No.', required=True)
    name = fields.Char(string='Ref.No', required=True)
    date = fields.Date(string='Created Date',default=fields.Date.today(), required=True)

    for_whom = fields.Char(string='Forwarding To', required=True)
    bank_name = fields.Char(string='Bank Name', required=True)
    bank_brunch = fields.Char(string='Bank Branch', required=True)
    bank_address = fields.Text(string='Bank Address', required=True)
    swift_code = fields.Char(string='Swift Code', required=True)


    lc_num = fields.Char(string='L/C No', required=True)
    lc_date = fields.Date(string='L/C Date', required=True)
    lc_num2 = fields.Char(string='lc_num', required=True)
    lc_date2 = fields.Date(string='lc_date', required=True)
    lc_bank_name = fields.Char(string='lc_bank_name', required=True)
    lc_bank_brunch = fields.Char(string='lc_bank_brunch', required=True)
    lc_bank_address = fields.Char(string='lc_bank_address', required=True)
    currency_symbol = fields.Char(string='currency_symbol', required=True)
    ordered_products_total_amount = fields.Char(string='Total', required=True)

    transfer_per = fields.Integer(string='Transfer Per', required=True)
    fc_account_no = fields.Char(string='F/C Account No', required=True)

    c1 = fields.Char(string='c1', required=True)
    c2 = fields.Char(string='c2', required=True)
    c3 = fields.Char(string='c3', required=True)
    c4 = fields.Char(string='c4', required=True)
    c5 = fields.Char(string='c5', required=True)
    c6 = fields.Char(string='c6', required=True)
    c7 = fields.Char(string='c7', required=True)
    c8 = fields.Char(string='c8', required=True)
    c9 = fields.Char(string='c9', required=True)



    # This function is for load data automatically in the existing field from another table
    def onchange_commercial_invoice_id(self, cr, uid, ids, commercial_invoice_id=False, context=None):
        res= {}
        if commercial_invoice_id:

            all_data_of_commercial_invoice = self.pool.get('commercial_invoice.model').browse(cr, uid, commercial_invoice_id,context=context)
            cus_invoice_id = all_data_of_commercial_invoice.customer_invoice_id
            proforma_invoice_id = all_data_of_commercial_invoice.proforma_invoice_id

            sale_order_id = self.pool.get('sale.order').search(cr, uid,[('name','=',proforma_invoice_id),],context=context)
            sale_order_data_list = self.pool.get('sale.order').read(cr, uid,sale_order_id,['beneficiary_bank_name2', 'beneficiary_bank_branch2','beneficiary_bank_address','swift_code'], context=context)
            beneficiary_bank_name = self.split_from_list(sale_order_data_list,'beneficiary_bank_name2')
            beneficiary_bank_branch = self.split_from_list(sale_order_data_list,'beneficiary_bank_branch2')
            beneficiary_bank_address = self.split_from_list(sale_order_data_list,'beneficiary_bank_address')
            swift_code = self.split_from_list(sale_order_data_list,'swift_code')

            
            service_obj= self.pool.get('account.invoice').browse(cr, uid,cus_invoice_id.id,context=context)
            currency_symbol= self.pool.get('res.currency').browse(cr, uid,service_obj.currency_id.id,context=context)


            lc_info_id = all_data_of_commercial_invoice.lc_num
            lc_info_pool_ids = self.pool.get('lc_informations.model').browse(cr, uid,lc_info_id.id,context=context)
            lc_num = lc_info_pool_ids.name
            lc_date = lc_info_pool_ids.created_date
            bank_name_id = lc_info_pool_ids.bank_name
            all_data_obj_of_bank_names = self.pool.get('bank_names.model').browse(cr, uid,bank_name_id.id,context=context)
            lc_bank_name = all_data_obj_of_bank_names.name
            lc_bank_branch_id = lc_info_pool_ids.bank_branch
            all_data_obj_of_bank_branch = self.pool.get('bank_branch.model').browse(cr, uid,lc_bank_branch_id.id,context=context)
            lc_bank_branch = all_data_obj_of_bank_branch.name
            lc_bank_address = lc_info_pool_ids.bank_address



            invoice_line_pool_ids = self.pool.get('account.invoice.line').search(cr, uid,[('invoice_id','=',cus_invoice_id.id),],context=context)

            invoice_lines_product_amount = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_subtotal'], context=context)

            ordered_products_total_amount = self.products_total_amount(invoice_lines_product_amount)


            now = datetime.datetime.now()
            uniq_num = 'AAYML-CERT/'+str(now.year)

            res = {'value':{
                'name': uniq_num,
                'lc_num':lc_num,
                'lc_date':lc_date,
                'lc_num2':lc_num, 
                'lc_date2':lc_date,
                'lc_bank_name':lc_bank_name,
                'lc_bank_brunch':lc_bank_branch,
                'lc_bank_address':lc_bank_address,
                'currency_symbol':currency_symbol.symbol,
                'ordered_products_total_amount':ordered_products_total_amount,
                'bank_name':beneficiary_bank_name,
                'bank_brunch':beneficiary_bank_branch,
                'bank_address':beneficiary_bank_address,
                'swift_code':swift_code,
            }}

        else:
            res={}  
        return res         

    def split_from_list(self,list_name,data_field):
        save = []
        for r in list_name:
            save.append(r[data_field])
            combine = '\n'.join([str(i) for i in save])
        return combine 

    def products_total_amount(self,invoice_lines_product_amount):
        total_amount= []
        idx = 0
        for r in invoice_lines_product_amount:
            total_amount.append(r['price_subtotal'])
            combine = sum(total_amount)
        return combine