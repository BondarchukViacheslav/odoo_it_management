"""
Extension of standard res.partner model.
"""
from odoo import models, fields


class ResPartner(models.Model):
    """Inherit partner model to add consumable supplier flag."""
    _inherit = 'res.partner'

    is_consumable_supplier = fields.Boolean(
        default=False,
        help="Check this box if this partner supplies IT consumables."
    )

    consumable_category_ids = fields.Many2many(
        'bp.it.consumable.category',
        string="Supplied Categories"
    )
