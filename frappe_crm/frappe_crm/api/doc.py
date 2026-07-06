import frappe

@frappe.whitelist()
def upsert(filters=None, **kwargs):
	# If filters are passed in query params and body is JSON, filters might be dropped from form_dict
	if filters is None and frappe.request and frappe.request.args.get("filters"):
		filters = frappe.request.args.get("filters")

	if isinstance(filters, str):
		filters = frappe.parse_json(filters)

	if not filters or not isinstance(filters, list) or len(filters) == 0:
		frappe.throw("Filters must be a list of lists, e.g. [['DocType', 'field', '=', 'value']]")

	doctype = filters[0][0]
	names = frappe.get_list(doctype, filters=filters, limit=1, pluck="name")
	docname = names[0] if names else None

	if docname:
		try:
			doc = frappe.get_doc(doctype, docname)
			doc.update(kwargs)
			doc.save()
			return doc
		except frappe.DoesNotExistError:
			docname = None

	if not docname:
		doc = frappe.new_doc(doctype)
		for f in filters:
			if len(f) == 4 and f[2] == "=":
				doc.set(f[1], f[3])

		doc.update(kwargs)

		# Custom modification: Add retry logic for database deadlocks/lock wait timeouts that happen under concurrent inserts (like Naming Series conflicts)
		import pymysql
		retries = 3
		for attempt in range(retries):
			try:
				doc.insert()
				break
			except pymysql.err.OperationalError as e:
				if e.args[0] in (1213, 1205, 1020) and attempt < retries - 1:
					frappe.db.rollback()
					import time
					import random
					time.sleep(random.uniform(0.1, 0.5))
				else:
					raise

		return doc
