from odoo import models, fields

class HospitalPatientEvaluation(models.Model):
    _name = 'hospital.patient.evaluation'
    _description = 'Patient Evaluation'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    physician_id = fields.Many2one('hospital.doctor', string='Physician')
    date = fields.Date(string='Date', default=lambda self: fields.Date.today())
    pulse_rate = fields.Char(string='Pulse Rate')
    oxygen_rate = fields.Char(string='Oxygen Rate')
    blood_pressure = fields.Char(string='Blood Pressure')
    weight = fields.Float(string='Weight')
    temperature = fields.Float(string='Temperature')
    chief_complaint = fields.Text(string='Chief Complaint')
    diagnosis = fields.Text(string='Diagnosis')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)