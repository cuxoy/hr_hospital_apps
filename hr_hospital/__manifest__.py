{
    'name': 'HR Hospital by Cuxoy',
    'summary':'Hospital menagement system',
    'version': '19.0.1.0.0',
    "author": "Dmytro Sukhorukov",
    "website": "https://github.com/ccccuxoy",
    'category': 'Services',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'external_dependencies': {
        'python': []
    },

    'data': [
    'security/security.xml',
    'security/ir.model.access.csv',

    'data/disease_data.xml',
    'data/doctor_category_data.xml',

    'views/doctor_views.xml',
    'views/patient_views.xml',
    'views/disease_views.xml',
    'views/visit_views.xml',
    'views/doctor_category_views.xml',
    'views/doctor_history_views.xml',
    'views/wizard_views.xml',
    'views/hr_hospital_menu.xml',
    'report/doctor_report.xml',
],
    'demo': ['demo/demo_data.xml',
],
    'installable': True,
    'application': True,
    'auto_install': False,
}