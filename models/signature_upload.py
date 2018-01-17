from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class Signature(models.Model):
    _name = 'signature_upload.model'


    name = fields.Char(required=True, string='Name')
    
    my_binary_field_name = fields.Binary(
       'Signarute',help="Select signature image here"
    )
    
    created_date = fields.Date('Created Dated', required=True, default=fields.Date.today())
