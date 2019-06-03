from hashlib import sha256

SECRET_KEY = ""


# SIGN COOKIE WITH SECRET MESSAGE(SIGNATURE)
def sign_cookie(val):
    str_val = str(val)
    #GENERATE SHA256 COOKIE VALUE
    cookie_sig = sha256(SECRET_KEY + str_val).hexdigest()
    return cookie_sig + "|" + str_val


# CHECKS COOKIE WHETHER IS CORRECT USING SECRET
def evaluate_cookie(val):
    #RETRIEVE THE SIGNITURE VALUE
    sig = val[:val.find('|')]
    #GET THE DECLARED VALUE TO BE COMPARED
    d_val = val[val.find('|') + 1:]
    #CHECK THE COOKIE STATUS
    if sha256(SECRET_KEY + d_val).hexdigest() == sig:
        return d_val
    else:
        return None
