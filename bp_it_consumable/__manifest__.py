{
    'name': 'IT Consumable Management',
    'version': '19.0.1.0.0',
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
        # Сюди ми будемо додавати шляхи до файлів security, views, wizards, data тощо.
    ],
    'demo': [
        # 'data/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [
        'static/description/icon.png'
    ],
}

