import jinja2
from fastapi import FastAPI, Request, Form, Depends, Query, Path
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic
from urllib.parse import urlencode
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
security= HTTPBasic()
app.add_middleware(SessionMiddleware, secret_key="secret")

def set_login_status(request: Request, value: bool):
    session = request.session
    session["SIGNED-IN"] = value

user_db=[
    {
        "username":"test",
        "password":"test"
    }
]


@app.get("/")
def login_form(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})

@app.post("/signin")
def login(request: Request, username:str=Form(""),password:str=Form("")):
    session = request.session
    if  not username or not password:
        error_message = "請輸入帳號密碼"
        query_params = urlencode({"message": error_message})
        error_url = f"/error?{query_params}"
        return RedirectResponse(url=error_url ) 

    for user in user_db:
        if  username == user["username"] and password == user["password"]:
            set_login_status(request, True) 
            break
           
    if  session["SIGNED-IN"] == True:
        return RedirectResponse(url="/member")
    
    else:
        error_message = "帳號、或密碼輸入錯誤"
        query_params = urlencode({"message": error_message})
        error_url = f"/error?{query_params}"
        return RedirectResponse(url=error_url )

@app.get('/member')
def member(request: Request):
    session = request.session
    
    if "SIGNED-IN" in session and session["SIGNED-IN"]:
        return templates.TemplateResponse("member.html", {"request": request})
    else:
        return RedirectResponse(url="/")

@app.post('/member')
def member(request: Request):
    session = request.session
    if session.get("SIGNED-IN", False):
        return templates.TemplateResponse("member.html", {"request": request})
    else:
        return RedirectResponse(url="/signout", status_code=401)

@app.post('/error')
def error(request: Request, message: str = Query("")):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.get('/signout')
def error(request: Request):
    set_login_status(request, False) 
    return RedirectResponse(url="/")

@app.get("/square/{number}")
def square_result(request: Request, number: int):
    square = number * number
    return templates.TemplateResponse("squared.html", {"request": request,"message": f"{square}"})    