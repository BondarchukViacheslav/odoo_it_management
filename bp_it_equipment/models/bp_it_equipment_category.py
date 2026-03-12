from odoo import models, fields


class BPITEquipmentCategory(models.Model):
    _name = 'bp.it.equipment.category'
    _description = 'Equipment Category'
    _order = 'name'

    name = fields.Char(string='Category Name', required=True)

    equipment_ids = fields.One2many(
        'bp.it.equipment.equipment',
        'category_id',
        string='Equipments'
    )

    equipment_count = fields.Integer(
        string='Equipment Count',
        compute='_compute_equipment_count'
    )

    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = len(record.equipment_ids)
