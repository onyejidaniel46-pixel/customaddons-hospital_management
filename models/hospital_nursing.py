from odoo import models, fields

class HospitalNursing(models.Model):
    _name = 'hospital.nursing'
    _description = 'Hospital Nursing'

    name = fields.Char(string='Name', required=True)
    department = fields.Char(string='Department')
    shift = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night')
    ], string='Shift')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    active = fields.Boolean(string='Active', default=True)