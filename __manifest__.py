{
    'name': 'Hospital Management Dev',
    'version': '1.0.0',
    'category': 'Healthcare',
    'summary': 'Hospital Management System',
    'author': 'Daniel Allison',
    'description': """Hospital Management System to manage patients, doctors, and appointments.""",
    'depends': ['base', 'mail', 'website'],
    'data': [
    'security/ir.model.access.csv',          # ← ALWAYS first
    'data/hospital_email_templates.xml',
    'views/hospital_patient_views.xml',
    'views/hospital_doctor_views.xml',
    'views/hospital_nursing_views.xml',
    'views/hospital_prescription_views.xml',
    'views/hospital_billing_views.xml',
    'views/appointment_views.xml',
    'views/hospital_laboratory_views.xml',
    'views/hospital_inpatient_views.xml',
    'views/hospital_clinical_views.xml',
    'views/reports_views.xml',
    'views/appointment_report_wizard_views.xml',
    'views/hospital_menu.xml',             
    
        ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    
}
