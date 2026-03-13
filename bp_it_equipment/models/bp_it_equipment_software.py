from odoo import models, fields, api


class BPITEquipmentSoftware(models.Model):
    _name = 'bp.it.equipment.software'
    _description = 'Software and Licenses'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Software Name', required=True, tracking=True)

    software_type = fields.Selection([
        ('os', 'Operating System'),
        ('app', 'Application'),
        ('subscription', 'Cloud Subscription'),
        ('service', 'Online Service')
    ], string='Software Type', default='app', required=True)

    license_type = fields.Selection([
        ('free', 'Free / Open Source'),
        ('retail', 'Retail (FPP)'),
        ('oem', 'OEM (Pre-installed)'),
        ('subscription', 'Subscription'),
        ('volume', 'Volume Licensing (VL)')
    ], string='License Type', default='free')

    license_required = fields.Boolean(
        string='License Required',
        default=True)

    license_key = fields.Char(
        string='License Key / ID',
        tracking=True)

    # Зв'язок з технікою (одна ліцензія — один пристрій)
    # Якщо потрібно ставити один Office на 5 комп'ютерів,
    # пізніше змінімо на Many2many
    equipment_id = fields.Many2one(
        'bp.it.equipment.equipment',
        string='Installed On',
        ondelete='set null'
    )

    expiration_date = fields.Date(string='Expiration Date', help="For subscriptions")
    vendor = fields.Char(string='Vendor', help="e.g., Microsoft, Adobe, JetBrains")

    is_active = fields.Boolean(string='Is Active', default=True)
    notes = fields.Text(string='Notes')
