{
    'name': 'IT equipment management',
    'version': '19.0.1.0.2',
    'category': 'Accounting',
    'summary': 'Personal finance management: income, expenses, budgets',
    'sequence': 10,
    'author': 'Bondarchuk Viacheslav',
    # 'website': 'https://www.yourwebsite.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'hr',
    ],
    'data': [
        'security/bp_it_management_groups.xml',
        'security/ir.model.access.csv',
        'security/bp_it_management_rules.xml',
        'views/bp_it_equipment_equipment_view.xml',
        'views/bp_it_equipment_category_view.xml',
        'views/bp_it_equipment_assignment_view.xml',
        'views/bp_it_equipment_software_view.xml',
        'views/bp_it_equipment_software_instance_view.xml',
        'views/bp_it_equipment_menu.xml',
        'wizard/hr_employee_return_wizard.view.xml',
        'views/hr_employee_view.xml',
        'data/bp_it_equipment_category_data.xml',
        'report/hr_employee_reports.xml',
        'report/hr_employee_equipment_template.xml',
    ],
    'demo': [
        'demo/bp_it_equipment_equipment_demo.xml',
        'demo/bp_it_equipment_software_demo.xml',
        'demo/bp_it_equipment_software_instance_demo.xml',
        'demo/bp_it_equipment_assignment_demo.xml',
        'demo/bp_it_equipment_status_log_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],

}
