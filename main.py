from fastapi import FastAPI, Request, Depends , BackgroundTasks, HTTPException, status
from tortoise import models
from tortoise.contrib.fastapi import register_tortoise
from models import *
from starlette.responses import HTMLResponse
from authontication import * #Auth functions
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from tortoise.signals import post_save
from typing import List, Optional , Type
from tortoise import BaseDBAsyncClient
from fastapi.exceptions import HTTPException
from fastapi import status
from email_service import * 


#response classess
from fastapi.responses import HTMLResponse

app = FastAPI()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")  
@app.post('/token')
async def generate_token(request: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(request.username, request.password)
    return{"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oath2_scheme)):
    try:
        payload = jwt.decode(token, config_credentials["SECRET"], algorithms= ['HS256'])
        user = await User.get(id = payload.get("id"))
    except:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid Username or Password",
            headers={"WWW.Authenticate": "Bearer"}
        )
    return await user




@post_save(User)
async def create_business(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fielsd: List[str]
    ) ->None:
    if created:
        business_obj = await Business.create(
            business_name = instance.username, owner = instance
        )
        await business_pydantic.from_tortoise_orm(business_obj)
        #for email
        await send_email([instance.email], instance)

    
    

@app.get("/")
def index():
    return {"Message": "Hello World"}
    


@app.post("/registration")
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset = True)
    user_info["password"]= get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return{"status": "OK", "data" : f"Hi!{new_user.username}, Thanks for registrations."}
templates = Jinja2Templates(directory="templates")

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)


@app.post("/user/me")
async def user_login(user: user_pydanticIn =Depends(get_current_user)):
    business = await Business.get(owner = user)
    return{
        "status": "ok",
        "data": {
            "username": user.username,
            "email": user.email,
            "verified": user.is_verified,
            "joined_date": user.join_date.strftime("%d %d %Y")
        }
    }



@app.get('/verification', response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
        user = await very_token(token)
        
        if user and not user.is_verified:
            user.is_verified =True
            await user.save()
            return templates.TemplateResponse("verification.html", {"request": request, "username" : user.username})
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Token o Expired",
            headers= {"Authentication": "Failed"}
        )
        
        
        
