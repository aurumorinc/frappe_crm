import frappe
from frappe.tests.utils import FrappeTestCase

from frappe_crm.utils.jinja import get_lead_link

class TestJinjaUtils(FrappeTestCase):
    def setUp(self):
        # Create a mock Lead
        self.lead = frappe.get_doc({
            "doctype": "CRM Lead",
            "first_name": "Test",
            "lead_name": "Test Lead for Link",
        }).insert(ignore_permissions=True)

        # Create a mock Papermark Link
        self.link = frappe.get_doc({
            "doctype": "Link",
            "reference_doctype": "CRM Lead",
            "reference_name": self.lead.name,
            "document": "Test Document",
            "url": "https://example.com/document"
        }).insert(ignore_permissions=True, ignore_links=True)

        # Create a mock Formbricks Personal Link
        self.personal_link = frappe.get_doc({
            "doctype": "Personal Link",
            "reference_doctype": "CRM Lead",
            "reference_name": self.lead.name,
            "survey": "Test Survey",
            "url": "https://example.com/survey"
        }).insert(ignore_permissions=True, ignore_links=True)

    def tearDown(self):
        self.link.delete(force=True)
        self.personal_link.delete(force=True)
        self.lead.delete(force=True)

    def test_get_lead_link_papermark(self):
        url = get_lead_link(self.lead.name, "Test Document")
        self.assertEqual(url, "https://example.com/document")

    def test_get_lead_link_formbricks(self):
        url = get_lead_link(self.lead.name, "Test Survey")
        self.assertEqual(url, "https://example.com/survey")

    def test_get_lead_link_not_found(self):
        url = get_lead_link(self.lead.name, "Non Existent Document")
        self.assertEqual(url, "#")
