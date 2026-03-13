from odoo import models, fields, api


class BPITEquipmentSoftware(models.Model):
    _name = 'bp.it.equipment.software'
    _description = 'Software and Licenses'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Software Name', required=True, tracking=True)

    license_status = fields.Selection([
        ('valid', 'Valid'),
        ('missing', 'Missing Key'),
        ('not_required', 'Not Required')
    ], string='License Status', compute='_compute_license_status', store=True)

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

    equipment_id = fields.Many2one(
        'bp.it.equipment.equipment',
        string='Installed On',
        ondelete='set null'
    )

    expiration_date = fields.Date(string='Expiration Date', help="For subscriptions")
    vendor = fields.Char(string='Vendor', help="e.g., Microsoft, Adobe, JetBrains")

    is_active = fields.Boolean(string='Is Active', default=True)
    notes = fields.Text(string='Notes')

    @api.depends('license_required', 'license_key')
    def _compute_license_status(self):
        for record in self:
            if not record.license_required:
                record.license_status = 'not_required'
            elif record.license_key:
                record.license_status = 'valid'
            else:
                record.license_status = 'missing'
