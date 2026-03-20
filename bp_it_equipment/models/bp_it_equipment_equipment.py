from odoo import models, fields, api


class BPITEquipmentEquipment(models.Model):
    """
    Main model for tracking IT assets like laptops, monitors, and printers.
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

    active = fields.Boolean(
        default=True,
        help="Set to False to hide the record without deleting it."
    )

    category_id = fields.Many2one(
        'bp.it.equipment.category',
        string='Category',
        required=True
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Assigned To',
        tracking=True,
        readonly=True,
        help="Current user of this equipment"
    )

    status_log_ids = fields.One2many('bp.it.equipment.status.log', 'equipment_id')

    software_instance_ids = fields.One2many(
        'bp.it.equipment.software.instance',
        'equipment_id',
        string='Installed Software'
    )

    def action_set_available(self):
        """
        Set the equipment state to 'Available'.
        Used for manual stock return or after completing repairs.
        """
        for record in self:
            record.state = 'available'

    def action_set_repair(self):
        """
        Set the equipment state to 'In Repair'.
        Used when the equipment requires maintenance or technical support.
        """
        for record in self:
            record.state = 'repair'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to automatically generate a status log entry.
        Creates an 'Initial creation' log for every new equipment record.
        """
        records = super().create(vals_list)
        for record in records:
            self.env['bp.it.equipment.status.log'].create({
                'equipment_id': record.id,
                'new_state': record.state,
                'note': 'Initial creation'
            })
        return records

    def write(self, vals):
        """
        Override write method to track changes in the 'state' field.
        If the state changes, a new entry is created in the status log
        history with previous and new state values.
        """
        for record in self:
            if 'state' in vals and record.state != vals['state']:
                self.env['bp.it.equipment.status.log'].create({
                    'equipment_id': record.id,
                    'old_state': record.state,
                    'new_state': vals['state'],
                    'user_id': self.env.user.id,
                    'note': vals.get('note', 'Status change via interface')
                })

        return super().write(vals)

    @api.model
    def _read_group_state(self, *args, **kwargs):
        """
        Ensure all state columns are displayed in the Kanban view,
        even if they don't contain any records.
        """
        state_list = [key for key, val in self._fields['state'].selection]
        return state_list

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        """
        If an employee is selected, the status automatically changes to 'Assigned'.
        If the employee is removed, it reverts to 'Available'.
        """
        if self.employee_id:
            self.state = 'assigned'
        else:
            if self.state == 'assigned':
                self.state = 'available'
