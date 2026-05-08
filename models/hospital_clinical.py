from odoo import models, fields, api


class HospitalMedication(models.Model):
    _name = 'hospital.medication'
    _description = 'Medication / Medicament'

    name = fields.Char(string='Medicine Name', required=True)
    category = fields.Char(string='Therapeutic Category')
    therapeutic_effect = fields.Text(string='Therapeutic Effect')
    active_components = fields.Text(string='Active Components')
    presentation = fields.Char(string='Presentation')
    composition = fields.Text(string='Composition')
    dosage = fields.Char(string='Dosage')
    expiry_date = fields.Date(string='Expiry Date')
    safe_for_pregnant = fields.Boolean(string='Safe for Pregnant Women', default=True)
    adverse_reaction = fields.Text(string='Adverse Reactions')
    storage_conditions = fields.Text(string='Storage Conditions')
    notes = fields.Text(string='Extra Information')


class HospitalVaccination(models.Model):
    _name = 'hospital.vaccination'
    _description = 'Patient Vaccination'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    vaccine = fields.Char(string='Vaccine', required=True)
    physician_id = fields.Many2one('hospital.doctor', string='Physician')
    date = fields.Date(string='Vaccination Date', default=fields.Date.today)
    next_dose_date = fields.Date(string='Next Dose Date')
    lot_number = fields.Char(string='Lot Number')
    notes = fields.Text(string='Notes')


class HospitalImaging(models.Model):
    _name = 'hospital.imaging'
    _description = 'Medical Imaging'

    name = fields.Char(string='Reference', readonly=True, default='New')
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    physician_id = fields.Many2one('hospital.doctor', string='Requesting Physician')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    imaging_type = fields.Selection([
        ('xray', 'X-Ray'),
        ('mri', 'MRI'),
        ('ct', 'CT Scan'),
        ('ultrasound', 'Ultrasound'),
        ('echo', 'Echocardiogram'),
        ('other', 'Other'),
    ], string='Imaging Type', required=True)
    body_part = fields.Char(string='Body Part / Region')
    result = fields.Text(string='Result / Findings')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string='Status', default='draft')
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.imaging') or 'New'
        return super().create(vals)


class HospitalSurgery(models.Model):
    _name = 'hospital.surgery'
    _description = 'Surgery'

    name = fields.Char(string='Surgery Reference', readonly=True, default='New')
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    surgeon_id = fields.Many2one('hospital.doctor', string='Surgeon', required=True)
    assistant_ids = fields.Many2many('hospital.doctor', string='Assistants')
    date = fields.Datetime(string='Surgery Date', required=True)
    surgery_type = fields.Char(string='Surgery Type')
    description = fields.Text(string='Description')
    result = fields.Text(string='Result / Notes')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='scheduled')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.surgery') or 'New'
        return super().create(vals)


class HospitalAmbulance(models.Model):
    _name = 'hospital.ambulance'
    _description = 'Ambulance Request'

    name = fields.Char(string='Reference', readonly=True, default='New')
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    driver = fields.Char(string='Driver Name')
    vehicle_number = fields.Char(string='Vehicle Number')
    pickup_location = fields.Char(string='Pickup Location')
    destination = fields.Char(string='Destination')
    request_date = fields.Datetime(string='Request Date', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('dispatched', 'Dispatched'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.ambulance') or 'New'
        return super().create(vals)


class HospitalBloodDonation(models.Model):
    _name = 'hospital.blood.donation'
    _description = 'Blood Donation'

    name = fields.Char(string='Reference', readonly=True, default='New')
    donor_name = fields.Char(string='Donor Name', required=True)
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ], string='Blood Type', required=True)
    donation_date = fields.Date(string='Donation Date', default=fields.Date.today)
    units = fields.Float(string='Units (ml)')
    physician_id = fields.Many2one('hospital.doctor', string='Physician')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft')
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.blood.donation') or 'New'
        return super().create(vals)


class HospitalInsurance(models.Model):
    _name = 'hospital.insurance'
    _description = 'Patient Insurance'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    insurer = fields.Char(string='Insurance Company', required=True)
    policy_number = fields.Char(string='Policy Number')
    expiry_date = fields.Date(string='Expiry Date')
    coverage = fields.Text(string='Coverage Details')
    notes = fields.Text(string='Notes')


class HospitalDisease(models.Model):
    _name = 'hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Disease Name', required=True)
    category = fields.Char(string='Disease Category')
    code = fields.Char(string='ICD Code')
    description = fields.Text(string='Description')


class HospitalPatientDisease(models.Model):
    _name = 'hospital.patient.disease'
    _description = 'Patient Disease History'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    disease_id = fields.Many2one('hospital.disease', string='Disease', required=True)
    physician_id = fields.Many2one('hospital.doctor', string='Physician')
    diagnosed_date = fields.Date(string='Diagnosed Date', default=fields.Date.today)
    healed_date = fields.Date(string='Healed Date')
    is_active = fields.Boolean(string='Currently Active', default=True)
    notes = fields.Text(string='Notes')
    diseases_note = fields.Text(string='Disease Notes')
    severity = fields.Selection([          # ← add this
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('critical', 'Critical'),
    ], string='Severity')


class HospitalPatientEvaluation(models.Model):
    _name = 'hospital.patient.evaluation'
    _description = 'Patient Evaluation'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    physician_id = fields.Many2one('hospital.doctor', string='Physician')
    date = fields.Datetime(string='Evaluation Date', default=fields.Datetime.now)
    chief_complaint = fields.Text(string='Chief Complaint')
    pulse_rate = fields.Integer(string='Pulse Rate (bpm)')
    oxygen_rate = fields.Float(string='Oxygen Saturation (%)')
    blood_pressure = fields.Char(string='Blood Pressure (mmHg)')
    weight = fields.Float(string='Weight (kg)')
    temperature = fields.Float(string='Temperature (°C)')
    diagnosis = fields.Text(string='Diagnosis')
    notes = fields.Text(string='Notes')