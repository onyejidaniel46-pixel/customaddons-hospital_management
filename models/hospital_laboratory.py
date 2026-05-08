from odoo import models, fields, api

class Laboratory(models.Model):
    _name = 'hospital.laboratory'
    _description = 'Hospital Laboratory'

    name = fields.Char(string='Name', required=True)
    test_type = fields.Char(string='Test Type')
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    result = fields.Text(string='Result')
    date = fields.Datetime(string='Test Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], string='Status', default='draft')

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.doctor_id and record.patient_id:
            template = self.env.ref('hospital_management.email_template_lab_test_notification')
            if template:
                template.send_mail(record.id, force_send=True)
        return record