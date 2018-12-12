try:
	from flask import (
		render_template
	)
except ImportError as IE:
	print(f"Error import in controllers/ErrorController.py: {IE}")
	
def error(e):
	"""
	Handles error codes
	Renders error template, passes error
	"""
	status_codes = ["400","401","403","404","405","429","500"]
	status_error = str(e)[:3]
	try:
		index = status_codes.index(status_error)
		error = status_codes[index]
	except:
		try: 
			error=e 
		except:
			error="An error has occured"
	return render_template('index/error.htm.j2', error=error)