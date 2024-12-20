import random, string

def randomString(length: int):
	upper = list(string.ascii_uppercase)
	lower = list(string.ascii_lowercase)
	numbers = list(range(0, 10))
	chars = upper + lower + numbers
	toJoin = [str(chars[random.randint(0, len(chars)-1)]) for _ in range(len(chars))]
	return ''.join(toJoin)
