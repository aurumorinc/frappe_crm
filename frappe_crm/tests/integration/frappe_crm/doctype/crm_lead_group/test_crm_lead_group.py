# Copyright (c) 2026, Aryan Singh and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


class IntegrationTestCRMLeadGroup(IntegrationTestCase):
	"""
	Integration tests for CRM Lead Group.
	"""

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		# Clear existing potential test records to avoid unique constraint issues
		frappe.db.delete("CRM Lead Group", {"group_name": "Test Partner Lead Group"})

	@classmethod
	def tearDownClass(cls):
		frappe.db.rollback()
		super().tearDownClass()

	def setUp(self):
		super().setUp()

	def tearDown(self):
		frappe.db.rollback()
		super().tearDown()

	def test_crm_lead_with_lead_group(self):
		# 1. Create a CRM Lead Group
		lead_group = frappe.get_doc({
			"doctype": "CRM Lead Group",
			"group_name": "Test Partner Lead Group",
			"description": "Partner source leads"
		})
		lead_group.insert()

		# 2. Create a CRM Lead linking to the lead_group
		lead = frappe.get_doc({
			"doctype": "CRM Lead",
			"first_name": "John",
			"last_name": "Doe",
			"email": "john.doe.group.test@example.com",
			"group": "Test Partner Lead Group"
		})
		lead.insert()

		# 3. Retrieve and assert
		fetched_lead = frappe.get_doc("CRM Lead", lead.name)
		self.assertEqual(fetched_lead.group, "Test Partner Lead Group")
		self.assertEqual(fetched_lead.first_name, "John")
