from odoo import models, fields, api


class BPITEquipmentEquipment(models.Model):
    """
    Main model for tracking IT equipment units.
    Contains technical details, serial numbers, and current status.
    """
    _name = 'bp.it.equipment.equipment'
    _description = 'IT Equipment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Equipment Name',
        required=True,
        tracking=True,
        help="Model name, e.g. MacBook Pro 14 or Dell U2412M"
    )

    serial_number = fields.Char(
        string='Serial Number',
        required=True,
        copy=False
    )

    inventory_number = fields.Char(
        string='Inventory Number',
        help="Internal company asset ID"
    )

    state = fields.Selection([
        ('draft', 'New'),
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('repair', 'In Repair'),
        ('scrapped', 'Scrapped'),
    ], string='Status', default='draft', group_expand='_read_group_state')

    purchase_date = fields.Date(string='Purchase Date')

    warranty_expiry = fields.Date(string='Warranty Expiry')

    note = fields.Text(string='Internal Notes')

    active = fields.Boolean(default=True, help="Set to False to hide the record without deleting it.")

    category_id = fields.Many2one(
        'bp.it.equipment.category',
        string='Category',
        required=True
    )

    status_log_ids = fields.One2many('bp.it.equipment.status.log', 'equipment_id')

    def action_set_available(self):
        """ Sets the equipment status to Available. """
        for record in self:
            record.state = 'available'

    def action_set_repair(self):
        """ Sets the equipment status to In Repair. """
        for record in self:
            record.state = 'repair'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            self.env['bp.it.equipment.status.log'].create({
                'equipment_id': record.id,
                'new_state': record.state,
                'note': 'Initial creation'
            })
        return records

    def write(self, vals):
        if 'state' in vals:
            for record in self:
                if record.state != vals['state']:
                    self.env['bp.it.equipment.status.log'].create({
                        'equipment_id': record.id,
                        'old_state': record.state,
                        'new_state': vals['state'],
                        'note': 'Status change via interface'
                    })
        return super().write(vals)

    @api.model
    def _read_group_state(self, *args, **kwargs):
        # Отримуємо всі ключі з нашого Selection поля 'state'
        # ВАЖЛИВО: перетворюємо на список (list), щоб Odoo зрозуміла результат
        state_list = [key for key, val in self._fields['state'].selection]
        return state_list
