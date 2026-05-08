from odoo import models, fields, api


class HospitalInpatient(models.Model):
    _name = 'hospital.inpatient'
    _description = 'Patient Hospitalization'

    name = fields.Char(string='Registration Number', readonly=True, default='New')
    registration_code = fields.Char(string='Registration Code', readonly=True, default='New')
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    bed_id = fields.Many2one('hospital.bed', string='Hospital Bed', required=True)
    ward_id = fields.Many2one('hospital.ward', string='Ward')
    extra_info = fields.Text(string='Extra Info')
    transfer_date = fields.Date(string='Transfer Date')
    transfer_from = fields.Many2one('hospital.bed', string='From')
    transfer_to = fields.Many2one('hospital.bed', string='To')
    attending_physician_id = fields.Many2one('hospital.doctor', string='Attending Physician')
    operating_physician_id = fields.Many2one('hospital.doctor', string='Operating Physician')
    admission_date = fields.Datetime(string='Admission Date', default=fields.Datetime.now)
    discharge_date = fields.Datetime(string='Expected Discharge Date')
    actual_discharge_date = fields.Datetime(string='Actual Discharge Date')
    admission_type = fields.Selection([
        ('routine', 'Routine'),
        ('maternity', 'Maternity'),
        ('icu', 'ICU'),
        ('emergency', 'Emergency'),
        ('elective', 'Elective'),
    ], string='Admission Type', default='routine')
    reason = fields.Selection([
        ('pregnancy', 'Pregnancy'),
        ('cancer', 'Cancer'),
        ('hiv', 'HIV/AIDS'),
        ('ulcer', 'Ulcer'),
        ('fever', 'High Fever'),
        ('surgery', 'Surgery Required'),
        ('injury', 'Injury/Trauma'),
        ('heart_disease', 'Heart Disease'),
        ('respiratory', 'Respiratory Infection'),
        ('diabetes', 'Diabetes Complications'),
        ('stroke', 'Stroke'),
        ('kidney_failure', 'Kidney Failure'),
        ('bleeding', 'Severe Bleeding'),
        ('poisoning', 'Poisoning'),
        ('mental_health', 'Mental Health Crisis'),
        ('other', 'Other'),
    ], string='Reason for Admission', default='other')
    state = fields.Selection([
        ('free', 'Free'),
        ('confirmed', 'Confirmed'),
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
    ], string='Status', default='free')
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.inpatient') or 'New'
        return super().create(vals)

    def action_confirm(self):
        self.state = 'confirmed'
        self.bed_id.state = 'occupied'

    def action_admit(self):
        self.state = 'admitted'

    def action_discharge(self):
        self.state = 'discharged'
        self.actual_discharge_date = fields.Datetime.now()
        self.bed_id.state = 'free'


class HospitalWard(models.Model):
    _name = 'hospital.ward'
    _description = 'Hospital Ward'

    name = fields.Char(string='Ward Name', required=True)
    building_id = fields.Many2one('hospital.building', string='Building')
    unit_id = fields.Many2one('hospital.unit', string='Unit')
    capacity = fields.Integer(string='Number of Beds')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('mixed', 'Mixed'),
    ], string='Gender')
    has_ac = fields.Boolean(string='Air Conditioning')
    has_tv = fields.Boolean(string='Television')
    has_internet = fields.Boolean(string='Internet Access')
    bed_ids = fields.One2many('hospital.bed', 'ward_id', string='Beds')
    notes = fields.Text(string='Notes')


class HospitalBed(models.Model):
    _name = 'hospital.bed'
    _description = 'Hospital Bed'

    name = fields.Char(string='Bed Number', required=True)
    ward_id = fields.Many2one('hospital.ward', string='Ward', required=True)
    bed_type = fields.Selection([
        ('standard', 'Standard'),
        ('electric', 'Electric'),
        ('icu', 'ICU'),
        ('maternity', 'Maternity'),
    ], string='Bed Type', default='standard')
    state = fields.Selection([
        ('free', 'Free'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ], string='Status', default='free')
    notes = fields.Text(string='Notes')


class HospitalBuilding(models.Model):
    _name = 'hospital.building'
    _description = 'Hospital Building'

    name = fields.Char(string='Building Name', required=True)
    institution_id = fields.Many2one('hospital.institution', string='Health Center')
    notes = fields.Text(string='Notes')


class HospitalUnit(models.Model):
    _name = 'hospital.unit'
    _description = 'Hospital Unit'

    name = fields.Char(string='Unit Name', required=True)
    institution_id = fields.Many2one('hospital.institution', string='Health Center')
    building_id = fields.Many2one('hospital.building', string='Building')
    notes = fields.Text(string='Notes')


class HospitalInstitution(models.Model):
    _name = 'hospital.institution'
    _description = 'Health Center / Institution'

    name = fields.Char(string='Institution Name', required=True)
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    notes = fields.Text(string='Notes')