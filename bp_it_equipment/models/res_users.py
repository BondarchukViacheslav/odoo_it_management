from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_it_technician = fields.Boolean(
        string='Is IT Technician',
        help="Check this if the user is part of the IT support team."
    )
