# Copyright (c) 2026, Aryan Singh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CRMJobOpening(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		currency: DF.Link | None
		description: DF.TextEditor | None
		employment_type: DF.Link | None
		job_title: DF.Data
		location: DF.Data | None
		lower_range: DF.Currency
		organization: DF.Link
		posted_on: DF.Date | None
		salary_per: DF.Literal["Month", "Year"]
		teable_ref_code: DF.Data | None
		upper_range: DF.Currency
		website: DF.Data | None
	# end: auto-generated types

	pass
