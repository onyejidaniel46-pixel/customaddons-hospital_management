from odoo import models, fields

class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Name', required=True)
    specialty = fields.Char(string='Specialty')
    patient_ids = fields.One2many('hospital.patient', 'doctor_id', string='Patients')
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string='Appointments')
    email = fields.Char(string='Email') 
