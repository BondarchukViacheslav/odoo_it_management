"""
Extension of equipment model from bp_it_equipment.
"""
from odoo import models, fields


class BPITEquipmentEquipment(models.Model):
    """Inherit equipment model to add consumable issues."""
    _inherit = 'bp.it.equipment.equipment'

    consumable_issue_ids = fields.One2many(
        'bp.it.consumable.issue',
        'equipment_id'
    )
