from functools import wraps

def logger():
	def decorate(f):
		@wraps(f)
		def decorated_func(*args, **kwargs):
			print("About to run the function", f.__name__)
			result = f(*args, **kwargs)
			if result:
				print("  - {} was successful".format(f.__name__))
			else:
				print("  - {} failed".format(f.__name__))
			return result
		return decorated_func
	return decorate