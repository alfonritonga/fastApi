from fastapi import HTTPException, FastAPI, Form, Depends
from typing import Annotated
from database import authenticate_user, get_db, create_jwt, exist_user, create_user, current_user
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
blacklisted_tokens = set()

app=FastAPI()

@app.post("/login")
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()], db = Depends(get_db)):
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    jwt_token = create_jwt(user.email, user.fullname, user.guid, user.id)
    user.token = jwt_token
    user.password = ""
    return {
        "status" : "true",
        "data" : user,
        "message" : "success"
    }

@app.get("/user/me")
async def user_me(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = current_user(token)
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
        
    return {
        "status" : "true",
        "data" : payload,
        "message" : "success"
    }


@app.post("/register")
async def register(email: Annotated[str, Form()], fullname: Annotated[str, Form()], password: Annotated[str, Form()], db = Depends(get_db)):
    existing_user = exist_user(email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail={
        "status" : "false",
        "message" : "Email already registered"
    })

    if "@" not in email:
        raise HTTPException(status_code=400, detail={
        "status" : "false",
        "message" : "Invalid email format"
    })

    if len(password) < 8:
        raise HTTPException(status_code=400, detail={
        "status" : "false",
        "message" : "Password must be at least 8 characters long"
    })

    user = create_user(email, fullname, password, db)
    return {
        "status" : "true",
        "data" : user,
        "message" : "regitered new user success"
    }

@app.post("/logout")
async def logout(token: Annotated[str, Depends(oauth2_scheme)]):
    blacklisted_tokens.add(token)
    return {
        "status" : "true",
        "message" : "Token revoked successfully"
    }