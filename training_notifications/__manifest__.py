{
    'name': 'Focus HRM Training notification',
    'version': '16.0',
    'summary': 'training notification ',
    'author': 'Focus corporation',
    'company': 'Focus corporation',
    'depends': ['base', 'Training_Management'],
    'maintainer': 'Focus corporation',
    'data': [ 
        'views/mail_template.xml',
        'views/hr_training_view.xml',
        'data/mail_cron.xml',   
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',

}