from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class Method_Of_Payment(models.Model):
    _name = 'method_of_payment.model'


    name = fields.Text(required=True, string='Method Of Payment')
    created_date = fields.Date('Created Dated', required=True, default=fields.Date.today())

