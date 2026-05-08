from odoo import models, fields,api

class ReportsDaily(models.Model):
    _name = 'reports.daily'
    _description = 'Daily Reports'

    name = fields.Char(string="Report Name")
    date = fields.Date(string="Date")
    report_date = fields.Date(string="Report Date")
    total_patients = fields.Integer(string="Total Patients")
    total_revenue = fields.Float(string="Total Revenue")

    # New relational fields
    appointment_ids = fields.One2many('hospital.appointment', 'report_id', string="Appointments")
    patient_ids = fields.Many2many('hospital.patient', string="Patients")
    doctor_ids = fields.Many2many('hospital.doctor', string="Doctors")

    @api.depends('appointment_ids')
    def _compute_total_patients(self):
        for record in self:
            record.total_patients = len(record.appointment_ids)
            

        def action_open_wizard(self):
            return {
        'type': 'ir.actions.act_window',
        'name': 'Filter Appointments',
        'res_model': 'appointment.report.wizard',
        'view_mode': 'form',
        'target': 'new',
    }