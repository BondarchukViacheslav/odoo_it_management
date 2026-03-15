"""
Main model for IT Consumables.
"""
from odoo import models, fields, api


class BPITConsumableConsumable(models.Model):
    """Main model representing an IT consumable item (e.g. cartridge)."""
    _name = 'bp.it.consumable.consumable'
    _description = 'IT Consumable'
    _order = 'name'

    name = fields.Char(required=True)

    category_id = fields.Many2one(
        'bp.it.consumable.category',
        required=True
    )

    qty_available = fields.Float(
        compute='_compute_qty_available',
        store=True
    )

    qty_min = fields.Float(default=0.0)

    qty_order = fields.Float(default=0.0)

    compatible_equipment_ids = fields.Many2many(
        'bp.it.equipment.equipment',
        relation='bp_it_consumable_equipment_rel',
        column1='consumable_id',
        column2='equipment_id'
    )

    # Add One2many relations for correct @api.depends triggering
    issue_ids = fields.One2many(
        'bp.it.consumable.issue',
        'consumable_id',
        string='Issues'
    )

    request_line_ids = fields.One2many(
        'bp.it.consumable.request.line',
        'consumable_id',
        string='Request Lines'
    )

    def _compute_display_name(self):
        """Compute the display name for the record."""
        for record in self:
            record.display_name = record.name or self.env._('New Consumable')

    @api.depends('issue_ids.qty', 'request_line_ids.qty', 'request_line_ids.request_id.state')
    def _compute_qty_available(self):
        """
        Compute available quantity:
        Received from suppliers minus Issued to employees/equipment.
        """
        for record in self:
            # Calculate total received quantity
            received_qty = sum(
                line.qty for line in record.request_line_ids
                if line.request_id.state == 'received'
            )

            # Calculate total issued quantity
            issued_qty = sum(issue.qty for issue in record.issue_ids)

            # Calculate available stock
            record.qty_available = received_qty - issued_qty

    def action_create_issue(self):
        """Open a form in a modal window to issue this consumable."""
        self.ensure_one()
        return {
            'name': self.env._('Issue Consumable'),
            'type': 'ir.actions.act_window',
            'res_model': 'bp.it.consumable.issue',
            'view_mode': 'form',
            'target': 'new',  # Opens the form as a modal dialog
            'context': {
                'default_consumable_id': self.id,
            }
        }
