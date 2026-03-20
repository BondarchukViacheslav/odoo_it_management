"""
Model for IT Consumable Issues (Log).
"""
from odoo import models, fields, api


class BPITConsumableIssue(models.Model):
    """Log model to track which consumable was issued to whom/where."""
    _name = 'bp.it.consumable.issue'
    _description = 'Consumable Issue Log'
    _order = 'issue_date desc, id desc'

    consumable_id = fields.Many2one(
        'bp.it.consumable.consumable',
        required=True
    )

    employee_id = fields.Many2one(
        'hr.employee',
        required=True
    )

    equipment_id = fields.Many2one(
        'bp.it.equipment.equipment',
        help="Optional: specific equipment this consumable was used for."
    )

    # Technical field for access to compatible_equipment_ids
    compatible_equipment_ids = fields.Many2many(
        related='consumable_id.compatible_equipment_ids',
        string="Compatible Equipments"
    )

    issue_date = fields.Date(
        default=fields.Date.context_today,
        required=True
    )

    qty = fields.Float(
        default=1.0,
        required=True
    )

    def _compute_display_name(self):
        """Compute the display name using lazy translation formatting."""
        for record in self:
            if record.consumable_id and record.employee_id:
                record.display_name = self.env._(
                    "Issue %(consumable)s to %(employee)s",
                    consumable=record.consumable_id.name,
                    employee=record.employee_id.name
                )
            else:
                record.display_name = self.env._('New Issue')

    @api.onchange('consumable_id')
    def _onchange_consumable_id(self):
        """
        Dynamically restrict the equipment_id domain based on the selected consumable.
        Clear the equipment_id if it is no longer compatible.
        """
        self.ensure_one()

        if self.compatible_equipment_ids:
            # Clear equipment_id if the previously selected equipment is not compatible anymore
            if self.equipment_id and self.equipment_id not in self.compatible_equipment_ids:
                self.equipment_id = False
