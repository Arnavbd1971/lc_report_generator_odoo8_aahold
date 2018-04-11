# -*- coding: utf-8 -*-
{
    'name' : 'LC Report Generator',

    'summary': "LC report management",

    'description': 'Simplly creat your LC report',

    'author': "Metaporphosis.com.bd",
    'website': "http://www.metamorphosis.com.bd/",

    'version': '0.1',

    'depends': [
        'base',
        'account',
    ],

    'data': [ 
        'views/customer_invoices_records.xml',
        'views/commercial_invoices.xml',
        'views/lc_informations.xml',
        'views/invoice_name_sequence.xml',
        'views/country_origin.xml', 
        'views/delivery_transport.xml',
        # 'views/delivery_address.xml', 
        # 'views/shipping_factory_name_address.xml', 
        # 'views/proforma_invoice.xml', 
        'views/packing_list.xml', 
        'views/truck_challan.xml', 
        'views/delivery_challan.xml',  
        'views/beneficiary_certificate.xml', 
        'views/certificate_of_origin.xml', 
        'views/forwarding_letter.xml',  
        'views/bill_of_exchange.xml', 
        'views/terms_conditions.xml',   
        'views/supplier_factory_name_addr.xml', 
        # 'views/customer_factory_name_addr.xml',  
        # 'views/bank_names.xml',
        # 'views/bank_branch.xml', 
        'views/bank_names_branch_address.xml', 
        # 'views/beneficiary_full_name.xml', 
        'views/reimbursement.xml',  
        'views/method_of_payment.xml', 
        'views/product_type.xml', 
        'views/terms_of_delivery.xml',
        # 'views/commodity.xml',
        # 'views/beneficiary_bank_branch.xml',
        'views/summery_reports/proforma_invoice_status.xml',
        'views/signature_upload.xml',
        
    ],
    'auto_install':False,
    'installable': True,
}    