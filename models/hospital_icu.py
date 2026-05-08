from odoo import models, fields, api


class HospitalICU(models.Model):
    _name = 'hospital.icu'
    _description = 'Patient ICU Info'

    inpatient_id = fields.Many2one('hospital.inpatient', string='Hospitalization', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', related='inpatient_id.patient_id', store=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    physician_id = fields.Many2one('hospital.doctor', string='Physician')

    # APACHE II Score fields
    age_score = fields.Integer(string='Age Score')
    temperature = fields.Float(string='Temperature (°C)')
    mean_arterial_pressure = fields.Float(string='Mean Arterial Pressure')
    heart_rate = fields.Integer(string='Heart Rate')
    respiratory_rate = fields.Integer(string='Respiratory Rate')
    fio2 = fields.Float(string='FiO2')
    ph = fields.Float(string='Arterial pH')
    sodium = fields.Float(string='Serum Sodium')
    potassium = fields.Float(string='Serum Potassium')
    creatinine = fields.Float(string='Serum Creatinine')
    hematocrit = fields.Float(string='Hematocrit')
    wbc = fields.Float(string='White Blood Cell Count')
    glasgow_coma_score = fields.Integer(string='Glasgow Coma Score')
    apache_score = fields.Integer(string='APACHE II Score', compute='_compute_apache_score', store=True)
    notes = fields.Text(string='Notes')

    @api.depends('age_score', 'glasgow_coma_score')
    def _compute_apache_score(self):
        for rec in self:
            rec.apache_score = rec.age_score + (15 - rec.glasgow_coma_score)


class HospitalECG(models.Model):
    _name = 'hospital.ecg'
    _description = 'ECG Test'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    inpatient_id = fields.Many2one('hospital.inpatient', string='Hospitalization')
    physician_id = fields.Many2one('hospital.doctor', string='Physician')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    heart_rate = fields.Integer(string='Heart Rate (bpm)')
    rhythm = fields.Selection([
        ('normal', 'Normal Sinus Rhythm'),
        ('tachycardia', 'Tachycardia'),
        ('bradycardia', 'Bradycardia'),
        ('afib', 'Atrial Fibrillation'),
        ('other', 'Other'),
    ], string='Rhythm')
    interpretation = fields.Text(string='Interpretation')
    notes = fields.Text(string='Notes')


class HospitalGCS(models.Model):
    _name = 'hospital.gcs'
    _description = 'Glasgow Coma Scale'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    inpatient_id = fields.Many2one('hospital.inpatient', string='Hospitalization')
    physician_id = fields.Many2one('hospital.doctor', string='Physician')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    eye_opening = fields.Selection([
        ('4', 'Spontaneous (4)'),
        ('3', 'To Voice (3)'),
        ('2', 'To Pain (2)'),
        ('1', 'None (1)'),
    ], string='Eye Opening')
    verbal_response = fields.Selection([
        ('5', 'Oriented (5)'),
        ('4', 'Confused (4)'),
        ('3', 'Inappropriate Words (3)'),
        ('2', 'Sounds (2)'),
        ('1', 'None (1)'),
    ], string='Verbal Response')
    motor_response = fields.Selection([
        ('6', 'Obeys Commands (6)'),
        ('5', 'Localizes Pain (5)'),
        ('4', 'Withdraws (4)'),
        ('3', 'Flexion (3)'),
        ('2', 'Extension (2)'),
        ('1', 'None (1)'),
    ], string='Motor Response')
    gcs_total = fields.Integer(string='GCS Total', compute='_compute_gcs', store=True)
    notes = fields.Text(string='Notes')

    @api.depends('eye_opening', 'verbal_response', 'motor_response')
    def _compute_gcs(self):
        for rec in self:
            eye = int(rec.eye_opening or 0)
            verbal = int(rec.verbal_response or 0)
            motor = int(rec.motor_response or 0)
            rec.gcs_total = eye + verbal + motor