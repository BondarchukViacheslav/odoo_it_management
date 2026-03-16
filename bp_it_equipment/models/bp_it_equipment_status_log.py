from odoo import models, fields, api


class BPITEquipmentStatusLog(models.Model):
    _name = 'bp.it.equipment.status.log'
    _description = 'Equipment Status Log'
    _order = 'change_date desc'

    equipment_id = fields.Many2one(
        'bp.it.equipment.equipment',
        string='Equipment', ondelete='cascade', required=True)
    old_state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('repair', 'Repair'),
        ('scrapped', 'Scrapped')
    ], string='Old Status')

    new_state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('repair', 'Repair'),
        ('scrapped', 'Scrapped')
    ], string='New Status', required=True)

    user_id = fields.Many2one(
        'res.users',
        string='Changed By',
        default=lambda self: self.env.user)

    change_date = fields.Datetime(
        string='Change Date',
        default=fields.Datetime.now
    )

    note = fields.Text(string='Note')
