from odoo import models, fields


class BPITEquipmentSoftware(models.Model):
    _name = 'bp.it.equipment.software'
    _description = 'Software Catalog'
    _order = 'name'

    name = fields.Char(string='Software Name', required=True)
    vendor = fields.Char(string='Vendor')
    default_license_required = fields.Boolean(
        string='License Required by Default',
        default=True
    )
    software_type = fields.Selection([
        ('os', 'Operating System'),
        ('app', 'Application'),
        ('driver', 'Driver'),
        ('service', 'Online Service'),
    ], string='Software Type', default='app')

    notes = fields.Text(string='Description')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Software name must be unique!')
    ]
