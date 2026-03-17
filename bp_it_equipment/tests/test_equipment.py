from odoo.tests.common import TransactionCase
from odoo import fields


class TestITEquipment(TransactionCase):

    def setUp(self):
        super(TestITEquipment, self).setUp()
        self.employee = self.env['hr.employee'].create({'name': 'Test Employee'})
        self.category = self.env['bp.it.equipment.category'].create({'name': 'Laptops'})
        self.equipment = self.env['bp.it.equipment.equipment'].create({
            'name': 'MacBook Pro',
            'category_id': self.category.id,
            'serial_number': 'SN123456789',
            'state': 'available'
        })

    def test_01_equipment_assignment(self):
        self.equipment.write({'employee_id': self.employee.id})
        self.assertEqual(self.equipment.employee_id.id, self.employee.id)

    def test_02_assignment_record(self):
        assignment = self.env['bp.it.equipment.assignment'].create({
            'employee_id': self.employee.id,
            'equipment_id': self.equipment.id,
            'date_start': fields.Date.today(),
            'state': 'active'
        })
        self.assertEqual(assignment.state, 'active')
        self.assertTrue(assignment.date_start)

    def test_03_return_wizard(self):
        # Створюємо активне призначення
        assignment = self.env['bp.it.equipment.assignment'].create({
            'employee_id': self.employee.id,
            'equipment_id': self.equipment.id,
            'state': 'active'
        })

        wizard = self.env['hr.employee.return.wizard'].with_context(active_id=self.employee.id).create({
            'employee_id': self.employee.id,
        })

        self.assertTrue(len(wizard.line_ids) > 0, "Wizard should pre-fill lines from active assignments")

        wizard.line_ids[0].condition = 'scrapped'

        wizard.action_confirm()

        self.assertEqual(assignment.state, 'returned')
        self.assertFalse(self.equipment.employee_id)
        self.assertEqual(self.equipment.state, 'scrapped')
