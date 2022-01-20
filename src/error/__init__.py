"""
custom exceptions 
"""

class MissingDataFrame(Exception):
	"""
       	Raised when get df with api_easiedata fails 
    """
	def __init__(self, *args):
		self.table_name = args[0]

	def __str__(self):
		return f"Error at getting table {self.table_name}"
