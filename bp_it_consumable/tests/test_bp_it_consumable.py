"""
Tests for IT Consumable Management module.
"""
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestBPITConsumable(TransactionCase):
    """Test cases for bp_it_consumable models."""

    def setUp(self):
        """Set up test data."""
        super().setUp()

        # 1. Create dependencies
        self.partner = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'is_consumable_supplier': True,
        })
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
        })

        # 2. Create category
        self.category = self.env['bp.it.consumable.category'].create({
            'name': 'Test Category',
        })

        # 3. Create consumable
        self.consumable = self.env['bp.it.consumable.consumable'].create({
            'name': 'Test Toner',
            'category_id': self.category.id,
            'qty_min': 5.0,
            'qty_order': 10.0,
        })

    def test_01_category_creation(self):
        """Test category creation and display name."""
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.display_name, 'Test Category')

    def test_02_consumable_creation(self):
        """Test consumable fields and default values."""
        self.assertEqual(self.consumable.category_id, self.category)
        self.assertEqual(self.consumable.qty_min, 5.0)
        self.assertEqual(self.consumable.qty_available, 0.0)

    def test_03_issue_creation(self):
        """Test consumable issue log creation."""
        issue = self.env['bp.it.consumable.issue'].create({
            'consumable_id': self.consumable.id,
            'employee_id': self.employee.id,
            'qty': 1.0,
        })
        self.assertTrue(issue.id)
        self.assertEqual(issue.qty, 1.0)
        # Check if display name contains consumable and employee names
        self.assertIn('Test Toner', issue.display_name)
        self.assertIn('Test Employee', issue.display_name)

    def test_04_request_and_line_creation(self):
        """Test supplier request, sequence and lines."""
        request = self.env['bp.it.consumable.request'].create({
            'partner_id': self.partner.id,
        })

        # Check if sequence replaced the 'New' name
        self.assertNotEqual(request.name, 'New')
        self.assertTrue(request.name.startswith('REQ/'))

        # Add line
        line = self.env['bp.it.consumable.request.line'].create({
            'request_id': request.id,
            'consumable_id': self.consumable.id,
            'qty': 5.0,
        })
        self.assertEqual(len(request.line_ids), 1)
        self.assertEqual(line.qty, 5.0)
        self.assertIn('Test Toner', line.display_name)

    def test_05_wizard_generation(self):
        """Test the automated request generation wizard."""
        # Set consumable available qty below min (0 < 5)
        # It should be picked up by the wizard

        wizard = self.env['bp.it.consumable.request.wizard'].create({
            'partner_id': self.partner.id,
        })

        action = wizard.action_generate_requests()

        # Action should return a view for the new request
        self.assertEqual(action.get('res_model'), 'bp.it.consumable.request')
        request_id = action.get('res_id')
        self.assertTrue(request_id)

        # Check if the generated request has our test consumable
        request = self.env['bp.it.consumable.request'].browse(request_id)
        self.assertTrue(any(
            line.consumable_id == self.consumable for line in request.line_ids
        ))

    def test_06_action_repopulate_lines(self):
        """Test the repopulate lines action for draft requests."""
        # Setup the partner: add the category from setUp
        self.partner.consumable_category_ids = [(6, 0, [self.category.id])]

        # Create an empty draft request
        request = self.env['bp.it.consumable.request'].create({
            'partner_id': self.partner.id,
        })

        # Verify that the request is created without lines
        self.assertEqual(len(request.line_ids), 0)

        # Call the auto-fill method
        request.action_repopulate_lines()

        # Verify if our test consumable was added (it has qty_available=0, qty_min=5)
        self.assertEqual(len(request.line_ids), 1)
        self.assertEqual(request.line_ids[0].consumable_id, self.consumable)
        # Quantity should be equal to qty_order (which is 10.0 in our setUp)
        self.assertEqual(request.line_ids[0].qty, 10.0)

        # Verify that the method raises an error if the request is not in draft state
        request.state = 'ordered'
        with self.assertRaises(UserError):
            request.action_repopulate_lines()
