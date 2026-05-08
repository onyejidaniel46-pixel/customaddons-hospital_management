from odoo import models, fields,api


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    report_id = fields.Many2one('reports.daily', string="Daily Report")
    date = fields.Datetime(string="Appointment Date", required=True)
    notes = fields.Text(string="Notes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft')

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # find or create today's daily report
        today = fields.date.today()
        report = self.env['reports.daily'].search([
            ('report_date', '=', today)
        ], limit=1)
        if not report:
            # each appointment creates a new report for the day separately
            report = self.env['reports.daily'].create({
                'report_date': today,
                'name': f"Daily Report - {today}",
                'total_patients': 0,
                'total_revenue': 100.0,
                'appointment_ids': [(4, record.id)],
            })
        record.report_id = report.id
        record.state = 'sent'
        # send approval request email to the doctor
        template = self.env.ref('hospital_management.email_template_appointment_to_doctor')
        if template:
            template.send_mail(record.id, force_send=True)
        return record

    def action_confirm(self):
        for record in self:
            if record.state not in ('draft', 'sent'):
                continue
            record.state = 'approved'
            template = self.env.ref('hospital_management.email_template_appointment_confirm')
            if template:
                template.send_mail(record.id, force_send=True)