from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class TermsConditions(models.Model):
    _name = 'terms_conditions.model'


    name = fields.Text(required=True, string='Other Terms and Conditions',size=100)
    date = fields.Date('Created Date', required=True, default=fields.Date.today())


    @api.one 
    @api.constrains('date')
    def _check_lc_date(self):
        if self.date > fields.Date.today():
            raise ValidationError(_("Date can't be greater than current date!"))