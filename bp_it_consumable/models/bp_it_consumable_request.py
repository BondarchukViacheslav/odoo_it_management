"""
Model for IT Consumable Supplier Requests (Header).
"""
from odoo import models, fields, api


class BPITConsumableRequest(models.Model):
    """Header model for supplier consumable requests."""
    _name = 'bp.it.consumable.request'
    _description = 'Consumable Request'
    _order = 'request_date desc, id desc'

    name = fields.Char(
        default=lambda self: self.env._('New'),
        readonly=True,
        copy=False
    )

    partner_id = fields.Many2one(
        'res.partner',
        required=True
    )

    request_date = fields.Date(
        default=fields.Date.context_today,
        required=True
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('ordered', 'Ordered'),
            ('received', 'Received')
        ],
        default='draft',
        required=True
    )

    # Зв'язок з моделлю рядків (буде створена в п. 3.5)
    line_ids = fields.One2many(
        'bp.it.consumable.request.line',
        'request_id'
    )

    def _compute_display_name(self):
        """Compute the display name for the record."""
        for record in self:
            record.display_name = record.name

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to assign sequence to name."""
        for vals in vals_list:
            if vals.get('name', self.env._('New')) == self.env._('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'bp.it.consumable.request.sequence'
                ) or self.env._('New')
        return super().create(vals_list)
