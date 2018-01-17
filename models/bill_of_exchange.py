from openerp import models, fields, api,_
import datetime

# packing list Model start

class BillOfExchangeModel(models.Model):
    _name = 'bill_of_exchange.model'

    name = fields.Char(string='name')
    bill_of_exchange_created_date = fields.Date(string='Created Date', default=fields.Date.today(), required=True)


    commercial_invoice_id = fields.Many2one('commercial_invoice.model',string='Commercial Invoice No.', required=True)

    ordered_products_total_amount = fields.Char(string='ordered_products_total_amount', required=True)
    ordered_products_total_amount_in_word = fields.Char(string='ordered_products_total_amount_in_word', required=True)
    currency_symbol_name = fields.Char(string='currency_symbol_name', required=True)
    currency_symbol_name2 = fields.Char(string='currency_symbol_name', required=True)
    currency_symbol = fields.Char(string='currency_symbol', required=True)
    currency_symbol2 = fields.Char(string='currency_symbol', required=True)
    days = fields.Char(string='days', required=True)

    bank_name = fields.Char(string='Bank Name' , required=True)
    bank_brunch = fields.Char(string='Bank Brunch' , required=True)
    bank_address = fields.Char(string='Bank Address' , required=True)
    swift_code = fields.Char(string='Swift Code' , required=True)


    customer_name = fields.Char(string='Customer Name', required=True)
    customer_full_address = fields.Text(string='Customer Address' , required=True)

    lc_num = fields.Char(string='L/C No' , required=True)
    lc_date = fields.Date(string='L/C Date', required=True)
    lc_bank_name = fields.Char(string='lc_bank_name' , required=True)
    lc_bank_name2 = fields.Char(string='lc_bank_name' , required=True)
    lc_bank_brunch = fields.Char(string='lc_bank_branch' , required=True)
    lc_bank_address = fields.Char(string='lc_bank_address' , required=True)

    contact_no = fields.Char(string='contact_no', required=True)
    contact_no_date = fields.Date(string='contact_no_date', required=True)

    company_name = fields.Many2one('beneficiary_full_name.model',string='Company name', required=True)

    


    # This function is for load data automatically in the existing field from another table
    def onchange_commercial_invoice_id(self, cr, uid, ids, commercial_invoice_id=False, context=None):
        res= {}
        if commercial_invoice_id:

            all_data_of_commercial_invoice = self.pool.get('commercial_invoice.model').browse(cr, uid, commercial_invoice_id,context=context)
            cus_invoice_id = all_data_of_commercial_invoice.customer_invoice_id
            proforma_invoice_id = all_data_of_commercial_invoice.proforma_invoice_id
            contact_no = all_data_of_commercial_invoice.contact_no
            contact_no_date = all_data_of_commercial_invoice.contact_no_date


            all_data_obj_of_PI = self.pool.get('proforma_invoice.model').browse(cr, uid,proforma_invoice_id.id,context=context)
            beneficiary_bank_name_id = all_data_obj_of_PI.beneficiary_bank_name
            all_data_obj_of_beneficiary_bank_names = self.pool.get('bank_names.model').browse(cr, uid,beneficiary_bank_name_id.id,context=context)
            beneficiary_bank_name = all_data_obj_of_beneficiary_bank_names.name

            beneficiary_bank_branch_id = all_data_obj_of_PI.beneficiary_bank_branch
            all_data_obj_of_beneficiary_bank_branch = self.pool.get('bank_branch.model').browse(cr, uid,beneficiary_bank_branch_id.id,context=context)
            beneficiary_bank_branch = all_data_obj_of_beneficiary_bank_branch.name

            beneficiary_bank_address = all_data_obj_of_PI.beneficiary_bank_address
            swift_code = all_data_obj_of_PI.swift_code


            service_obj= self.pool.get('account.invoice').browse(cr, uid,cus_invoice_id,context=context)
            service_obj2= self.pool.get('res.partner').browse(cr, uid,service_obj.partner_id.id,context=context)
            service_obj3= self.pool.get('res.country').browse(cr, uid,service_obj2.country_id.id,context=context)
            currency_symbol= self.pool.get('res.currency').browse(cr, uid,service_obj.currency_id.id,context=context)

            cus_name = service_obj2.name
            cus_full_address = str(service_obj2.street) + " , " + str(service_obj2.street2) + " , " + str(service_obj2.city)+ " - " + str(service_obj2.zip) + " , " + str(service_obj3.name)


            lc_num = all_data_of_commercial_invoice.lc_num
            all_data_obj_of_LC = self.pool.get('lc_informations.model').browse(cr, uid,lc_num.id,context=context)
            lc_num = all_data_obj_of_LC.name
            lc_date = all_data_obj_of_LC.created_date
            lc_bank_name_id = all_data_obj_of_LC.bank_name
            all_data_obj_of_bank_names = self.pool.get('bank_names.model').browse(cr, uid,lc_bank_name_id.id,context=context)
            lc_bank_name = all_data_obj_of_bank_names.name
            lc_bank_branch_id = all_data_obj_of_LC.bank_branch
            all_data_obj_of_bank_branch = self.pool.get('bank_branch.model').browse(cr, uid,lc_bank_branch_id.id,context=context)
            lc_bank_branch = all_data_obj_of_bank_branch.name
            lc_bank_address = all_data_obj_of_LC.bank_address



            invoice_line_pool_ids = self.pool.get('account.invoice.line').search(cr, uid,[('invoice_id','=',cus_invoice_id),],context=context)

            invoice_lines_product_amount = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_subtotal'], context=context)


            ordered_products_total_amount = self.products_total_amount(invoice_lines_product_amount)

            ordered_products_total_amount_in_word = self.numToWords(ordered_products_total_amount)

            res = {'value':{
                'ordered_products_total_amount': "{:,}".format( ordered_products_total_amount) ,
                'ordered_products_total_amount_in_word':ordered_products_total_amount_in_word,
                'bank_name':beneficiary_bank_name,
                'bank_brunch':beneficiary_bank_branch,
                'bank_address':beneficiary_bank_address,
                'swift_code':swift_code,
                'currency_symbol_name':currency_symbol.name,
                'currency_symbol':currency_symbol.symbol,
                'currency_symbol_name2':currency_symbol.name,
                'currency_symbol2':currency_symbol.symbol,
                'customer_name':cus_name,
                'customer_full_address':cus_full_address,
                'lc_num':lc_num,
                'lc_date':lc_date,
                'lc_bank_name':lc_bank_name,
                'lc_bank_name2':lc_bank_name,
                'lc_bank_brunch':lc_bank_branch,
                'lc_bank_address':lc_bank_address,
                'contact_no':contact_no, 
                'contact_no_date':contact_no_date,
            }}

        else:
            res={}  
        return res     



    def products_total_amount(self,invoice_lines_product_amount):
        total_amount= []
        idx = 0
        for r in invoice_lines_product_amount:
            total_amount.append(r['price_subtotal'])
            combine = sum(total_amount)
        return combine


    def numToWords(self,num,join=True):
        '''words = {} convert an integer number into words'''
        units = ['','one','two','three','four','five','six','seven','eight','nine']
        teens = ['','eleven','twelve','thirteen','fourteen','fifteen','sixteen', \
                'seventeen','eighteen','nineteen']
        tens = ['','ten','twenty','thirty','forty','fifty','sixty','seventy', \
                'eighty','ninety']
        thousands = ['','thousand','million','billion','trillion','quadrillion', \
                    'quintillion','sextillion','septillion','octillion', \
                    'nonillion','decillion','undecillion','duodecillion', \
                    'tredecillion','quattuordecillion','sexdecillion', \
                    'septendecillion','octodecillion','novemdecillion', \
                    'vigintillion']
        words = []
        if num==0: words.append('zero')
        else:
            numStr = '%d'%num
            numStrLen = len(numStr)
            groups = (numStrLen+2)/3
            numStr = numStr.zfill(groups*3)
            for i in range(0,groups*3,3):
                h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
                g = groups-(i/3+1)
                if h>=1:
                    words.append(units[h])
                    words.append('hundred')
                if t>1:
                    words.append(tens[t])
                    if u>=1: words.append(units[u])
                elif t==1:
                    if u>=1: words.append(teens[u])
                    else: words.append(tens[t])
                else:
                    if u>=1: words.append(units[u])
                if (g>=1) and ((h+t+u)>0): words.append(thousands[g]+',')
        if join: return ' '.join(words)
        return words