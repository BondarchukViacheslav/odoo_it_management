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
        # 'hr',  # Наслідування (для зв'язку з працівником, як один з пунктів)
    ],
    'data': [
        'security/bp_it_management_groups.xml',
        'security/ir.model.access.csv',
        'security/bp_it_management_rules.xml',
        'views/bp_it_equipment_equipment_view.xml',
        'views/bp_it_equipment_category_view.xml',
        'views/bp_it_equipment_assignment_view.xml',
        'views/bp_it_equipment_menu.xml',
        # 'views/cashflow_master_transaction.xml',
        # Сюди будемо додавати інші view по мірі створення
        'data/bp_it_equipment_category_data.xml',
    ],
    'demo': [
        'demo/bp_it_equipment_equipment_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

    'images': [
        # 'static/description/icon.png'
    ],

}
