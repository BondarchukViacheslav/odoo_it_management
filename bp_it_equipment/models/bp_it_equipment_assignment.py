from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BPITEquipmentAssignment(models.Model):
    _name = 'bp.it.equipment.assignment'
    _description = 'Equipment Assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'

    name = fields.Char(
        string='Reference',
        readonly=True,
        default=lambda self: self.env._('New')
    )

    equipment_id = fields.Many2one(
        'bp.it.equipment.equipment',
        string='Equipment',
        required=True,
        tracking=True
    )
    employee_id = fields.Many2one(
        'res.users',
        string='Employee',
        required=True,
        default=lambda self: self.env.user)

    date_start = fields.Date(
        string='Start Date',
        default=fields.Date.today,
        required=True)

    date_end = fields.Date(string='End Date')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('returned', 'Returned'),
    ], string='Status', default='draft', tracking=True)

    def action_confirm(self):
        for record in self:
            if record.equipment_id.state != 'available':
                raise ValidationError(
                    _("This equipment is not available for assignment! Current status: %s") % record.equipment_id.state)

            record.equipment_id.state = 'assigned'
            record.equipment_id.employee_id = record.employee_id
            record.state = 'active'
            record.name = f"{record.equipment_id.name} -> {record.employee_id.name}"

    def action_return(self):
        for record in self:
            record.equipment_id.state = 'available'
            record.state = 'returned'
            record.date_end = fields.Date.today()
            record.equipment_id.employee_id = False
