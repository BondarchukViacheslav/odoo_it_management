"""
Extension of standard hr.employee model.
"""
from odoo import models, fields


class HrEmployee(models.Model):
    """Inherit employee model to add consumable issue count."""
    _inherit = 'hr.employee'

    consumable_issue_count = fields.Integer(
        compute='_compute_consumable_issue_count'
    )

    def _compute_consumable_issue_count(self):
        """Compute the total number of consumable issues for employee."""
        issue_model = self.env['bp.it.consumable.issue']
        for employee in self:
            employee.consumable_issue_count = issue_model.search_count([
                ('employee_id', '=', employee.id)
            ])
