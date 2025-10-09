from odoo import models, fields

class WebForm(models.Model):
    _name = 'web.form'
    _description = 'Web Form'
    _rec_name ="name"

    name = fields.Char(string='Form Name', required=True, store=True)
    age = fields.Integer(string='Age', store=True)
    description = fields.Text(string='Description', store=True)
    test_field = fields.Char(string="Test Field", store=True)
    new_field = fields.Char(string="New Field", store=True)
    
    test_new_field = fields.Char(string="Test New Field", store=True)
