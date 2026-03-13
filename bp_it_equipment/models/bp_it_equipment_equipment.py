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

    employee_id = fields.Many2one(
        'res.users',
        string='Assigned To',
        tracking=True,
        help="Current user of this equipment"
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
        for record in self:
            # 1. ЛОГІКА ІСТОРІЇ СТАТУСІВ (Твій код)
            if 'state' in vals and record.state != vals['state']:
                self.env['bp.it.equipment.status.log'].create({
                    'equipment_id': record.id,
                    'old_state': record.state,
                    'new_state': vals['state'],
                    'user_id': self.env.user.id,
                    'note': vals.get('note', 'Status change via interface')
                })

            # 2. ЛОГІКА ПРИЗНАЧЕНЬ (Assignments)
            if 'employee_id' in vals:
                new_employee_id = vals.get('employee_id')
                if new_employee_id:
                    # Створюємо запис про видачу
                    self.env['bp.it.equipment.assignment'].create({
                        'equipment_id': record.id,
                        'employee_id': new_employee_id,
                        'date_start': fields.Date.today(),
                        'state': 'active',
                        'name': f"Auto: {record.name}"
                    })
                elif record.employee_id:
                    # Якщо працівника прибрали — закриваємо останнє активне призначення
                    last_assignment = self.env['bp.it.equipment.assignment'].search([
                        ('equipment_id', '=', record.id),
                        ('employee_id', '=', record.employee_id.id),
                        ('state', '=', 'active')
                    ], limit=1)
                    if last_assignment:
                        last_assignment.state = 'returned'
                        last_assignment.date_end = fields.Date.today()

        return super().write(vals)

    @api.model
    def _read_group_state(self, *args, **kwargs):
        # Отримуємо всі ключі з нашого Selection поля 'state'
        # ВАЖЛИВО: перетворюємо на список (list), щоб Odoo зрозуміла результат
        state_list = [key for key, val in self._fields['state'].selection]
        return state_list

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        """
        Якщо ми обираємо працівника, статус автоматично стає 'Assigned'.
        Якщо прибираємо працівника — повертається в 'Available'.
        """
        if self.employee_id:
            self.state = 'assigned'
        else:
            # Якщо техніка була призначена, а тепер вільна
            if self.state == 'assigned':
                self.state = 'available'
