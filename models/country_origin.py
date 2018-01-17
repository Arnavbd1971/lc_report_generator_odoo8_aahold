from openerp import models, fields

class LCinformations(models.Model):
    _name = 'country_origin.model'


    name = fields.Char(required=True, string='Country Of Origin Name',size=64)
    date = fields.Date('Created date', required=True, default=fields.Date.today())
