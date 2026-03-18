"""
Wizard model for automating consumable requests.
"""
from odoo import models, fields, api
from odoo.fields import Command


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

    category_ids = fields.Many2many(
        'bp.it.consumable.category',
        string="Categories to Order"
    )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Auto-fill categories based on the selected supplier."""
        if self.partner_id:
            self.category_ids = self.partner_id.consumable_category_ids
        else:
            self.category_ids = False

    @api.model
    def default_get(self, fields_list):
        """Override default_get to handle context actions."""
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')

        if active_model == 'res.partner' and active_id:
            res['partner_id'] = active_id
            # If a partner is selected, we immediately pull up his categories
            partner = self.env['res.partner'].browse(active_id)
            if partner.consumable_category_ids:
                res['category_ids'] = [Command.set(partner.consumable_category_ids.ids)]

        return res

    def _compute_display_name(self):
        """Compute display name according to development standards."""
        for record in self:
            record.display_name = self.env._('Generate Consumable Request')

    def action_generate_requests(self):
        """Generate supplier request for consumables with low stock."""
        self.ensure_one()

        active_ids = self.env.context.get('active_ids', [])
        active_model = self.env.context.get('active_model')

        # Determine if the wizard was called from selected consumables
        consumable_ids = None
        if active_model == 'bp.it.consumable.consumable' and active_ids:
            consumable_ids = self.env['bp.it.consumable.consumable'].browse(active_ids)

        # Call the Request model to get the prepared line commands
        request_model = self.env['bp.it.consumable.request']
        new_line_commands = request_model._get_restock_line_commands(
            category_ids=self.category_ids,
            consumable_ids=consumable_ids
        )

        # Create the Request with lines in a single transaction
        new_request = request_model.create({
            'partner_id': self.partner_id.id,
            'line_ids': new_line_commands,
        })

        # Return an action to open the newly created request
        return {
            'name': self.env._("Generated Request"),
            'type': 'ir.actions.act_window',
            'res_model': 'bp.it.consumable.request',
            'view_mode': 'form',
            'res_id': new_request.id,
            'target': 'current',
        }
