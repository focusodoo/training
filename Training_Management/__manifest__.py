{
    'name': 'Focus HRM Training Management',
    'version': '16.0',
    'summary': 'Training Management',
    'sequence': -100,
    'description': """Training Management""",
    'author': 'Focus Corporation',
    'company': 'Focus corporation',
    'website':'https://focus-corporation.com/',
    'license': 'AGPL-3',
    'depends': [
        'hr', 'base','hr_skills','board'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_training_security.xml',
        'views/training_views.xml',
        'views/evaluation_by_manager.xml',
        'views/evaluation_by_employee_view.xml',
        'views/dashboard.xml',
        'views/employee_eval_view.xml'


    ],
    'assets':{
        'web.assets_backend': [
            'Training_Management/static/src/css/style.scss',

        ],
    },
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': '4.99',
    'currency': 'USD',
}