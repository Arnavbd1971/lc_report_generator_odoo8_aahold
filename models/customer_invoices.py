from openerp import models, fields, api


# Customer Invoice Model start

class CustomerInvoiceModel(models.Model):

    _inherit = 'account.invoice'
    # _name = 'custom_test1.model'

    testField = fields.Char(string='testField')

# Customer Invoice Model end