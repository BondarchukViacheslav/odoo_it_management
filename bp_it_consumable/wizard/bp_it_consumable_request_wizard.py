"""
Wizard model for automating consumable requests.
"""
from odoo import models, fields, api
from odoo.exceptions import UserError


class BPITConsumableRequestWizard(models.TransientModel):
    """Transient model to generate requests for low stock items."""
    _name = 'bp.it.consumable.request.wizard'
    _description = 'Automated Consumable Request Wizard'

    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        domain=[('is_consumable_supplier', '=', True)],
        help="Select the supplier for the generated request."
    )

    @api.model
    def default_get(self, fields_list):
        """Override default_get to handle context actions."""
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')

        # Automatically set partner if called from partner context action
        if active_model == 'res.partner' and active_id:
            res['partner_id'] = active_id

        return res

    def _compute_display_name(self):
        """Compute display name according to development standards."""
        for record in self:
            record.display_name = self.env._('Generate Consumable Request')

    def action_generate_requests(self):
        """Generate supplier request for consumables with low stock."""
        self.ensure_one()

        # Find all consumables and filter those that reached the minimum stock
        consumables = self.env['bp.it.consumable.consumable'].search([])
        low_stock_items = consumables.filtered(
            lambda c: c.qty_available <= c.qty_min
        )

        # If there are no items to order, notify the user
        if not low_stock_items:
            raise UserError(
                self.env._("No consumables require restocking at this moment.")
            )

        # Create the request header
        request_vals = {
            'partner_id': self.partner_id.id,
        }
        new_request = self.env['bp.it.consumable.request'].create(request_vals)

        # Create request lines for each low stock item
        for item in low_stock_items:
            qty_to_order = item.qty_order if item.qty_order > 0 else 1.0

            self.env['bp.it.consumable.request.line'].create({
                'request_id': new_request.id,
                'consumable_id': item.id,
                'qty': qty_to_order,
            })

        # Return an action to open the created request
        return {
            'name': self.env._("Generated Request"),
            'type': 'ir.actions.act_window',
            'res_model': 'bp.it.consumable.request',
            'view_mode': 'form',
            'res_id': new_request.id,
            'target': 'current',
        }
