from odoo import models, fields

class HospitalPrescription(models.Model):
    _name = 'hospital.prescription'
    _description = 'Hospital Prescription'
    _order = 'date desc'
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    date = fields.Datetime(string="Prescription Date", required=True)
    medication = fields.Char(string="Medication", required=True)
    dosage = fields.Char(string="Dosage")
    instructions = fields.Text(string="Instructions")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('dispensed', 'Dispensed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft')

    
