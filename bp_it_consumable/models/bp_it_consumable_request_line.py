"""
Model for IT Consumable Supplier Request Lines.
"""
from odoo import models, fields


class BPITConsumableRequestLine(models.Model):
    """Line model for supplier consumable requests."""
    _name = 'bp.it.consumable.request.line'
    _description = 'Consumable Request Line'
    _order = 'request_id, id'

    request_id = fields.Many2one(
        'bp.it.consumable.request',
        required=True,
        ondelete='cascade'
    )

    consumable_id = fields.Many2one(
        'bp.it.consumable.consumable',
        required=True
    )

    qty = fields.Float(
        default=1.0,
        required=True
    )

    def _compute_display_name(self):
        """Compute the display name using lazy translation formatting."""
        for record in self:
            if record.request_id and record.consumable_id:
                record.display_name = self.env._(
                    "%(request)s - %(consumable)s",
                    request=record.request_id.name,
                    consumable=record.consumable_id.name
                )
            else:
                record.display_name = self.env._('New Line')
