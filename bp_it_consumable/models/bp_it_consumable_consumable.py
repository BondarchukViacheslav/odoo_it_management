"""
Main model for IT Consumables.
"""
from odoo import models, fields


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

    def _compute_display_name(self):
        """Compute the display name for the record."""
        for record in self:
            record.display_name = record.name or self.env._('New Consumable')

    def _compute_qty_available(self):
        """
        Compute available quantity.
        Will be fully implemented after adding issue and request models.
        """
        for record in self:
            # Placeholder: will calculate (Received - Issued) later
            record.qty_available = 0.0
