"""
Model for IT Consumable Supplier Requests (Header).
"""
from odoo import models, fields, api
from odoo.fields import Command
from odoo.exceptions import UserError


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

    def action_mark_ordered(self):
        """Set request state to ordered."""
        for record in self:
            record.state = 'ordered'

    def action_mark_received(self):
        """Set request state to received."""
        for record in self:
            record.state = 'received'

    @api.model
    def _get_restock_line_commands(self, category_ids=None, consumable_ids=None):
        """
        Universal method: generates commands (Command.create) for items
        requiring restocking.
        """
        domain = []

        # Filter by provided categories
        if category_ids:
            domain.append(('category_id', 'in', category_ids.ids))

        # Filter by specific consumables (e.g., selected from the list view)
        if consumable_ids:
            domain.append(('id', 'in', consumable_ids.ids))

        # Search consumables and filter those with low stock
        consumables = self.env['bp.it.consumable.consumable'].search(domain)
        low_stock_items = consumables.filtered(
            lambda c: c.qty_available <= c.qty_min
        )

        if not low_stock_items:
            raise UserError(
                self.env._("No consumables require restocking at this moment.")
            )

        # Build the list of commands
        commands = []
        for item in low_stock_items:
            qty_to_order = item.qty_order if item.qty_order > 0 else 1.0
            commands.append(Command.create({
                'consumable_id': item.id,
                'qty': qty_to_order,
            }))

        return commands

    def action_repopulate_lines(self):
        """Clear existing lines and populate them based on supplier's categories."""
        self.ensure_one()

        if self.state != 'draft':
            raise UserError(
                self.env._("You can only repopulate lines for a draft request.")
            )

        # Call the universal method to get new lines
        categories = self.partner_id.consumable_category_ids
        new_line_commands = self._get_restock_line_commands(category_ids=categories)

        # Add Command.clear() to remove old lines before creating new ones
        self.line_ids = [Command.clear()] + new_line_commands
