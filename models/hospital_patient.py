from odoo import api, models, fields
from datetime import date

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    ref = fields.Char(string='Ref')
    name = fields.Char(string='Name', required=True)
    dob = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute="_compute_age", store=True, readonly=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', required=True)
    image = fields.Image(string='Image')
    father_name = fields.Char(string='Father name')
    partner_name = fields.Char(string='Partner name')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married')
    ], string='Marital status')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    patient_disease_ids = fields.One2many('hospital.patient.disease', 'patient_id', string="Patient Diseases")
    # NEW FIELD
    prescription_ids = fields.One2many("hospital.prescription", "patient_id", string="Prescriptions")
    active = fields.Boolean(string='Active', default=True)

    @api.depends('dob')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.dob:
                record.age = today.year - record.dob.year - (
                    (today.month, today.day) < (record.dob.month, record.dob.day)
                )
            else:
                record.age = 0


class HospitalPatientDiseases(models.Model):
    _name = "hospital.patient.disease"
    _description = "Patient diseases"

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    diseases_note = fields.Char(string='Patients Diseases')
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium','Medium'),
        ('high','High')
    ])
