from odoo import models

class AppointmentReportXlsx(models.AbstractModel):
    _name = 'report.appointment_report_wizard.appointment_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Appointments Excel Report'

    def generate_xlsx_report(self, workbook, data, wizard):
        sheet = workbook.add_worksheet('Appointments')
        bold = workbook.add_format({'bold': True})

        sheet.write(0, 0, 'Date', bold)
        sheet.write(0, 1, 'Doctor', bold)
        sheet.write(0, 2, 'Patient', bold)

        appointments = self.env['doctor.appointment'].search([
            ('date', '>=', wizard.start_date),
            ('date', '<=', wizard.end_date),
            ('doctor_id', '=', wizard.doctor_id.id) if wizard.doctor_id else (1, '=', 1)
        ])

        row = 1
        for appt in appointments:
            sheet.write(row, 0, str(appt.date))
            sheet.write(row, 1, appt.doctor_id.name)
            sheet.write(row, 2, appt.patient_id.name)
            row += 1
