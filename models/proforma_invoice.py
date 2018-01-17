from openerp import models, fields, api,_
from openerp import exceptions

class ProformaInvoiceModel(models.Model):
    _name = 'proforma_invoice.model'

    _rec_name = "name"

    name = fields.Char(string='P/I No.', size=100, readonly=True)
    proforma_invoice_created_date = fields.Date(string='Created Date', readonly=True,default=fields.Date.today(), required=True)
    validity_date = fields.Date(string='Validity Date', default=fields.Date.today(), required=True)

    account_invoice_id = fields.Many2one('account.invoice',string='Customer Invoice No.', required=True)

    customer_name = fields.Char(string='Customer Name',required=True)
    customer_full_address = fields.Text(string='Customer Address',required=True) 

    ordered_products_name = fields.Text(string='ordered_products_name') 
    ordered_products_price_of_unit = fields.Text(string='ordered_products_price_of_unit') 
    ordered_products_quantity = fields.Text(string='ordered_products_quantity')
    ordered_products_amount = fields.Text(string='ordered_products_amount')

    ordered_products_total_quantity = fields.Char(string='ordered_products_total_quantity') 
    ordered_products_total_amount = fields.Char(string='Total')
    ordered_products_total_amount_in_word = fields.Char(string='ordered_products_total_amount_in_word')

    currency_symbol_name = fields.Char(string='currency_symbol_name')
    currency_symbol_name1 = fields.Char(string='currency_symbol_name')
    currency_symbol_name2 = fields.Char(string='currency_symbol_name')
    currency_symbol = fields.Char(string='')
    currency_symbol1 = fields.Char(string='')
    currency_symbol2 = fields.Char(string='')

    beneficiary_full_name = fields.Many2one('beneficiary_full_name.model',string='Beneficiary Full Name',required=True) 
    # beneficiary_full_name = fields.One2many('behalf_of',string='Beneficiary Full Name',copy=True) 
    erc_no = fields.Char(string='ERC NO.',required=True)
    method_of_payment = fields.Many2one('method_of_payment.model',string='Method of Payment',required=True)
    reimbursement = fields.Many2one('reimbursement.model',string='Reimbursement',required=True)

    beneficiary_bank_name = fields.Many2one('bank_names.model',string='Beneficiary Bank Name',required=True)
    beneficiary_bank_branch = fields.Many2one('bank_branch.model',string='Beneficiary Bank Branch',required=True)
    beneficiary_bank_address = fields.Text(string='Beneficiary Bank Address',required=True)
    swift_code = fields.Char(string='Swift Code',required=True)

    product_type = fields.Many2one('product_type.model',string='Type',required=True)
    bin_no = fields.Char(string='BIN',required=True)
    country_of_origin = fields.Many2one('country_origin.model',string='Country Of Origin', required=True)
    terms_of_delivery = fields.Many2one('terms_of_delivery.model',string='Terms of Delivery',required=True) 
    time_of_delivery = fields.Char(string='Time of Delivery',required=True)

    place_of_delivery_name = fields.Many2one('supplier_factory_name_address.model',string='Delivery Factory Name', required=True)
    place_of_delivery_addr = fields.Text(string='Delivery Factory Address',required=True)

    bags_of_packing = fields.Char(string='Packing',required=True) 

    other_terms_and_condition = fields.Many2one('terms_conditions.model',string='Other Terms & Condition',required=True)
    behalf_of = fields.Char(string='On behalf of',required=True)



    #This fuction is for create a uniq number for a invoice report.
    @api.model
    def create(self, vals):
        """
        Overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """
        if not vals:
            vals = {}
        seq_obj = self.env['ir.sequence']
        invoice_num = seq_obj.next_by_code('proforma_invoice.model') or 'New'
        vals['name'] = invoice_num
        return super(ProformaInvoiceModel, self).create(vals)

    # @api.onchange('validity_date')    
    # def date_validation(self):
    #     if self.validity_date < fields.Date.today():
    #        raise exceptions.ValidationError(_("Validity date is can't less then current date.")) 



    # @api.onchange('beneficiary_full_name') 
    # def beneficiary_full_name(self):
    #     res = {}

    #     beneficiary_full_names = form.getvalue(self.beneficiary_full_name)

    #     if len(beneficiary_full_names) != 0 :
    #         res = {'value':{'behalf_of':beneficiary_full_names,}}
    #     else:
    #         res = {}
    #     return res        



    # This function is for load data automatically in the existing field from another table   
    def onchange_account_invoice_id(self, cr, uid, ids, account_invoice_id=False, context=None):
        res= {}
        if account_invoice_id:

            service_obj= self.pool.get('account.invoice').browse(cr, uid,account_invoice_id,context=context)
            service_obj2= self.pool.get('res.partner').browse(cr, uid,service_obj.partner_id.id,context=context)
            service_obj3= self.pool.get('res.country').browse(cr, uid,service_obj2.country_id.id,context=context)
            currency_symbol= self.pool.get('res.currency').browse(cr, uid,service_obj.currency_id.id,context=context)
            
            cus_full_address = str(service_obj2.street) + " , " + str(service_obj2.street2) + " , " + str(service_obj2.city)+ " - " + str(service_obj2.zip) + " , " + str(service_obj3.name)



            invoice_line_pool_ids = self.pool.get('account.invoice.line').search(cr, uid,[('invoice_id','=',account_invoice_id),],context=context)

            invoice_lines_product_name = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['name'], context=context)

            invoice_lines_product_quantity = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['quantity'], context=context)

            invoice_lines_product_price_of_unit = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_unit'], context=context)

            invoice_lines_product_amount = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_subtotal'], context=context)

            


            ordered_products_names = self.split_products_names(invoice_lines_product_name) 

            # ordered_products_number_of_bags = self.split_products_number_of_bags(invoice_lines_product_quantity)

            ordered_products_quantity = self.split_products_quantity(invoice_lines_product_quantity)

            ordered_products_price_of_unit = self.split_products_price_of_unit(invoice_lines_product_price_of_unit)

            ordered_products_amount = self.split_products_amount(invoice_lines_product_amount)

            ordered_products_total_quantity = self.products_total_quantity(invoice_lines_product_quantity)

            ordered_products_total_amount = self.products_total_amount(invoice_lines_product_amount)

            ordered_products_total_amount_in_word = self.numToWords(ordered_products_total_amount)






            res = {'value':{'account_invoice_id2':service_obj.number,'invoice_created_date':service_obj.date_invoice,
            'customer_name':service_obj2.name, 
            'customer_full_address':cus_full_address,
            'ordered_products_name':ordered_products_names,
            'ordered_products_price_of_unit':ordered_products_price_of_unit,
            'ordered_products_quantity':ordered_products_quantity,
            'ordered_products_amount':ordered_products_amount,
            'ordered_products_total_quantity': "{:,}".format( ordered_products_total_quantity ), 
            'ordered_products_total_amount': "{:,}".format( ordered_products_total_amount ),
            'ordered_products_total_amount_in_word':ordered_products_total_amount_in_word,
            'currency_symbol_name':currency_symbol.name,
            'currency_symbol_name1':currency_symbol.name,
            'currency_symbol_name2':currency_symbol.name,
            'currency_symbol':currency_symbol.symbol,
            'currency_symbol1':currency_symbol.symbol, 
            'currency_symbol2':currency_symbol.symbol
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

    def split_products_quantity(self,invoice_lines_product_quantity):
        quantity= []
        idx = 0
        for r in invoice_lines_product_quantity:
            quantity.append( "{:,}".format( int(r['quantity']) ))
            combine = '\n \n \n'.join([str(i) for i in quantity])
        return combine

    def split_products_price_of_unit(self,invoice_lines_product_price_of_unit):
        price_of_unit= []
        idx = 0
        for r in invoice_lines_product_price_of_unit:
            price_of_unit.append( "{:,}".format( r['price_unit']) )
            combine = '\n \n \n'.join([str(i) for i in price_of_unit])
        return combine

    def split_products_amount(self,invoice_lines_product_amount):
        amount= []
        idx = 0
        for r in invoice_lines_product_amount:
            amount.append( "{:,}".format( r['price_subtotal']) )
            combine = '\n \n \n'.join([str(i) for i in amount])
        return combine    
    def products_total_quantity(self,invoice_lines_product_quantity):
        total_quantity= []
        idx = 0
        for r in invoice_lines_product_quantity:
            total_quantity.append(r['quantity'])
            in_com = sum(total_quantity)
            combine = int(in_com)
        return combine   

    def products_total_amount(self,invoice_lines_product_amount):
        total_amount= []
        idx = 0
        for r in invoice_lines_product_amount:
            total_amount.append(r['price_subtotal'])
            combine = sum(total_amount)
        return combine

    def onchange_factory_name(self, cr, uid, ids, place_of_delivery_name=False, context=None):
        res= {}
        if place_of_delivery_name:
            service_obj= self.pool.get('supplier_factory_name_address.model')
            rec = service_obj.browse(cr, uid, place_of_delivery_name)
            res = {'value':{
                'place_of_delivery_addr':rec.address,
                }}
        else:
            res={}  
        return res

    # @api.onchange('beneficiary_full_name')    
    # def beneficiary_full_name(self, cr, uid, ids, beneficiary_full_name=False, context=None):
    #     res = {}

    #     if beneficiary_full_name:
    #         res = {'value':{
    #             'behalf_of':beneficiary_full_name,
    #             }}
    #     else:
    #         res={}  
        
    #     return res


    # @api.onchange('bank_name','bank_branch')        
    def onchange_bank_name_branch(self, cr, uid, ids, beneficiary_bank_name,beneficiary_bank_branch, context=None):
        bank_name_id = beneficiary_bank_name
        bank_branch_id = beneficiary_bank_branch
        if bank_name_id and bank_branch_id :
            service_obj= self.pool.get('bank_names_branch_address.model').search(cr, uid,[('name','=',bank_name_id),('branch','=',bank_branch_id),],context=context)
            bank_address_in_list = self.pool.get('bank_names_branch_address.model').read(cr, uid,service_obj,['address'], context=context)
            if len(bank_address_in_list) != 0:
                bank_address = self.split_bank_address(bank_address_in_list)
                res = {
                    'value': {
                        'beneficiary_bank_address': bank_address
                    }
                }
            else :
                res = {
                    'value': {
                        'beneficiary_bank_address': ''
                    }
                }
        else:
            res = {}
        return res

    
    def split_bank_address(self,bank_address_in_list):
        address= []
        idx = 0
        for r in bank_address_in_list:
            address.append(r['address']) 
            combine = '\n \n \n'.join([str(i) for i in address])
        return combine


    @api.multi
    def amount_to_text(self, amount_total):
        return amount_to_text(amount_total)

    def onchange_beneficiary_full_name(self, cr, uid, ids, beneficiary_full_name, context=None):
        beneficiary_full_name_id = beneficiary_full_name

        if beneficiary_full_name_id : 
            service_obj= self.pool.get('beneficiary_full_name.model').browse(cr, uid,beneficiary_full_name_id,context=context)
            name = service_obj.name
            erc_no = service_obj.erc_no

            res = {
                    'value': { 
                        'erc_no': erc_no,
                        'behalf_of': name
                    }
                }
        else :        
            res = {
                    'value': {
                        'erc_no': '',
                        'behalf_of': ''
                    }
                } 

        return res        


    
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