import random, string

def random_string(length: int):
	upper = list(string.ascii_uppercase)
	lower = list(string.ascii_lowercase)
	numbers = list(range(0, 10))
	chars = upper + lower + numbers
	toJoin = [str(chars[random.randint(0, len(chars)-1)]) for _ in range(len(chars))]
	return ''.join(toJoin)


def get_initials(string: str, lower=True) -> str:
	"""
	Return the initials of the given string.

	Arguments
	---------
		string (str) : String to initialize
		lower (bool=True) : return initials in lowercase
	"""
	if lower:
		return ''.join([x[0].lower() for x in string.split(' ')])
	else:
		return ''.join([x[0].upper() for x in string.split(' ')])

