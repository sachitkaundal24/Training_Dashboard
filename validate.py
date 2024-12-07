import re

def validate_username(username):
    if not username:
        return {"message": "Username cannot be blank."}
    
    return True

def validate_password(password):
    if not password:
        return {"message":"Password cannot be blank."}
    
    if len(password)<8:
        return {"message":"Password must be at least 8 characters long."}
    
    if not re.search(r"\d",password):
        return {"message": "Password must contain at least one uppercase letter"}
    
    if not re.search(r"[A-Z]",password):
        return {"message": "Password must contain at least one uppercase letter"}
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]",password):
        return {"message": "Password must contain at least one special character"}
    
    return True