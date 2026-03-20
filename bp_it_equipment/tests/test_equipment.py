from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.exceptions import ValidationError


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

    def test_01_equipment_methods_and_logging(self):
        """ Тест методів зміни стану та логування """
        # Перевірка action_set_repair
        self.equipment.action_set_repair()
        self.assertEqual(self.equipment.state, 'repair')

        # Перевірка action_set_available
        self.equipment.action_set_available()
        self.assertEqual(self.equipment.state, 'available')

        # Перевірка створення логу при зміні стану через write
        logs_count = len(self.equipment.status_log_ids)
        self.equipment.write({'state': 'scrapped'})

        # Перевіряємо, що кількість логів збільшилась
        self.assertEqual(len(self.equipment.status_log_ids), logs_count + 1)

        # Отримуємо саме останній створений лог, ігноруючи сортування за датою
        last_log = self.equipment.status_log_ids.sorted('id', reverse=True)[0]
        self.assertEqual(last_log.new_state, 'scrapped')
        
    def test_02_onchange_employee(self):
        """ Тест логіки @api.onchange('employee_id') """
        # Спрацювання onchange при призначенні
        self.equipment.employee_id = self.employee
        self.equipment._onchange_employee_id()
        self.assertEqual(self.equipment.state, 'assigned')

        # Спрацювання onchange при видаленні співробітника
        self.equipment.employee_id = False
        self.equipment._onchange_employee_id()
        self.assertEqual(self.equipment.state, 'available')

    def test_03_assignment_constraints(self):
        """ Тест обмежень моделі призначення """
        # Спроба призначити обладнання в ремонті має викликати помилку
        self.equipment.state = 'repair'
        assignment = self.env['bp.it.equipment.assignment'].create({
            'employee_id': self.employee.id,
            'equipment_id': self.equipment.id,
            'state': 'draft'
        })
        with self.assertRaises(ValidationError):
            assignment.action_confirm()

    def test_04_assignment_confirmation_and_return(self):
        """ Тест повного циклу призначення через модель assignment """
        self.equipment.state = 'available'
        assignment = self.env['bp.it.equipment.assignment'].create({
            'employee_id': self.employee.id,
            'equipment_id': self.equipment.id,
        })

        # Підтвердження призначення
        assignment.action_confirm()
        self.assertEqual(assignment.state, 'active')
        self.assertEqual(self.equipment.state, 'assigned')
        self.assertEqual(self.equipment.employee_id, self.employee)

        # Повернення обладнання
        assignment.action_return()
        self.assertEqual(assignment.state, 'returned')
        self.assertEqual(self.equipment.state, 'available')
        self.assertFalse(self.equipment.employee_id)

    def test_05_mass_return_wizard_logic(self):
        """ Розширений тест візарда масового повернення """
        # Створюємо активне призначення
        self.env['bp.it.equipment.assignment'].create({
            'employee_id': self.employee.id,
            'equipment_id': self.equipment.id,
            'state': 'active'
        })
        self.equipment.write({'employee_id': self.employee.id, 'state': 'assigned'})

        # Ініціалізація візарда
        wizard = self.env['hr.employee.return.wizard'].with_context(
            active_id=self.employee.id
        ).create({})

        # Перевірка default_get (автозаповнення рядків)
        self.assertTrue(len(wizard.line_ids) > 0)
        self.assertEqual(wizard.line_ids[0].equipment_id, self.equipment)

        # Зміна стану на 'repair' через візард
        wizard.line_ids[0].condition = 'repair'
        wizard.action_confirm()

        self.assertEqual(self.equipment.state, 'repair')
        self.assertFalse(self.equipment.employee_id)
