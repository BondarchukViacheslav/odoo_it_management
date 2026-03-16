from odoo import models, fields, api, _


class BPITEquipmentSoftwareInstance(models.Model):
    _name = 'bp.it.equipment.software.instance'
    _description = 'Installed Software Instance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    software_id = fields.Many2one(
        'bp.it.equipment.software',
        string='Software',
        required=True,
        tracking=True
    )

    name = fields.Char(
        related='software_id.name',
        string='Display Name',
        readonly=True,
        store=True
    )

    # Використовуємо related, щоб автоматично бачити тип з довідника
    software_type = fields.Selection(
        related='software_id.software_type',
        string='Type',
        readonly=True
    )

    equipment_id = fields.Many2one(
        'bp.it.equipment.equipment',
        string='Installed On',
        ondelete='cascade',
        required=True
    )

    license_required = fields.Boolean(
        string='License Required',
        tracking=True
    )

    license_key = fields.Char(string='License Key / ID', tracking=True)

    installation_date = fields.Date(
        string='Installation Date',
        default=fields.Date.today
    )

    @api.onchange('software_id')
    def _onchange_software_id(self):
        if self.software_id:
            self.license_required = self.software_id.default_license_required

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.software_id.name} ({record.equipment_id.name})"
            result.append((record.id, name))
        return result
