from odoo import models, fields

class AppointmentReportWizard(models.TransientModel):
    _name=  'appointment.report.wizard'
    _description = 'Wizard for Appointment Report'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")  # ✅ fixed

    def action_generate_report(self):
        domain = [('date', '>=', self.start_date), ('date', '<=', self.end_date)]
        if self.doctor_id:
            domain.append(('doctor_id', '=', self.doctor_id.id))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments Report',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',  # ✅ fixed
            'domain': domain,
        }