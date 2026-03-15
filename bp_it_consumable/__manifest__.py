{
    'name': 'IT Consumable Management',
    'version': '19.0.2.0.0',
    'category': 'IT Management',
    'summary': 'Облік витратних матеріалів та картриджів відділу IT',
    'sequence': 10,
    "author": "Serhii Pidopryhora, "
    "Odoo Community Association (OCA)",
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'hr',
        'bp_it_equipment',
    ],
    'data': [
        'data/bp_it_consumable_sequence.xml',

        'security/bp_it_consumable_groups.xml',
        'security/bp_it_consumable_rules.xml',
        'security/ir.model.access.csv',

        'views/bp_it_consumable_res_partner_view.xml',
        'views/bp_it_consumable_equipment_view.xml',

        'views/bp_it_consumable_category_view.xml',
        'views/bp_it_consumable_consumable_view.xml',
        'views/bp_it_consumable_issue_view.xml',
        'views/bp_it_consumable_request_view.xml',
        'views/bp_it_consumable_request_line_view.xml',

        'wizard/bp_it_consumable_request_wizard_view.xml',

        'views/bp_it_consumable_menu.xml',

        'report/bp_it_consumable_request_report.xml',
    ],
    'demo': [
        'demo/bp_it_consumable_res_partner_demo.xml',
        'demo/bp_it_consumable_hr_employee_demo.xml',
        'demo/bp_it_consumable_category_demo.xml',
        'demo/bp_it_consumable_consumable_demo.xml',
        'demo/bp_it_consumable_issue_demo.xml',
        'demo/bp_it_consumable_request_demo.xml',
        'demo/bp_it_consumable_request_line_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [
        'static/description/icon.png'
    ],
}
