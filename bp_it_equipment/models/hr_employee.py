from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    equipment_ids = fields.One2many(
        'bp.it.equipment.assignment',
        'employee_id',
        string='Assigned Equipment',
        domain=[('state', '=', 'active')],
        help="List of IT equipment currently assigned to this employee."
    )
