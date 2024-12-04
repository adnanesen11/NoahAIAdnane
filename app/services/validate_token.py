from jwt import encode, decode
from config import JWT_SECRET

def validateJWT(Authtoken):
# If needed to validate the token
        validate = decode(Authtoken, JWT_SECRET, algorithms=["HS256"])
        print('Validate',validate)
        if validate:
            return True
        else:
            return False
