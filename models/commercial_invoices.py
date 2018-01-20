from openerp import models, fields, api,_
# from openerp.exceptions import ValidationError

# commercial invoice Model start

class CommercialInvoiceModel(models.Model):
    _name = 'commercial_invoice.model'

    _rec_name = "name"

    name = fields.Char(string='Commercial Invoice Number',  readonly=True)
    commercial_invoice_created_date = fields.Date(string='Date', readonly=True, default=fields.Date.today(), required=True)

    # account_invoice_id = fields.Many2one('account.invoice',string='Customer Invoice No.', required=True)
    # account_invoice_id2 = fields.Char(string='account_invoice_id')


    customer_invoice_id = fields.Many2one('account.invoice',string='Customer Invoice No.',  required=True)

    # customer_invoice_id = fields.Integer(string='Customer Invoice Id',  required=True)
    customer_name = fields.Char(string='Customer Name',  required=True)
    customer_name2 = fields.Char(string='Customer Name',  required=True)
    customer_full_address = fields.Text(string='Customer Address',  required=True)

    proforma_invoice_id = fields.Char(string='Proforma Invoice No.',  required=True)
    proforma_invoice_created_date = fields.Date(string='Proforma Invoice Date',  required=True)

    transport = fields.Many2one('delivery_transport.model',string='Means of Transport',  required=True)
    supplier_factory_name = fields.Char(string='Delivery From Factory Name',  required=True)
    supplier_factory_address = fields.Text(string='Delivery From Factory Address',  required=True)
    beneficiary_vat_no = fields.Char(string='Beneficiary VAT No:',  required=True)
    erc_no = fields.Char(string='ERC No',  required=True)

    country_of_origin = fields.Char(string='Country Of Origin',  required=True)
    country_of_origin2 = fields.Char(string='Country Of Origin',  required=True)

    destination_address = fields.Text(string='Destination',  required=True)

    client_shipping_factory_name = fields.Many2one('customer_factory_name_address.model',string='Factory Name',  required=True)
    client_shipping_factory_address = fields.Text(string='Factory Address',  required=True)

    lc_num = fields.Many2one('lc_informations.model','L/C No.',  required=True)
    lc_num2 = fields.Char(string='L/C No.',  required=True)
    lc_date = fields.Date(string='L/C Dated',  required=True)
    lc_date2 = fields.Date(string='L/C Dated',  required=True)
    issuing_bank = fields.Text(string='Issuing Bank',  required=True)
    vat_code = fields.Char(string='VAT No.' ,  required=True)
    irc_num = fields.Char(string='IRC No.' ,  required=True)
    bin_num = fields.Char(string='BIN No.' ,  required=True) 
    tin_num = fields.Char(string='TIN No.' ,  required=True)
    amend_no = fields.Char(string='Amend No' )
    amend_date = fields.Char(string='Amend Date' )

    ordered_products_name = fields.Text(string='ordered_products_name') 
    ordered_products_number_of_bags = fields.Text(string='ordered_products_number_of_bags') 
    ordered_products_quantity = fields.Text(string='ordered_products_quantity') 
    ordered_products_price_of_unit = fields.Text(string='ordered_products_price_of_unit')
    ordered_products_amount = fields.Text(string='ordered_products_amount')

    ordered_products_total_quantity = fields.Char(string='ordered_products_total_quantity')
    ordered_products_total_amount = fields.Char(string='Total')
    ordered_products_total_amount_in_word = fields.Char(string='ordered_products_total_amount_in_word')

    currency_symbol_name = fields.Char(string='currency_symbol_name')
    currency_symbol_name1 = fields.Char(string='currency_symbol_name')
    currency_symbol_name2 = fields.Char(string='currency_symbol_name')
    currency_symbol = fields.Char(string='currency_symbol')
    currency_symbol1 = fields.Char(string='currency_symbol')
    currency_symbol2 = fields.Char(string='currency_symbol')

    contact_no = fields.Text(string='contact no',  required=True)

    only_seq_num = fields.Char(string='only_seq_num', size=255)
    num_of_bags = fields.Char(string='num_of_bags', size=255)

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
        seq_obj2 = self.env['ir.sequence']
        invoice_num = seq_obj.next_by_code('commercial_invoice_report_num') or 'New'
        only_num = seq_obj2.next_by_code('only_num') or 'New_seqq'
        vals['name'] = invoice_num
        vals['only_seq_num'] = only_num
        return super(CommercialInvoiceModel, self).create(vals)

    

  

    # This function is for load data automatically in the existing field from another table
    def onchange_lc_num_service(self, cr, uid, ids, lc_num=False, context=None):
        res= {}
        if lc_num:
            service_obj= self.pool.get('lc_informations.model')
            rec = service_obj.browse(cr, uid, lc_num)

            bank_name_id = rec.bank_name
            bank_branch_id = rec.bank_branch
            bank_address = rec.bank_address
            vat_no = rec.vat_no
            irc_no = rec.irc_no
            bin_no = rec.bin_no
            tin_no = rec.tin_no

            amend_no = rec.amend_no
            amend_date = rec.amend_date

            all_data_obj_of_bank_names = self.pool.get('bank_names.model').browse(cr, uid,bank_name_id.id,context=context)

            bank_name = all_data_obj_of_bank_names.name

            all_data_obj_of_bank_branch = self.pool.get('bank_branch.model').browse(cr, uid,bank_branch_id.id,context=context)

            bank_branch = all_data_obj_of_bank_branch.name

            bank_info = str(bank_name) + "\n" + str(bank_branch) + "\n" + str(bank_address)

            res= {
                    'value':
                        { 
                            'lc_date':rec.created_date,
                            'issuing_bank':bank_info,
                            'lc_num2':rec.name,
                            'lc_date2':rec.created_date,
                            'vat_code':rec.vat_no,
                            'irc_num':rec.irc_no,
                            'bin_num':rec.irc_no, 
                            'tin_num':rec.irc_no,
                            'amend_no':rec.amend_no,
                            'amend_date':rec.amend_date,
                        }
                }
        else:
            res= {'value':{'lc_date':False,'issuing_bank':False}}
        return res



    # This function is for load data automatically in the existing field from another table
    def onchange_customer_invoice_id(self, cr, uid, ids, customer_invoice_id=False, context=None):
        res= {}
        if customer_invoice_id:

            service_obj= self.pool.get('account.invoice').browse(cr, uid,customer_invoice_id,context=context)
            service_obj2= self.pool.get('res.partner').browse(cr, uid,service_obj.partner_id.id,context=context)
            service_obj3= self.pool.get('res.country').browse(cr, uid,service_obj2.country_id.id,context=context)
            currency_symbol= self.pool.get('res.currency').browse(cr, uid,service_obj.currency_id.id,context=context)

            cus_name = service_obj2.name
            cus_full_address = str(service_obj2.street) + ", " + str(service_obj2.street2) + ", " + str(service_obj2.city)+ " - " + str(service_obj2.zip) + ", " + str(service_obj3.name)


            delivery_order_num = service_obj.origin
            stock_picking_id = self.pool.get('stock.picking').search(cr, uid,[('name','=',delivery_order_num),],context=context)
            stock_picking_data_list = self.pool.get('stock.picking').read(cr, uid,stock_picking_id,['origin'], context=context)
            pi_no = self.split_from_list(stock_picking_data_list,'origin')
            sale_order_id = self.pool.get('sale.order').search(cr, uid,[('name','=',pi_no),],context=context)
            sale_order_data_list = self.pool.get('sale.order').read(cr, uid,sale_order_id,['id', 'create_date','place_of_delivery_name2','place_of_delivery_addr', 'erc_no','country_of_origin2','bags_of_packing'], context=context)
            pi_create_date = self.split_from_list(sale_order_data_list,'create_date')
            supplier_factory_name = self.split_from_list(sale_order_data_list,'place_of_delivery_name2')
            supplier_factory_address = self.split_from_list(sale_order_data_list,'place_of_delivery_addr')
            erc_no = self.split_from_list(sale_order_data_list,'erc_no')
            country_of_origin = self.split_from_list(sale_order_data_list,'country_of_origin2')
            num_of_bags = self.split_from_list(sale_order_data_list,'bags_of_packing')
         

            invoice_line_pool_ids = self.pool.get('account.invoice.line').search(cr, uid,[('origin','=',delivery_order_num),],context=context)

            invoice_lines_product_name = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['name'], context=context)

            invoice_lines_product_quantity = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['quantity'], context=context)

            invoice_lines_product_price_of_unit = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_unit'], context=context)

            invoice_lines_product_amount = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_subtotal'], context=context)


            ordered_products_names = self.split_products_names(invoice_lines_product_name) 

            ordered_products_number_of_bags = self.split_products_number_of_bags(invoice_lines_product_quantity,num_of_bags)

            ordered_products_quantity = self.split_products_quantity(invoice_lines_product_quantity)

            ordered_products_price_of_unit = self.split_products_price_of_unit(invoice_lines_product_price_of_unit)

            ordered_products_amount = self.split_products_amount(invoice_lines_product_amount)

            ordered_products_total_quantity = self.products_total_quantity(invoice_lines_product_quantity)

            ordered_products_total_amount = self.products_total_amount(invoice_lines_product_amount)

            ordered_products_total_amount_in_word = self.numToWords(ordered_products_total_amount)

            


            res = {'value':{
                'customer_name':cus_name,
                'customer_name2':service_obj2.name,
                'customer_full_address':cus_full_address,
                'proforma_invoice_id':pi_no,
                'proforma_invoice_created_date':pi_create_date,
                'supplier_factory_name':supplier_factory_name,
                'supplier_factory_address':supplier_factory_address,
                'erc_no':erc_no,
                'country_of_origin':country_of_origin,
                'country_of_origin2':country_of_origin,
                'num_of_bags': num_of_bags,

                'ordered_products_name':ordered_products_names,
                'ordered_products_number_of_bags':ordered_products_number_of_bags,
                'ordered_products_quantity':ordered_products_quantity,'ordered_products_price_of_unit':ordered_products_price_of_unit,
                'ordered_products_amount': ordered_products_amount,
                'ordered_products_total_quantity': "{:,}".format(ordered_products_total_quantity),
                'ordered_products_total_amount': "{:,}".format(ordered_products_total_amount),
                'ordered_products_total_amount_in_word':ordered_products_total_amount_in_word,
                'currency_symbol_name':currency_symbol.name,
                'currency_symbol_name1':currency_symbol.name,
                'currency_symbol_name2':currency_symbol.name,
                'currency_symbol':currency_symbol.symbol,
                'currency_symbol1':currency_symbol.symbol,
                'currency_symbol2':currency_symbol.symbol, 
                
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
            number_of_bags.append(int(r['quantity'] / bags))
            combine = '\n \n'.join([str(i) for i in number_of_bags])
        return combine

    def split_products_quantity(self,invoice_lines_product_quantity):
        quantity= []
        idx = 0
        for r in invoice_lines_product_quantity:
            quantity.append( "{:,}".format( int(r['quantity']) ) )
            combine = '\n \n'.join([str(i) for i in quantity])
        return combine

    def split_products_price_of_unit(self,invoice_lines_product_price_of_unit):
        price_of_unit= []
        idx = 0
        for r in invoice_lines_product_price_of_unit:
            price_of_unit.append("{:,}".format(r['price_unit']))
            combine = '\n \n'.join([str(i) for i in price_of_unit])
        return combine

    def split_products_amount(self,invoice_lines_product_amount):
        amount= []
        idx = 0
        for r in invoice_lines_product_amount:
            amount.append("{:,}".format( r['price_subtotal']) )
            combine = '\n \n'.join([str(i) for i in amount])
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



      
    # def onchange_country_origin(self, cr, uid, ids, country_of_origin=False, context=None):
    #     res= {}
    #     if country_of_origin:
    #         service_obj= self.pool.get('country_origin.model')
    #         rec = service_obj.browse(cr, uid, country_of_origin)
    #         res = {'value':{'country_of_origin2':rec.name}}
    #     else:
    #         res={}  
    #     return res

    def onchange_client_shipping_factory_name(self, cr, uid, ids, client_shipping_factory_name=False, context=None):
        res= {}
        if client_shipping_factory_name:
            service_obj= self.pool.get('customer_factory_name_address.model')
            rec = service_obj.browse(cr, uid, client_shipping_factory_name)
            res = {'value':{
                'client_shipping_factory_address':rec.address,
                'destination_address':rec.address
                }}
        else:
            res={}  
        return res


    def onchange_supplier_factory_name(self, cr, uid, ids, supplier_factory_name=False, context=None):
        res= {}
        if supplier_factory_name:
            service_obj= self.pool.get('supplier_factory_name_address.model')
            rec = service_obj.browse(cr, uid, supplier_factory_name)
            res = {'value':{
                'supplier_factory_address':rec.address
                }}
        else:
            res={}  
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









