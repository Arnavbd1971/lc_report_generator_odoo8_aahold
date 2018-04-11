from openerp import models, fields, api

class SupplierFactoryNameAddress(models.Model):
    _name = 'supplier_factory_name_address.model' 

    name = fields.Char(compute='concatenate_custom_fields',store=True,string='name')
    factory_name = fields.Char(required=True, string='Supplier Factory Name')
    address = fields.Text(required=True, string='Supplier Factory Address')
    company_id = fields.Many2one('res.company', string='Company',required=True)
    company_name= fields.Char(string='company_name')
    date = fields.Date('Created date', required=True, default=fields.Date.today())

    
    @api.depends('company_name','factory_name')
    def concatenate_custom_fields(self):
        self.name = str(self.company_name) + ', ' + str(self.factory_name) + ' '

    def company_id_onchange(self, cr, uid, ids, company_id=False, context=None):    
        res = {}
        if company_id: 
            
            service_obj= self.pool.get('res.company')
            rec = service_obj.browse(cr, uid, company_id)
            
            res= {
                    'value':
                        { 
                            'company_name':rec.name,
                        }
            }    
        else:
            res={
                'value':
                    {
                        'company_name':' ',
                    }
            }            

        return res

    # def _get_default_company(self, cr, uid, context=None):
    #     company_id = self.pool.get('res.users')._get_company(cr, uid, context=context)
        # if not company_id:
        #     raise osv.except_osv(_('Error!'), _('There is no default company for the current user!'))
        # return company_id

