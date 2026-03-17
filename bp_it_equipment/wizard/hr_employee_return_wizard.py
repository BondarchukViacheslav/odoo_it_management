from odoo import models, fields, api


class HREmployeeReturnWizard(models.TransientModel):
    """
    Wizard for mass returning IT equipment from an employee.
    Used during offboarding processes to ensure all assets are recovered.
    """
    _name = 'hr.employee.return.wizard'
    _description = 'Mass Equipment Return Wizard'

    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True)
    line_ids = fields.One2many(
        'hr.employee.return.wizard.line',
        'wizard_id',
        string="Equipment to Return"
    )

    @api.model
    def default_get(self, fields):
        """
        Pre-fills the wizard lines with all active assignments for the selected employee.
        """
        res = super(HREmployeeReturnWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            res['employee_id'] = active_id
            assignments = self.env['bp.it.equipment.assignment'].search([
                ('employee_id', '=', active_id),
                ('state', '=', 'active')
            ])

            lines = []
            for asm in assignments:
                lines.append((0, 0, {
                    'assignment_id': asm.id,
                    'equipment_id': asm.equipment_id.id,
                    'condition': 'available'
                }))
            res['line_ids'] = lines
        return res

    def action_confirm(self):
        """
        Finalizes the return process. Updates assignments to 'returned'
        and resets equipment state based on the chosen final condition.
        """
        for line in self.line_ids:
            # Update the assignment record: set end date and state
            line.assignment_id.write({
                'state': 'returned',
                'date_end': fields.Date.today()
            })

            # Complex logic: Unlink the employee from the asset and update asset health
            if line.assignment_id.equipment_id:
                line.assignment_id.equipment_id.write({
                    'employee_id': False,
                    'state': line.condition
                })
        return {'type': 'ir.actions.client', 'tag': 'reload'}


class HREmployeeReturnWizardLine(models.TransientModel):
    _name = 'hr.employee.return.wizard.line'
    _description = 'Mass Equipment Return Line'

    wizard_id = fields.Many2one('hr.employee.return.wizard')
    assignment_id = fields.Many2one('bp.it.equipment.assignment')
    equipment_id = fields.Many2one(
        'bp.it.equipment.equipment',
        string="Equipment", readonly=True
    )
    condition = fields.Selection([
        ('available', 'Good (Available)'),
        ('repair', 'Needs Repair'),
        ('scrapped', 'Worn Out (Scrapped)')
    ], string="Final Condition", default='available', required=True)
