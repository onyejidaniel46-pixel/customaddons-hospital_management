from odoo import models, fields

class Billing(models.Model):
    _name = 'hospital.billing'
    _description = 'Hospital Billing'

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    amount = fields.Float(string="Amount", required=True)
    date = fields.Datetime(string="Billing Date", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft')
