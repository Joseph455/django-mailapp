import string
import random


def password_generator():
    char = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    return ''.join(random.choice(char) for i in range(7))


