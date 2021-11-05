import os
import hashlib
from django.contrib import messages

ENCRIPTING_ITERATIONS = 10**6 #Minimum recommended is 100,000

def EncryptPassword(password, passwordSalt = os.urandom(32)):
    return (hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        passwordSalt,
        ENCRIPTING_ITERATIONS), passwordSalt)

def SendErrors(request, errors):
    for error in errors:
        messages.error(request, error)