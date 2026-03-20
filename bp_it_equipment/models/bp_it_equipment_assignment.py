from odoo import models, fields, _
from odoo.exceptions import ValidationError


class BPITEquipmentAssignment(models.Model):
    _name = 'bp.it.equipment.assignment'
    _description = 'Equipment Assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'

    name = fields.Char(
        string='Reference',
        readonly=True,
        default=_('New')
    )

    equipment_id = fields.Many2one(
        'bp.it.equipment.equipment',
        string='Equipment',
        required=True,
        tracking=True,
        domain="[('state', 'in', ('available', 'new'))]"
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
        default=lambda self: self.env.user.employee_id)

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

    equipment_state = fields.Selection(
        related='equipment_id.state',
        string="Equipment Status",
        readonly=True
    )

    _sql_constraints = [
        ('unique_active_equipment',
         'unique(equipment_id, state)',
         'This equipment is already assigned!')
    ]

    def action_confirm(self):
        """
        Confirm the equipment assignment to the employee.
        Validates if the equipment is not already assigned or in repair.
        Updates equipment state to 'Assigned' and links it to the employee.
        """
        for record in self:
            if record.equipment_id.employee_id:
                raise ValidationError(
                    _("Equipment %s is still assigned to %s. Please return it first!") %
                    (record.equipment_id.name, record.equipment_id.employee_id.name)
                )

            if record.equipment_id.state in ['repair', 'damaged']:
                raise ValidationError(
                    _("Equipment %s is %s and cannot be assigned.") %
                    (record.equipment_id.name, record.equipment_id.state)
                )

            record.equipment_id.write({
                'state': 'assigned',
                'employee_id': record.employee_id.id
            })

            record.write({
                'state': 'active',
                'name': f"{record.equipment_id.name} -> {record.employee_id.name}"
            })

    def action_return(self):
        """
        Process the equipment return.
        Sets equipment state back to 'Available', clears the employee link,
        and sets the assignment end date.
        """
        for record in self:
            record.equipment_id.state = 'available'
            record.state = 'returned'
            record.date_end = fields.Date.today()
            record.equipment_id.employee_id = False
