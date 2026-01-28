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

from fastapi import status
from email_service import * 
# for upload images
from fastapi import File, UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image
#response classess
from fastapi.responses import HTMLResponse
#Static file config setup
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name = "static")




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
    
@app.post("/uploadfile/profle")
async def create_upload_files(file: UploadFile = File(...), user: user_pydantic = Depends(get_current_user)):
    FILEPATH = "./static/images/"
    filename= file.filename
    extension = filename.split(".")[1]
    
    if extension not in ["png", "jpg"]:
        return {"status": "Error", "Detail": "File Extension not supported"}
    token_name = secrets.token_hex(10)+ "." + extension
    
    generated_name = FILEPATH +token_name
    file_content = await file.read()
    
    with open(generated_name, "wb") as file:
        file.write(file_content)



    #pillow
    img = Image.open(generated_name)
    img = img.resize(size= (200,200))
    img.save(generated_name)
    file.close()
    
    business = await Business.get(owner = user)
    owner = await business.owner
    
    if owner == user:
        business.logo = token_name
        await business.save()
        
    else:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Not authenticated",
            headers={"WWW.Authenticate": "Bearer"}
        )
    file_location = "localhost:8000"+ generated_name[1:]
    return {"status": "OK", "msg": "Uploaded", "file place" : file_location}







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
    logo = business.logo
    logoplace = "localhost:8000/static/images/" + logo
    return{
        "status": "ok",
        "data": {
            "username": user.username,
            "email": user.email,
            "verified": user.is_verified,
            "joined_date": user.join_date.strftime("%d %d %Y"),
            "business_logo": logoplace
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
        
        
        
@app.post("/uploadfile/product/{id}")
async def create_upload_file(id: int, file: UploadFile = File(...), user: user_pydantic = Depends(get_current_user)):
    FILEPATH = "./static/images/"
    filename= file.filename
    extension = filename.split(".")[1]
    
    if extension not in ["png", "jpg"]:
        return {"status": "Error", "Detail": "File Extension not supported"}
    token_name = secrets.token_hex(10)+ "." + extension
    
    generated_name = FILEPATH +token_name
    file_content = await file.read()
    
    with open(generated_name, "wb") as file:
        file.write(file_content)



    #pillow
    img = Image.open(generated_name)
    img = img.resize(size= (200,200))
    img.save(generated_name)
    file.close()
    
    product = await Product.get(id = id)
    business = await product.business
    owner = await business.owner
    
    if owner == user:
        product.product_image = token_name
        await product.save()
    else:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Token o Expired",
            headers= {"Authentication": "Failed"}
        )
    file_location = "localhost:8000"+ generated_name[1:]
    return {"status": "OK", "msg": "Uploaded", "file place" : file_location}


#CRUD for products
@app.post("/product/create")
async def create_product(product: Product_pydanticIn, user: user_pydantic = Depends(get_current_user)):
    product_data = product.dict(exclude_unset=True)

    # Convert prices to float
    product_data["original_price"] = float(product_data["original_price"])
    product_data["new_price"] = float(product_data["new_price"])

    if product_data["original_price"] <= 0:
        raise HTTPException(status_code=400, detail="Original price must be greater than 0")

    # Calculate discount
    product_data["percentage_discount"] = (
        (product_data["original_price"] - product_data["new_price"]) / product_data["original_price"]
    ) * 100

    # Get the business object for this user
    business = await Business.get(owner=user)

    # Create product
    product_obj = await Product.create(**product_data, business=business)
    product_obj_pydantic = await Product_pydantic.from_tortoise_orm(product_obj)

    # Convert Decimal to float for JSON
    product_dict = product_obj_pydantic.dict()
    product_dict["original_price"] = float(product_dict["original_price"])
    product_dict["new_price"] = float(product_dict["new_price"])

    return {"status": "ok", "data": product_dict}

@app.get("/product")
async def get_product():
    response = await Product_pydantic.from_queryset(Product.all())
    return {"status": "ok", "data": response}


@app.get("/product/{id}")
async def get_product(id: int):
    product = await Product.get(id = id)
    business = await product.business
    owner = await business.owner
    response = await Product_pydantic.from_queryset_single(Product.get(id = id))
    
    return{
        "status": "ok", "data": {
            "product_details": response,
            "business_details": {
                "name": business.business_name,
                "city": business.city,
                "region": business.region,
                "description"  : business.business_description,
                "logo": business.logo,
                "business_id": business.id,
                "owner_id": owner.id,
                "email": owner.email,
                "join_date": owner.join_date.strftime("%b %d %Y")
            }
        }
    }
    
    

@app.put("/product/{id}")
async def update_product(id: int , update_info : Product_pydanticIn, user: user_pydantic = Depends(get_current_user)):
    product = await Product.get(id = id)
    business = await product.business
    owner = await business.owner
    update_info = update_info.dict(exclude_unset = True)
    if user == owner and update_info["original_price"] != 0:
        update_info["percentage_discount"] = ((update_info["original_price"] - update_info["new_price"]) / update_info["original_price"]) * 100
        product = await product.update_from_dict(update_info)
        await product.save()
        response = await Product_pydantic.from_tortoise_orm(product)
        return {"status": "ok" , "data": response}
    else:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED to update this",
            headers= {"Authentication": "Failed"}
        )

@app.put("/business/{id}")
async def update_business(id: int , update_business : business_pydanticIn, user: user_pydantic = Depends(get_current_user)):
    update_business = update_business.dict()
    business = await Business.get(id = id)
    business_owner = await business.owner
    
    # update_info = update_info.dict(exclude_unset = True)
    if user == business_owner:
        await business.update_from_dict(update_business)
        await business.save()
        response = await business_pydantic.from_tortoise_orm(business)
        return {"status": "ok" , "data": response}
    else:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED to update this",
            headers= {"Authentication": "Failed"}
        )

    
@app.delete("/product/{id}")
async def delete_product(id: int , user: user_pydantic = Depends(get_current_user)):
    product = await Product.get(id = id)
    business = await product.business
    owner = await business.owner
    
    if user == owner:
        
        await product.delete()
    else:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED to delete this",
            headers= {"Authentication": "Failed"}
        )
    return {"status": "ok"}