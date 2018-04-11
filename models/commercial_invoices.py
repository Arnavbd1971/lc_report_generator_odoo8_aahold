from openerp import models, fields, api,_
from openerp.exceptions import except_orm, Warning, RedirectWarning

class CommercialInvoiceModel(models.Model):
    _name = 'commercial_invoice.model'
    _rec_name = "name"
    name = fields.Char(string='Commercial Invoice Number',readonly=True)
    commercial_invoice_created_date = fields.Date(string='Created Date',default=fields.Date.today())
    customer_invoice_id = fields.Many2one('account.invoice',string='Customer Invoice No.')
    pi_id = fields.Many2one('sale.order',string='Proforma Invoice No.', required=True)
    customer_name = fields.Char(string='Customer Name')
    customer_name2 = fields.Char(string='Customer Name')
    customer_full_address = fields.Text(string='Customer Address')
    proforma_invoice_id = fields.Char(string='Proforma Invoice No.')
    proforma_invoice_created_date = fields.Date(string='Proforma Invoice Date')
    transport = fields.Many2one('delivery_transport.model',string='Means of Transport', required=True)
    supplier_factory_name = fields.Char(string='Delivery From Factory Name')
    supplier_factory_address = fields.Text(string='Delivery From Factory Address')
    beneficiary_vat_no = fields.Char(string='Beneficiary VAT No:', required=True)
    erc_no = fields.Char(string='ERC No')
    country_of_origin = fields.Char(string='Country Of Origin')
    country_of_origin2 = fields.Char(string='Country Of Origin')
    destination_address = fields.Text(string='Destination')
    client_shipping_factory_address = fields.Text(string='Factory Address') 
    lc_id = fields.Char('L/C id')
    lc_num = fields.Char('L/C No.')
    lc_num2 = fields.Char(string='L/C No.')
    lc_date = fields.Date(string='L/C Dated')
    lc_date2 = fields.Date(string='L/C Dated')
    issuing_bank = fields.Text(string='Issuing Bank')
    vat_code = fields.Char(string='VAT No.' )
    irc_num = fields.Char(string='IRC No.' )
    bin_num = fields.Char(string='BIN No.' ) 
    tin_num = fields.Char(string='TIN No.' )
    amend_no = fields.Char(string='Amend No' )
    amend_date = fields.Date(string='Amend Date' )
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
    contact_no = fields.Text(string='contact no',default='Export Sales Contract No. MCFN-MK010-018 dated 07-APR-18')
    only_seq_num = fields.Char(string='only_seq_num', size=255)
    num_of_bags = fields.Char(string='num_of_bags', size=255)
    delivery_order_num = fields.Char(string='Delivery Order Number')  
    delivery_challan_num = fields.Char(string='Delivery Challan Number')
    delivery_order_created_date = fields.Date(string='Delivery Order Created date')

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

    def onchange_pi_id(self, cr, uid, ids, pi_id=False, context=None):
        res= {}
        if pi_id:
            service_obj= self.pool.get('sale.order').browse(cr, uid,pi_id,context=context)  
            service_obj2= self.pool.get('res.partner').browse(cr, uid,service_obj.partner_id.id,context=context)
            service_obj3= self.pool.get('res.country').browse(cr, uid,service_obj2.country_id.id,context=context)
            currency_symbol= self.pool.get('res.currency').browse(cr, uid,service_obj.currency_id.id,context=context)
            cus_name = service_obj2.name
            cus_full_address = str(service_obj2.street) + ", " + str(service_obj2.street2) + ", " + str(service_obj2.city)+ " - " + str(service_obj2.zip) + ", " + str(service_obj3.name)
            lc_id = service_obj.lc_num_id
            lc_service_obj= self.pool.get('lc_informations.model')
            rec = lc_service_obj.browse(cr, uid, lc_id.id)
            lc_bank_name = rec.bank_name2
            lc_bank_branch = rec.bank_branch
            lc_bank_address = rec.bank_address
            vat_no = rec.vat_no
            irc_no = rec.irc_no
            bin_no = rec.bin_no
            tin_no = rec.tin_no
            amend_no = rec.amend_no
            amend_date = rec.amend_date
            bank_info = str(lc_bank_name) + "\n" + str(lc_bank_branch) + "\n" + str(lc_bank_address)
            account_invoice_ids = self.pool.get('account.invoice').search(cr, uid,[('pi_no','=',service_obj.name),('process','=','set_for_LC')],context=context)
            if not account_invoice_ids:
                # print('Account invoice list is empty.')
                raise except_orm(_('Validation!'),
                    _("No document ready for set L/C document under PI No. %s !")% (service_obj.name,))
            else:
                invoice_line_pool_ids = self.pool.get('account.invoice.line').search(cr, uid,[('invoice_id','=',account_invoice_ids),],context=context)  
                invoice_lines_product_name = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['name'], context=context)
                invoice_lines_product_quantity = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['quantity','name'], context=context)
                invoice_lines_product_price_of_unit = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_unit','name'], context=context)
                invoice_lines_product_amount = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_subtotal','name'], context=context)
                num_of_bags = service_obj.bags_of_packing
                ordered_products_names = self.split_products_names(invoice_lines_product_name) 
                ordered_products_number_of_bags = self.split_products_number_of_bags(invoice_lines_product_quantity,num_of_bags)
                ordered_products_quantity = self.split_products_quantity(invoice_lines_product_quantity)
                ordered_products_price_of_unit = self.split_products_price_of_unit(invoice_lines_product_price_of_unit)
                ordered_products_amount = self.split_products_amount(invoice_lines_product_amount)
                ordered_products_total_quantity = self.products_total_quantity(invoice_lines_product_quantity)
                ordered_products_total_amount = self.products_total_amount(invoice_lines_product_amount)
                ordered_products_total_amount_in_word = self.numToWords(ordered_products_total_amount)

                do_no_read = self.pool.get('account.invoice').read(cr, uid,account_invoice_ids,['do_no'], context=context)
                do_no = self.split_do_no(do_no_read)
                stock_picking_ser_ids= self.pool.get('stock.picking').search(cr, uid,[('origin','=',service_obj.name),],context=context)
                order_date_read = self.pool.get('stock.picking').read(cr, uid,stock_picking_ser_ids,['date'], context=context)
                delivery_order_date = self.split_order_date_read(order_date_read)

            res = {'value':{
                'customer_name':cus_name,
                'customer_name2':service_obj2.name, 
                'customer_full_address':cus_full_address,
                'proforma_invoice_id':service_obj.name,
                'proforma_invoice_created_date':service_obj.create_date,
                'supplier_factory_name':service_obj.place_of_delivery_name2, 
                'supplier_factory_address':service_obj.place_of_delivery_addr, 
                'client_shipping_factory_address':service_obj.cus_factory_addr,
                'destination_address': service_obj.cus_factory_addr,
                'erc_no':service_obj.erc_no,
                'country_of_origin':service_obj.country_of_origin2,
                'country_of_origin2':service_obj.country_of_origin2,
                'num_of_bags': service_obj.bags_of_packing, 
                'lc_id':lc_id.id,
                'lc_num':rec.name,
                'lc_num2':rec.name,
                'lc_date':rec.created_date,
                'issuing_bank':bank_info,
                'lc_date2':rec.created_date,
                'vat_code':rec.vat_no,
                'irc_num':rec.irc_no,
                'bin_num':rec.bin_no, 
                'tin_num':rec.tin_no,
                'amend_no':rec.amend_no,
                'amend_date':rec.amend_date,
                'ordered_products_name':ordered_products_names,
                'ordered_products_number_of_bags':ordered_products_number_of_bags,
                'ordered_products_quantity':ordered_products_quantity,
                'ordered_products_price_of_unit':ordered_products_price_of_unit,
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
                'delivery_order_num':do_no, 
                'delivery_order_created_date':delivery_order_date, 
            }}
        else:
            res={}  
        return res    

    def split_order_date_read(self,order_date_read):
        seen = set()
        date= []
        answer = []
        for r in order_date_read: 
            date.append(r['date'])
            combine_date = '\n'.join([str(i) for i in date])
            for line in combine_date.splitlines():
                if line not in seen:
                    seen.add(line)
                    answer.append(line)
                    combine = '\n'.join(answer)
        return combine

    def split_do_no(self,do_no_read):
        seen = set()
        do= []
        answer = []
        for r in do_no_read: 
            do.append(r['do_no'])
            combine_do = '\n'.join([str(i) for i in do])
            for line in combine_do.splitlines():
                if line not in seen:
                    seen.add(line)
                    answer.append(line)
                    combine = '\n'.join(answer)
        return combine    

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

    def split_products_price_of_unit(self,invoice_lines_product_price_of_unit):
        price_of_unit= []
        testListDict = {}
        for item in invoice_lines_product_price_of_unit:
            try:
                d=item['name']
                testListDict[d] = item['price_unit'] 
            except:
                d=item['name']
                testListDict[d] = item['price_unit']

        for the_key, the_value in testListDict.iteritems():
            price_of_unit.append(the_value)
            combine = '\n \n'.join([str(i) for i in price_of_unit])
        return combine

    def split_products_amount(self,invoice_lines_product_amount):
        amount= []
        testListDict = {}
        for item in invoice_lines_product_amount:
            try:
                d=item['name']
                testListDict[d] += int(item['price_subtotal']) 
            except:
                d=item['name']
                testListDict[d] = int(item['price_subtotal'])

        for the_key, the_value in testListDict.iteritems():
            amount.append(the_value)
            combine = '\n \n'.join([str(i) for i in amount])
        return combine    

    def products_total_quantity(self,invoice_lines_product_quantity):
        total_quantity= []
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

    # def split_products_names(self,invoice_lines_product_name):
    #     names= []
    #     idx = 0
    #     for r in invoice_lines_product_name:
    #         names.append(r['name'])
    #         combine = '\n'.join([str(i) for i in names])  
    #     return combine    

    # def split_from_list(self,list_name,data_field):
    #     save = []
    #     for r in list_name:
    #         save.append(r[data_field])
    #         combine = '\n'.join([str(i) for i in save])
    #     return combine    








