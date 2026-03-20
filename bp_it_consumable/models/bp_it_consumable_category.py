"""
Model for IT Consumable Categories.
"""
from odoo import models, fields


class BPITConsumableCategory(models.Model):
    """Category model for grouping IT consumables."""
    _name = 'bp.it.consumable.category'
    _description = 'Consumable Category'
    _order = 'name'

    name = fields.Char(required=True)

    def _compute_display_name(self):
        """Compute the display name for the record."""
        for record in self:
            record.display_name = record.name or self.env._('New Category')
